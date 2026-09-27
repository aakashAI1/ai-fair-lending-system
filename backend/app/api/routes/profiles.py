"""
API routes for profile generation and management.
"""

import logging
import uuid
import os
import random
from typing import List
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, UploadFile, File
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.api.deps import get_database
from app.models import StudentProfile, TestRun, TestDimension
from app.schemas import (
    ProfileGenerationRequest,
    ProfileGenerationResponse,
    StudentProfileResponse,
    StudentProfileCreate
)
from app.services.genai_service import genai_service
from app.services.file_upload_service import file_upload_service
from app.database import Base, engine

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/profiles", tags=["profiles"])

# Upload directory
UPLOAD_DIR = Path(__file__).parent.parent.parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/generate", response_model=ProfileGenerationResponse)
async def generate_profiles(
    request: ProfileGenerationRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_database)
):
    """
    Generate synthetic student profiles using GenAI.
    """
    try:
        test_run_id = f"TEST_{uuid.uuid4().hex[:8]}"
        
        # Create test run record
        test_run = TestRun(
            test_run_id=test_run_id,
            profile_count=request.count,
            dimensions_tested=[d.value for d in request.dimensions],
            status="generating",
            progress_percentage=0.0
        )
        db.add(test_run)
        db.commit()
        
        # Generate profiles in background
        async def generate_task():
            from app.database import SessionLocal
            # Import models here to avoid scope issues
            from app.models import TestDimension as TestDim, ScoringType
            bg_db = SessionLocal()
            try:
                logger.info(f"Starting profile generation for {request.count} profiles...")
                profiles_data = await genai_service.generate_profiles(
                    count=request.count,
                    dimensions=[d.value for d in request.dimensions],
                    batch_size=request.batch_size
                )
                
                if not profiles_data:
                    raise ValueError("No profiles were generated")
                
                logger.info(f"Generated {len(profiles_data)} profiles, saving to database...")
                
                # Save profiles to database
                profile_ids_created = []
                save_errors = []
                # Get the highest existing profile ID number to continue sequence
                max_profile = bg_db.query(StudentProfile).order_by(StudentProfile.id.desc()).first()
                start_num = (max_profile.id + 1) if max_profile else 1
                
                for idx, profile_data in enumerate(profiles_data):
                    try:
                        # Generate sequential profile ID: stud_001, stud_002, etc.
                        profile_id = profile_data.get("profile_id") or f"stud_{start_num + idx:03d}"
                        
                        # Check for duplicate profile_id
                        existing = bg_db.query(StudentProfile).filter(
                            StudentProfile.profile_id == profile_id
                        ).first()
                        
                        if existing:
                            # Find next available number
                            counter = start_num + idx + 1
                            while bg_db.query(StudentProfile).filter(
                                StudentProfile.profile_id == f"stud_{counter:03d}"
                            ).first():
                                counter += 1
                            profile_id = f"stud_{counter:03d}"
                        
                        # Validate and set name - ensure it's always present with a real name (without numbers)
                        name_value = profile_data.get("name")
                        if not name_value or (isinstance(name_value, str) and name_value.strip() == ""):
                            # Generate a realistic Indian name from shared list (no numbers)
                            import re
                            name_value = None
                        elif name_value:
                            # Remove any trailing numbers from name (e.g., "Kiran Reddy 000" -> "Kiran Reddy")
                            import re
                            name_value = re.sub(r'\s+\d+$', '', str(name_value).strip()).strip()
                        
                        if not name_value:
                            try:
                                from app.data.indian_names import INDIAN_NAMES
                            except ImportError:
                                # Fallback if module doesn't exist
                                INDIAN_NAMES = [
                                    "Rajesh Kumar", "Priya Sharma", "Amit Patel", "Sneha Reddy", "Vikram Singh",
                                    "Anjali Gupta", "Rahul Mehta", "Kavita Desai", "Suresh Iyer", "Meera Nair",
                                    "Arjun Joshi", "Divya Rao", "Karan Malhotra", "Pooja Shah", "Nikhil Agarwal",
                                    "Riya Kapoor", "Aditya Verma", "Shreya Chaturvedi", "Rohan Bhatia", "Neha Trivedi",
                                    "Ravi Kumar", "Sunita Patel", "Manoj Singh", "Kiran Reddy", "Deepak Sharma",
                                    "Nisha Gupta", "Vivek Agarwal", "Manisha Desai", "Sachin Iyer", "Preeti Nair",
                                    "Akshay Kumar", "Jyoti Singh", "Varun Patel", "Swati Reddy", "Ajay Kumar",
                                    "Kavita Sharma", "Nikhil Patel", "Anita Iyer", "Rohit Nair", "Pooja Desai"
                                ]
                            name_value = random.choice(INDIAN_NAMES)
                        else:
                            name_value = str(name_value).strip()
                        
                        # Truncate name if too long
                        if len(name_value) > 200:
                            name_value = name_value[:200]
                        
                        # Ensure test_dimension is valid enum value
                        test_dim_str = profile_data.get("test_dimension", "geographic")
                        try:
                            if isinstance(test_dim_str, str):
                                test_dim = TestDim(test_dim_str.lower())
                            else:
                                test_dim = TestDim(test_dim_str)
                        except (ValueError, AttributeError):
                            # Invalid test dimension, default to geographic
                            test_dim = TestDim.GEOGRAPHIC
                        
                        profile = StudentProfile(
                            profile_id=profile_id,
                            name=name_value,  # Use validated name
                            postcode=str(profile_data.get("postcode") or "000000")[:10],
                            region=str(profile_data.get("region") or "urban_tier1")[:50],
                            state=str(profile_data.get("state") or "Maharashtra")[:50],
                            family_income=int(profile_data.get("family_income", 1000000)),
                            cibil_score=int(profile_data.get("cibil_score", 600)),
                            requested_loan_amount=int(profile_data.get("requested_loan_amount", 500000)),
                            gpa=float(profile_data.get("gpa", 7.0)),
                            course=str(profile_data.get("course") or "BTech")[:100],
                            educational_background=str(profile_data.get("educational_background") or "Engineering")[:100],
                            co_applicant=profile_data.get("co_applicant")[:50] if profile_data.get("co_applicant") else None,
                            employment_type=str(profile_data.get("employment_type") or "student")[:50],
                            family_structure=str(profile_data.get("family_structure") or "nuclear")[:50],
                            test_dimension=test_dim
                        )
                        bg_db.add(profile)
                        bg_db.flush()  # Flush to get the ID
                        profile_ids_created.append(profile.id)
                        logger.debug(f"Successfully saved profile {idx+1}/{len(profiles_data)}: {profile_id}")
                    except Exception as e:
                        error_detail = f"Profile {idx+1}: {str(e)}"
                        logger.error(f"Error saving profile {idx}: {error_detail}", exc_info=True)
                        save_errors.append(error_detail)
                        # Continue with next profile
                        continue
                
                if not profile_ids_created:
                    error_summary = f"Failed to save any profiles to database. Errors: {'; '.join(save_errors[:5])}"
                    logger.error(error_summary)
                    raise ValueError(error_summary)
                
                # Commit all saved profiles
                bg_db.commit()
                logger.info(f"Committed {len(profile_ids_created)} profiles to database")
                
                # Update test run
                test_run = bg_db.query(TestRun).filter(TestRun.test_run_id == test_run_id).first()
                if test_run:
                    test_run.total_profiles_generated = len(profile_ids_created)
                    test_run.status = "completed"
                    test_run.progress_percentage = 100.0
                    bg_db.commit()
                    logger.info(f"Updated test_run {test_run_id}: {len(profile_ids_created)} profiles generated")
                
                logger.info(f"Successfully saved {len(profile_ids_created)} profiles for test_run_id: {test_run_id}")
                
                # Automatically score profiles (fair and biased)
                from app.services.scoring_service import ScoringService
                
                logger.info("Starting automatic scoring for generated profiles...")
                scoring_service = ScoringService(bg_db)
                
                # Score with fair model
                try:
                    logger.info(f"Scoring {len(profile_ids_created)} profiles with FAIR scoring...")
                    await scoring_service.score_profiles(
                        profile_ids=profile_ids_created,
                        scoring_type=ScoringType.FAIR,
                        batch_size=100
                    )
                    logger.info("FAIR scoring completed")
                except Exception as e:
                    logger.error(f"Error in FAIR scoring: {e}", exc_info=True)
                
                # Score with biased model
                try:
                    logger.info(f"Scoring {len(profile_ids_created)} profiles with BIASED scoring...")
                    await scoring_service.score_profiles(
                        profile_ids=profile_ids_created,
                        scoring_type=ScoringType.BIASED,
                        batch_size=100
                    )
                    logger.info("BIASED scoring completed")
                except Exception as e:
                    logger.error(f"Error in BIASED scoring: {e}", exc_info=True)
                
                # Automatically calculate metrics
                from app.services.metrics_service import MetricsService
                
                try:
                    logger.info("Calculating bias metrics...")
                    metrics_service = MetricsService(bg_db)
                    metrics_service.calculate_bias_metrics(
                        test_run_id=test_run_id,
                        dimensions=[
                            TestDim.GEOGRAPHIC,
                            TestDim.INCOME,
                            TestDim.CREDIT,
                            TestDim.EDGE_CASES
                        ]
                    )
                    logger.info("Metrics calculation completed")
                except Exception as e:
                    logger.error(f"Error calculating metrics: {e}", exc_info=True)
                
            except Exception as e:
                error_msg = str(e)
                logger.error(f"Error generating profiles: {error_msg}", exc_info=True)
                test_run = bg_db.query(TestRun).filter(TestRun.test_run_id == test_run_id).first()
                if test_run:
                    test_run.status = "failed"
                    test_run.error_message = error_msg[:500]  # Limit error message length
                    bg_db.commit()
                    logger.info(f"Updated test_run {test_run_id} status to 'failed' with error: {error_msg[:100]}")
            finally:
                bg_db.close()
        
        # Start background task (run async function properly)
        import asyncio
        import threading
        
        def run_async_task():
            """Run async task in a new thread with its own event loop."""
            from app.database import SessionLocal as TaskSessionLocal
            
            def run_in_new_loop():
                """Create a new event loop in this thread and run the async task."""
                try:
                    # Create a completely new event loop for this thread
                    new_loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(new_loop)
                    try:
                        new_loop.run_until_complete(generate_task())
                    finally:
                        new_loop.close()
                except Exception as e:
                    logger.error(f"Error in async task runner: {e}", exc_info=True)
                    # Update test run status even if async runner fails
                    try:
                        bg_db = TaskSessionLocal()
                        test_run = bg_db.query(TestRun).filter(TestRun.test_run_id == test_run_id).first()
                        if test_run:
                            test_run.status = "failed"
                            test_run.error_message = f"Async task error: {str(e)[:500]}"
                            bg_db.commit()
                        bg_db.close()
                    except Exception as db_err:
                        logger.error(f"Error updating test run status: {db_err}", exc_info=True)
            
            # Run in a separate thread to avoid blocking and event loop conflicts
            thread = threading.Thread(target=run_in_new_loop, daemon=True)
            thread.start()
        
        background_tasks.add_task(run_async_task)
        
        return ProfileGenerationResponse(
            test_run_id=test_run_id,
            total_generated=0,
            profiles=[],
            status="generating",
            progress_percentage=0.0
        )
        
    except Exception as e:
        logger.error(f"Error in generate_profiles: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/test-run/{test_run_id}")
