# Government Student Loan Database Import

## Overview

Successfully imported **960 student profiles** from the government student loan relational database (Prolog format) into the Fair Lending AI Validation system.

## Data Source

- **Source**: Government student loan database (Prolog format)
- **File**: `student+loan+relational.zip`
- **Format**: Prolog relational database (.pl files)
- **Total Students**: 1,000 students in original database
- **Imported**: 960 profiles (students with enrollment data)

## Data Mapping

The Prolog database was mapped to our `StudentProfile` schema as follows:

### Original Prolog Relations:
- `enrolled(Student, School, Units)` → Enrollment information
- `male(Student)` → Gender identification
- `no_payment_due(Student)` → Loan payment status (643 positive instances)
- `longest_absense_from_school(Student, Months)` → Absence duration
- `enlist(Student, Organization)` → Military/service enrollment
- `unemployed(Student)` → Employment status
- `filed_for_bankrupcy(Student)` → Bankruptcy history
- `disabled(Student)` → Disability status

### Mapped to StudentProfile:
- **Profile ID**: `govt_{original_student_id}` (e.g., `govt_student1000`)
- **Name**: Generated Indian names based on gender
- **Gender**: Mapped from `male()` relation
- **Region/State**: Mapped to Indian states and regions
- **Income**: Calculated based on loan status, employment, and other factors
- **Credit Score**: Derived from bankruptcy, absence, and payment status
- **GPA**: Calculated from enrollment units and absence
- **Course**: Mapped from school type
- **Employment**: Mapped from `unemployed()` relation
- **Test Dimension**: Assigned based on gender, region, income, or credit factors

## Import Statistics

- **Total Profiles Imported**: 960
- **Profile ID Prefix**: `govt_`
- **Data Quality**: All profiles have complete enrollment data
- **Test Dimensions Covered**:
  - Gender bias testing
  - Geographic bias testing
  - Income bias testing
  - Credit score bias testing
  - Edge case scenarios

## Usage

The imported data is now available in the database and can be used for:

1. **Bias Testing**: Real-world student loan data for fairness validation
2. **Scoring**: Generate fair and biased scores for these profiles
3. **Metrics Calculation**: Calculate bias metrics across different dimensions
4. **Mitigation**: Test mitigation strategies on real data

## Import Script

The import script is located at:
```
backend/scripts/import_government_data.py
```

To re-import or update:
```bash
cd backend
python3 scripts/import_government_data.py
```

**Note**: The script skips profiles that already exist (based on `profile_id`), so it's safe to run multiple times.

## Data Characteristics

### Gender Distribution
- Male students: Based on `male()` relation
- Female students: All other students

### Loan Status
- **No Payment Due**: 643 students (positive instances)
- **Payment Due**: 357 students (negative instances)

### Employment Status
- Students with employment data
- Unemployed students flagged

### Special Circumstances
- Disabled students
- Bankruptcy history
- Military/service enrollment
- Long absences from school

## Integration with Existing System

The government data integrates seamlessly with:
- ✅ Profile generation (can mix with GenAI-generated profiles)
- ✅ Scoring service (fair and biased scoring)
- ✅ Metrics calculation (bias detection)
- ✅ Human feedback system
- ✅ Mitigation workflows

## Next Steps

1. **Generate Scores**: Run scoring on the imported profiles
2. **Calculate Metrics**: Analyze bias across dimensions
3. **Compare**: Compare government data results with GenAI-generated profiles
4. **Validate**: Use human feedback to validate findings

## Files

- **Import Script**: `backend/scripts/import_government_data.py`
- **Source Data**: `data_extracted/` (extracted from zip)
- **Database**: `backend/fairlending.db`

