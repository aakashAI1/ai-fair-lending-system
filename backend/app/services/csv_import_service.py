"""
CSV import service for student profile data.
Handles CSV files with student loan application data.
"""

import csv
import logging
from pathlib import Path
from typing import List, Dict, Optional
import pandas as pd
from sqlalchemy.orm import Session

from app.models import StudentProfile, TestDimension
from app.database import SessionLocal

logger = logging.getLogger(__name__)


class CSVImportService:
    """Service for importing CSV files with student profile data."""
    
    # Mapping of common column names to our schema
    COLUMN_MAPPINGS = {
        # Profile ID
        'profile_id': ['profile_id', 'id', 'student_id', 'applicant_id'],
        
        # Personal Information
        'name': ['name', 'student_name', 'applicant_name', 'full_name'],
        'postcode': ['postcode', 'postal_code', 'zip', 'pincode'],
        'region': ['region', 'area_type', 'urban_rural'],
        'state': ['state', 'province'],
        
        # Financial Information
        'family_income': ['family_income', 'income', 'annual_income', 'household_income', 'family_salary'],
        'cibil_score': ['cibil_score', 'credit_score', 'cibil', 'credit_rating'],
        'requested_loan_amount': ['requested_loan_amount', 'loan_amount', 'loan_value', 'amount'],
        
        # Academic Information
        'gpa': ['gpa', 'grade_point_average', 'cgpa'],
        'course': ['course', 'degree', 'program', 'programme'],
        'educational_background': ['educational_background', 'education', 'academic_background', 'field'],
        
        # Family Structure
        'co_applicant': ['co_applicant', 'coapplicant', 'co_applicant_type'],
        'employment_type': ['employment_type', 'employment', 'job_type', 'occupation'],
        'family_structure': ['family_structure', 'family_type', 'household_type'],
        
        # Test Dimension (optional)
        'test_dimension': ['test_dimension', 'dimension', 'bias_dimension'],
    }
    
    def detect_column_mapping(self, csv_file_path: Path) -> Dict[str, str]:
        """
        Detect column mapping by reading CSV header.
        Returns mapping: {our_field_name: csv_column_name}
        """
        mapping = {}
        
        try:
            # Read first row to get headers
            with open(csv_file_path, 'r', encoding='utf-8', errors='ignore') as f:
                reader = csv.DictReader(f)
                csv_columns = reader.fieldnames or []
                
                # Normalize CSV column names (lowercase, strip spaces)
                csv_columns_lower = {col.lower().strip(): col for col in csv_columns}
                
                # Try to map each of our fields
                for our_field, possible_names in self.COLUMN_MAPPINGS.items():
                    for possible_name in possible_names:
                        if possible_name.lower() in csv_columns_lower:
                            mapping[our_field] = csv_columns_lower[possible_name.lower()]
                            break
                
                logger.info(f"Detected column mapping: {mapping}")
                return mapping
                
        except Exception as e:
            logger.error(f"Error detecting column mapping: {e}")
            raise
    
    def map_csv_row_to_profile(self, row: Dict, column_mapping: Dict[str, str]) -> Optional[Dict]:
        """
        Map a CSV row to StudentProfile dictionary.
        """
        try:
            profile_data = {}
            
            # Map basic fields
            for our_field, csv_col in column_mapping.items():
                if csv_col in row and row[csv_col]:
                    value = row[csv_col]
                    
                    # Convert based on field type
                    if our_field in ['family_income', 'cibil_score', 'requested_loan_amount']:
                        # Remove currency symbols, commas, etc.
                        value = str(value).replace('₹', '').replace(',', '').replace(' ', '').strip()
                        try:
                            value = int(float(value))
                        except (ValueError, TypeError):
                            logger.warning(f"Could not convert {our_field} value: {row[csv_col]}")
                            value = None
                    elif our_field == 'gpa':
                        try:
                            value = float(value)
                            # Convert 4-point scale to 10-point scale if needed (backward compatibility)
                            # If GPA is <= 4.0, assume it's on 4-point scale and convert to 10-point
                            if value > 0 and value <= 4.0:
                                value = value * 2.5  # Convert 4-point to 10-point scale
                                logger.info(f"Converted GPA from 4-point ({value/2.5:.2f}) to 10-point scale ({value:.2f})")
                            # Ensure value is within valid range
                            value = max(0.0, min(10.0, value))
                        except (ValueError, TypeError):
                            logger.warning(f"Could not convert GPA value: {row[csv_col]}")
                            value = None
                    elif our_field == 'test_dimension':
                        # Try to match to TestDimension enum
                        value_str = str(value).lower().strip()
                        for dim in TestDimension:
                            if dim.value.lower() in value_str or value_str in dim.value.lower():
                                value = dim
                                break
                        else:
                            value = None
                    
                    profile_data[our_field] = value
            
            # Set defaults for required fields
            profile_id = profile_data.get('profile_id') or f"CSV_{hash(str(row))}"
            name = profile_data.get('name') or 'Unknown Student'
            
            # Generate profile_id if not present
            if not profile_data.get('profile_id'):
                import uuid
                profile_data['profile_id'] = f"CSV_{uuid.uuid4().hex[:8].upper()}"
            
            # Set defaults
            profile_data.setdefault('name', 'Unknown Student')
            profile_data.setdefault('postcode', '000000')
            profile_data.setdefault('region', 'urban_tier1')
            profile_data.setdefault('state', 'Unknown')
            profile_data.setdefault('family_income', 2000000)
            profile_data.setdefault('cibil_score', 650)
            profile_data.setdefault('requested_loan_amount', 1000000)
            profile_data.setdefault('gpa', 7.0)  # Default to 7.0 on Indian 10-point scale
            profile_data.setdefault('course', 'BTech')
            profile_data.setdefault('educational_background', 'Engineering')
            profile_data.setdefault('co_applicant', 'parent')
            profile_data.setdefault('employment_type', 'student')
            profile_data.setdefault('family_structure', 'nuclear')
            profile_data.setdefault('test_dimension', TestDimension.GEOGRAPHIC)
            
            # Validate required fields
            required_fields = [
                'profile_id', 'name', 'postcode', 'region', 'state',
                'family_income', 'cibil_score', 'requested_loan_amount',
                'gpa', 'course', 'educational_background'
            ]
            
            for field in required_fields:
                if field not in profile_data or profile_data[field] is None:
                    logger.warning(f"Missing required field: {field} in row")
                    return None
            
            # Ensure test_dimension is a TestDimension enum
            if isinstance(profile_data.get('test_dimension'), str):
                test_dim_str = profile_data['test_dimension'].lower()
                for dim in TestDimension:
                    if dim.value.lower() in test_dim_str:
                        profile_data['test_dimension'] = dim
                        break
                else:
                    profile_data['test_dimension'] = TestDimension.GEOGRAPHIC
            
            return profile_data
            
        except Exception as e:
            logger.error(f"Error mapping CSV row to profile: {e}")
            return None
    
    def import_csv_file(self, csv_file_path: Path, job_id: str, db: Optional[Session] = None) -> Dict:
        """
        Import CSV file and create StudentProfile records.
        
        Returns:
            Dict with import results: {imported, skipped, total, errors}
        """
        if db is None:
            db = SessionLocal()
            should_close = True
        else:
            should_close = False
        
        try:
            # Detect column mapping
            column_mapping = self.detect_column_mapping(csv_file_path)
            
            if not column_mapping:
                raise ValueError("Could not detect column mapping from CSV file. Please check column names.")
            
            # Read CSV file
            profiles_data = []
            errors = []
            
            try:
                # Use pandas for better CSV handling
                df = pd.read_csv(csv_file_path, encoding='utf-8', errors='ignore')
                
                logger.info(f"CSV file loaded: {len(df)} rows, {len(df.columns)} columns")
                
                for idx, row in df.iterrows():
                    try:
                        row_dict = row.to_dict()
                        profile_data = self.map_csv_row_to_profile(row_dict, column_mapping)
                        
                        if profile_data:
                            profiles_data.append(profile_data)
                        else:
                            errors.append(f"Row {idx + 2}: Could not map to profile")
                    except Exception as e:
                        errors.append(f"Row {idx + 2}: {str(e)}")
                        
            except Exception as e:
                # Fallback to standard CSV reader
                logger.warning(f"Pandas read failed, using standard CSV reader: {e}")
                with open(csv_file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    reader = csv.DictReader(f)
                    for idx, row in enumerate(reader):
                        try:
                            profile_data = self.map_csv_row_to_profile(row, column_mapping)
                            if profile_data:
                                profiles_data.append(profile_data)
                            else:
                                errors.append(f"Row {idx + 2}: Could not map to profile")
                        except Exception as e:
                            errors.append(f"Row {idx + 2}: {str(e)}")
            
            logger.info(f"Parsed {len(profiles_data)} valid profiles from CSV")
            
            # Import to database
            imported = 0
            skipped = 0
            
            for profile_data in profiles_data:
                try:
                    # Check if already exists
                    existing = db.query(StudentProfile).filter(
                        StudentProfile.profile_id == profile_data['profile_id']
                    ).first()
                    
                    if existing:
                        skipped += 1
                        continue
                    
                    # Create new profile
                    profile = StudentProfile(**profile_data)
                    db.add(profile)
                    imported += 1
                    
                except Exception as e:
                    logger.error(f"Error creating profile: {e}")
                    errors.append(f"Profile {profile_data.get('profile_id')}: {str(e)}")
            
            db.commit()
            
            return {
                "imported": imported,
                "skipped": skipped,
                "total": len(profiles_data),
                "errors": errors[:10]  # Limit errors in response
            }
            
        finally:
            if should_close:
                db.close()


# Global instance
csv_import_service = CSVImportService()