async def get_test_run_status(
    test_run_id: str,
    db: Session = Depends(get_database)
):
    """
    Get the status and generated count for a test run.
    """
    try:
        test_run = db.query(TestRun).filter(TestRun.test_run_id == test_run_id).first()
        if not test_run:
            raise HTTPException(status_code=404, detail="Test run not found")
        
        return {
            "test_run_id": test_run.test_run_id,
            "status": test_run.status,
            "total_profiles_generated": test_run.total_profiles_generated or 0,
            "progress_percentage": test_run.progress_percentage or 0.0,
            "error_message": test_run.error_message
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting test run status: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[StudentProfileResponse])
async def list_profiles(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_database)
):
    """
    List all student profiles.
    """
    try:
        profiles = db.query(StudentProfile).offset(skip).limit(limit).all()
        
        # Ensure all profiles have names (fix any existing profiles without names)
        updated_count = 0
        try:
            from app.data.indian_names import INDIAN_NAMES
        except ImportError:
            # Fallback if module doesn't exist
            INDIAN_NAMES = [
                "Rajesh Kumar", "Priya Sharma", "Amit Patel", "Sneha Reddy", "Vikram Singh",
                "Anjali Gupta", "Rahul Mehta", "Kavita Desai", "Suresh Iyer", "Meera Nair",
                "Arjun Joshi", "Divya Rao", "Karan Malhotra", "Pooja Shah", "Nikhil Agarwal",
                "Riya Kapoor", "Aditya Verma", "Shreya Chaturvedi", "Rohan Bhatia", "Neha Trivedi",
                "Ravi Kumar", "Sunita Patel", "Manoj Singh", "Kiran Reddy", "Deepak Sharma",
                "Nisha Gupta", "Vivek Agarwal", "Manisha Desai", "Sachin Iyer", "Preeti Nair",
                "Akshay Kumar", "Jyoti Singh", "Varun Patel", "Swati Reddy", "Ajay Kumar",
                "Kavita Sharma", "Nikhil Patel", "Anita Iyer", "Rohit Nair", "Pooja Desai"
            ]
        for profile in profiles:
            # Check if name is missing, empty, or is a fallback name
            name_str = str(profile.name).strip() if profile.name else ""
            # Remove trailing numbers from names
            import re
            name_str = re.sub(r'\s+\d+$', '', name_str).strip()
            is_fallback = (
                name_str.startswith("Student ") or 
                name_str.startswith("STU_") or
                name_str == profile.profile_id or 
                not name_str or
                re.search(r'\s+\d+$', str(profile.name).strip())  # Has trailing numbers
            )
            
            if is_fallback or name_str != str(profile.name).strip():
                profile.name = random.choice(INDIAN_NAMES)
                updated_count += 1
        
        if updated_count > 0:
            try:
                db.commit()
                logger.info(f"Updated {updated_count} profiles with missing names")
            except Exception as commit_err:
                logger.error(f"Error committing name updates: {commit_err}", exc_info=True)
                db.rollback()
        
        return profiles
    except Exception as e:
        logger.error(f"Error listing profiles: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{profile_id}", response_model=StudentProfileResponse)
