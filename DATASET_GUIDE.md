# Dataset Import Guide

## 📊 Supported Formats

The system now supports **multiple dataset formats**:

### 1. **CSV Files** ✅ (Most Common)
- **Direct upload**: Upload `.csv` file directly
- **In ZIP**: Upload ZIP file containing `.csv` files
- **Recommended for**: Most datasets, easy to prepare

### 2. **Prolog Files** ✅
- **Format**: `.pl` files in ZIP archive
- **Use case**: Government databases in Prolog format

## 📋 CSV Column Requirements

### Required Columns
Your CSV must have at least these columns (column names are flexible - see mapping below):

| Our Field Name | Acceptable Column Names | Example |
|----------------|------------------------|---------|
| `name` | name, student_name, applicant_name, full_name | "Rajesh Kumar" |
| `family_income` | family_income, income, annual_income, household_income | 2000000 (₹20L) |
| `cibil_score` | cibil_score, credit_score, cibil, credit_rating | 750 |
| `requested_loan_amount` | requested_loan_amount, loan_amount, loan_value, amount | 1500000 (₹15L) |
| `gpa` | gpa, grade_point_average, cgpa | 7.5 (Indian 10-point scale) |
| `postcode` | postcode, postal_code, zip, pincode | "110001" |
| `region` | region, area_type, urban_rural | "urban_tier1" |
| `state` | state, province | "Delhi" |

### Optional Columns (with defaults)
- `profile_id` (auto-generated if missing)
- `course` (defaults to "BTech")
- `educational_background` (defaults to "Engineering")
- `co_applicant` (defaults to "parent")
- `employment_type` (defaults to "student")
- `family_structure` (defaults to "nuclear")
- `test_dimension` (defaults to "geographic")

## 📝 CSV Format Example

```csv
name,family_income,cibil_score,requested_loan_amount,gpa,postcode,region,state,course,employment_type
Rajesh Kumar,2500000,780,1500000,8.5,110001,urban_tier1,Delhi,BTech,salaried
Priya Sharma,1200000,650,800000,7.2,841427,rural_tier2,Bihar,BCom,student
Amit Patel,3000000,820,2000000,9.0,400001,urban_tier1,Mumbai,BTech,government
```

### Region Values
- `urban_tier1` - Urban Tier-1 cities (Delhi, Mumbai, Bangalore, etc.)
- `rural_tier2` - Rural Tier-2 (Bihar, UP, MP, etc.)
- `rural_tier3` - Rural Tier-3 (smaller states)

### Employment Type Values
- `salaried`
- `self-employed`
- `government`
- `student`
- `other`

### Family Structure Values
- `nuclear`
- `joint`
- `single_parent`
- `widow`

## 🚀 How to Upload Your Datasets

### Option 1: Upload via Dashboard UI
1. Start your servers (backend + frontend)
2. Go to http://localhost:3000/dashboard
3. Use the "Upload Student Profile Data" section
4. Drag & drop or click to select your CSV/ZIP file
5. Wait for processing (progress bar will show)

### Option 2: Use API Directly
```bash
curl -X POST "http://localhost:8000/api/v1/profiles/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_dataset.csv"
```

### Option 3: Direct Database Import (For Developers)
```python
from backend.app.services.csv_import_service import csv_import_service
from pathlib import Path

csv_file = Path("your_dataset.csv")
result = csv_import_service.import_csv_file(csv_file, "job_123")
print(f"Imported {result['imported']} profiles")
```

## 🔍 Which Dataset to Use?

### Use **Both Datasets** if:
- They have different characteristics (e.g., one urban, one rural)
- They cover different time periods
- They represent different regions or demographics
- Combined, they provide better diversity

### Use **Dataset 1** if:
- It's larger (more records = better statistical significance)
- It has more complete data (fewer missing fields)
- It represents your target population better

### Use **Dataset 2** if:
- It's more recent or relevant
- It has better data quality
- It covers edge cases better

## 💡 Recommendations

### For Showcase/Presentation:
1. **Use the realistic data generator** first (500 profiles):
   ```bash
   setup-showcase.bat  # Windows
   ./setup-showcase.sh  # Mac/Linux
   ```

2. **Then add your real datasets**:
   - Upload via dashboard
   - They will be added to existing data
   - Metrics will be recalculated with combined dataset

### Best Practice:
- **Generate base dataset** (500 profiles) for guaranteed metrics
- **Add your real datasets** for authenticity and additional diversity
- **Combine multiple datasets** for comprehensive coverage

## 📊 Data Quality Tips

### Before Uploading:
1. **Check column names**: Use standard names (see mapping above)
2. **Validate data types**:
   - Income: Numbers only (₹ symbols removed automatically)
   - CIBIL: 300-900 range
   - GPA: 0.0-10.0 range (Indian 10-point scale)
   - Postcode: 6-digit Indian postcodes
3. **Handle missing values**: System has defaults, but better to provide data
4. **Normalize values**: 
   - Region should be exact: `urban_tier1`, `rural_tier2`, etc.
   - Employment type should match exactly

### After Uploading:
1. **Check dashboard**: Verify profiles appear
2. **Calculate metrics**: Run scoring and metrics calculation
3. **Review results**: Check if bias patterns are detected

## ❓ When to Provide Datasets

**Please share your datasets when:**
1. You're ready to upload them
2. You want me to review the format/columns
3. You need help mapping columns
4. You want to verify compatibility

**I'll need:**
- Dataset format (CSV, Excel, etc.)
- Sample rows (first 2-3 rows) to verify structure
- Column names to ensure proper mapping
- Any special considerations (encoding, delimiters, etc.)

## 🛠️ Troubleshooting

### "Could not detect column mapping"
- Check column names match acceptable names
- Ensure CSV has headers
- Verify file encoding is UTF-8

### "Missing required field"
- Check that required columns are present
- Verify data is not empty/null
- Review error messages for specific missing fields

### "Could not convert value"
- Check numeric fields have valid numbers
- Remove currency symbols, commas from numbers
- Verify GPA is in 0.0-4.0 range
- Verify CIBIL is 300-900 range

---

**Ready to upload?** Share your datasets and I'll help verify they're compatible! 🚀

