"""
Service for processing uploaded student profile data files.
"""

import os
import zipfile
import tempfile
import shutil
import logging
import uuid
from pathlib import Path
from typing import Dict, Optional
from sqlalchemy.orm import Session

from app.models import StudentProfile, TestDimension
from app.database import SessionLocal

logger = logging.getLogger(__name__)

# Note: We'll import the parser functions dynamically to avoid circular imports


class FileUploadService:
    """Service for processing uploaded files."""
    
    def __init__(self):
        self.upload_dir = Path(__file__).parent.parent.parent / "uploads"
        self.upload_dir.mkdir(exist_ok=True)
        self.processing_jobs: Dict[str, Dict] = {}
    
    def process_upload(self, file_path: Path, job_id: str) -> Dict:
        """
        Process an uploaded file and import student profiles.
        
        Args:
            file_path: Path to the uploaded file
            job_id: Unique job identifier for tracking
            
        Returns:
            Dict with processing results
        """
        try:
            self.processing_jobs[job_id] = {
                "status": "processing",
                "progress": 0,
                "imported": 0,
                "total": 0,
                "error": None
            }
            
            # Extract if zip file
            extract_dir = None
            if file_path.suffix.lower() == ".zip":
                extract_dir = self._extract_zip(file_path, job_id)
                data_dir = extract_dir
            else:
                data_dir = file_path.parent
            
            # Detect file type and process
            if self._is_prolog_database(data_dir):
                logger.info(f"Detected Prolog database format")
                result = self._process_prolog_data(data_dir, job_id)
            elif self._is_csv_file(file_path, data_dir):
                logger.info(f"Detected CSV format")
                result = self._process_csv_data(file_path, data_dir, job_id)
            else:
                raise ValueError("Unsupported file format. Please upload a ZIP file containing Prolog (.pl) files or a CSV file.")
            
            # Cleanup
            if extract_dir and extract_dir.exists():
                shutil.rmtree(extract_dir, ignore_errors=True)
            
            self.processing_jobs[job_id]["status"] = "completed"
            self.processing_jobs[job_id]["progress"] = 100
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing upload: {e}", exc_info=True)
            self.processing_jobs[job_id] = {
                "status": "failed",
                "error": str(e)
            }
            raise
    
    def _extract_zip(self, zip_path: Path, job_id: str) -> Path:
        """Extract ZIP file to temporary directory."""
        extract_dir = self.upload_dir / f"extract_{job_id}"
        extract_dir.mkdir(exist_ok=True)
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        
        logger.info(f"Extracted ZIP to {extract_dir}")
        return extract_dir
    
    def _is_prolog_database(self, data_dir: Path) -> bool:
        """Check if directory contains Prolog database files."""
        prolog_files = list(data_dir.glob("*.pl"))
        return len(prolog_files) > 0
    
    def _is_csv_file(self, file_path: Path, data_dir: Path) -> bool:
        """Check if file is a CSV file."""
        # Check if the uploaded file itself is CSV
        if file_path.suffix.lower() == ".csv":
            return True
        # Check if extracted directory contains CSV files
        csv_files = list(data_dir.glob("*.csv"))
        return len(csv_files) > 0
    
    def _process_prolog_data(self, data_dir: Path, job_id: str) -> Dict:
        """Process Prolog database files and import to database."""
        # Import the parser functions directly
        import sys
        # Path: backend/app/services/file_upload_service.py -> backend/scripts
        # file_upload_service.py is at: backend/app/services/
        # parent.parent.parent = backend/
        scripts_path = Path(__file__).parent.parent.parent / "scripts"
        if str(scripts_path) not in sys.path:
            sys.path.insert(0, str(scripts_path))
        
        # Import with full path
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "import_government_data",
            scripts_path / "import_government_data.py"
        )
        import_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(import_module)
        
        # Temporarily set the data directory
        original_data_dir = import_module.DATA_DIR
        import_module.DATA_DIR = data_dir
        
        try:
            # Load all data
            logger.info("Loading Prolog data...")
            data = import_module.load_all_data()
            
            total_students = len(data['students'])
            self.processing_jobs[job_id]["total"] = total_students
            
            # Convert to profiles
            profiles = []
            students_list = sorted(data['students'])
            
            logger.info(f"Converting {len(students_list)} students to profiles...")
            
            for idx, student_id in enumerate(students_list):
                profile_data = import_module.map_to_student_profile(student_id, data)
                if profile_data:
                    profiles.append(profile_data)
                
                # Update progress
                if (idx + 1) % 10 == 0:
                    progress = int((idx + 1) / total_students * 100)
                    self.processing_jobs[job_id]["progress"] = progress
            
            # Import to database
            logger.info(f"Importing {len(profiles)} profiles to database...")
            db = SessionLocal()
            imported = 0
            skipped = 0
            
            try:
                for idx, profile_data in enumerate(profiles):
                    # Check if already exists
                    existing = db.query(StudentProfile).filter(
                        StudentProfile.profile_id == profile_data['profile_id']
                    ).first()
                    
                    if existing:
                        skipped += 1
                        continue
                    
                    # Create new profile
                    profile = StudentProfile(**{k: v for k, v in profile_data.items() if k != '_metadata'})
                    db.add(profile)
                    imported += 1
                    
                    # Update progress
                    if (idx + 1) % 50 == 0:
                        db.commit()
                        progress = int((idx + 1) / len(profiles) * 100)
                        self.processing_jobs[job_id]["progress"] = progress
                        self.processing_jobs[job_id]["imported"] = imported
                
                db.commit()
                
            finally:
                db.close()
            
            self.processing_jobs[job_id]["imported"] = imported
            
            logger.info(f"Import complete: {imported} imported, {skipped} skipped")
            
            return {
                "imported": imported,
                "skipped": skipped,
                "total": len(profiles)
            }
            
        finally:
            # Restore original data directory
            import_module.DATA_DIR = original_data_dir
            # Clean up sys.path
            if str(scripts_path) in sys.path:
                sys.path.remove(str(scripts_path))
    
    def _process_csv_data(self, file_path: Path, data_dir: Path, job_id: str) -> Dict:
        """Process CSV file and import to database."""
        from app.services.csv_import_service import csv_import_service
        
        # Find CSV file
        if file_path.suffix.lower() == ".csv":
            csv_file = file_path
        else:
            csv_files = list(data_dir.glob("*.csv"))
            if not csv_files:
                raise ValueError("No CSV files found in uploaded archive")
            csv_file = csv_files[0]
        
        logger.info(f"Processing CSV file: {csv_file}")
        
        # Import CSV
        result = csv_import_service.import_csv_file(csv_file, job_id)
        
        # Update job status
        self.processing_jobs[job_id]["imported"] = result["imported"]
        self.processing_jobs[job_id]["total"] = result["total"]
        
        return result
    
    def get_job_status(self, job_id: str) -> Optional[Dict]:
        """Get status of a processing job."""
        return self.processing_jobs.get(job_id)


# Global instance
file_upload_service = FileUploadService()