async def get_profile(
    profile_id: int,
    db: Session = Depends(get_database)
):
    """
    Get a specific student profile.
    """
    try:
        profile = db.query(StudentProfile).filter(StudentProfile.id == profile_id).first()
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        # Ensure profile has a name (fix if missing or is a fallback or has numbers)
        name_str = str(profile.name).strip() if profile.name else ""
        import re
        # Remove trailing numbers from names
        name_str_cleaned = re.sub(r'\s+\d+$', '', name_str).strip()
        is_fallback = (
            name_str.startswith("Student ") or 
            name_str.startswith("STU_") or
            name_str == profile.profile_id or 
            not name_str or
            re.search(r'\s+\d+$', str(profile.name).strip())  # Has trailing numbers
        )
        
        if is_fallback or name_str_cleaned != name_str:
            try:
                from app.data.indian_names import INDIAN_NAMES
            except ImportError:
                # Fallback if module doesn't exist
                INDIAN_NAMES = [
                    "Rajesh Kumar", "Priya Sharma", "Amit Patel", "Sneha Reddy", "Vikram Singh",
                    "Anjali Gupta", "Rahul Mehta", "Kavita Desai", "Suresh Iyer", "Meera Nair",
                    "Arjun Joshi", "Divya Rao", "Karan Malhotra", "Pooja Shah", "Nikhil Agarwal",
                    "Riya Kapoor", "Aditya Verma", "Shreya Chaturvedi", "Rohan Bhatia", "Neha Trivedi",
                    "Ravi Kumar", "Sunita Patel", "Manoj Singh", "Kiran Reddy", "Deepak Sharma",
                    "Nisha Gupta", "Vivek Agarwal", "Manisha Desai", "Sachin Iyer", "Preeti Nair",
                    "Akshay Kumar", "Jyoti Singh", "Varun Patel", "Swati Reddy", "Ajay Kumar",
                    "Kavita Sharma", "Nikhil Patel", "Anita Iyer", "Rohit Nair", "Pooja Desai"
                ]
            profile.name = random.choice(INDIAN_NAMES)
            try:
                db.commit()
                logger.info(f"Updated profile {profile_id} with missing name")
            except Exception as commit_err:
                logger.error(f"Error committing name update: {commit_err}", exc_info=True)
                db.rollback()
        
        return profile
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting profile: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """
    Upload a ZIP file containing student profile data.
    Supports Prolog database format (.pl files).
    """
    try:
        # Validate file type
        if not (file.filename.endswith(".zip") or file.filename.endswith(".csv")):
            raise HTTPException(
                status_code=400,
                detail="Only ZIP files (containing .pl or .csv files) or CSV files are supported"
            )
        
        # Generate job ID
        job_id = f"upload_{uuid.uuid4().hex[:12]}"
        
        # Save uploaded file
        file_path = UPLOAD_DIR / f"{job_id}_{file.filename}"
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        logger.info(f"File uploaded: {file.filename}, size: {len(content)} bytes")
        
        # Process in background
        def process_task():
            try:
                file_upload_service.process_upload(file_path, job_id)
            except Exception as e:
                logger.error(f"Error in background processing: {e}", exc_info=True)
                file_upload_service.processing_jobs[job_id] = {
                    "status": "failed",
                    "error": str(e)
                }
            finally:
                # Cleanup uploaded file after processing
                if file_path.exists():
                    file_path.unlink()
        
        if background_tasks:
            background_tasks.add_task(process_task)
        else:
            # If no background tasks, process synchronously (for testing)
            process_task()
        
        return JSONResponse({
            "job_id": job_id,
            "status": "uploaded",
            "message": "File uploaded successfully. Processing in background."
        })
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading file: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to upload file: {str(e)}")


@router.get("/upload/status/{job_id}")
async def get_upload_status(job_id: str):
    """
    Get the status of a file upload/processing job.
    """
    status = file_upload_service.get_job_status(job_id)
    
    if not status:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return JSONResponse({
        "job_id": job_id,
        "status": status.get("status", "unknown"),
        "progress": status.get("progress", 0),
        "imported": status.get("imported", 0),
        "total": status.get("total", 0),
        "error": status.get("error")
    })







