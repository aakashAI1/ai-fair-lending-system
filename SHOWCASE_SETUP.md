# Showcase Setup Guide

This guide will help you set up the dashboard with realistic data for showcasing the Fair Lending AI Validation system.

## Quick Start

### Windows
```bash
setup-showcase.bat
```

### Mac/Linux
```bash
chmod +x setup-showcase.sh
./setup-showcase.sh
```

## What Gets Generated

The setup script automatically creates:

1. **500 Realistic Student Profiles**
   - Properly distributed across all test dimensions
   - Realistic income, credit scores, and academic profiles
   - Geographic diversity (urban/rural, tier-1/2/3)
   - Edge cases included

2. **Fair & Biased Scoring Results**
   - All profiles scored with deterministic fair model
   - All profiles scored with deterministic biased model
   - Clear differences showing bias patterns

3. **Comprehensive Bias Metrics**
   - Metrics calculated across all 5 dimensions:
     - Geographic (Urban vs Rural, Tier-1 vs Tier-2/3)
     - Income (High vs Low income)
     - Credit (Good vs Fair vs Poor credit)
     - Gender (placeholder)
     - Edge Cases (Self-employed, single parent, etc.)
   - Statistical validation (t-tests, p-values, confidence intervals)
   - Severity levels assigned

4. **Sample Human Feedback**
   - Pre-populated feedback for top findings
   - Ready for demonstration of HITL workflow

## Dashboard Features

After running the setup, your dashboard will show:

### KPI Cards
- **Approval Parity**: Ratio of approval rates (Target: ≥0.95)
- **Interest Gap**: Difference in interest rates (Target: <0.5%)
- **Collateral Gap**: Difference in collateral requirements (Target: <10%)
- **Fairness Score**: Overall fairness metric (Target: ≥85/100)

Each KPI card shows:
- Current value vs target
- Pass/fail indicator
- Color-coded status (green = pass, red = fail)
- Professional styling with icons

### Bias Heatmap
- Visual representation of bias findings across dimensions
- Color-coded severity levels (Critical, High, Medium, Low)
- Total counts per dimension
- Easy to identify problem areas

### Top Findings
- Most critical bias issues
- Detailed descriptions
- Group comparisons
- Severity indicators

## Scoring Models

### Fair Scoring Model
- **Academic Merit (40%)**: Based on GPA and educational background
- **Creditworthiness (30%)**: Based on CIBIL score
- **Repayment Capacity (30%)**: Based on income-to-loan ratio and stability

**Key Feature**: Completely ignores demographic factors (geography, income level, family structure)

### Biased Scoring Model
Applies realistic biases:
- **Rural Penalty**: -2.0 points for rural locations
- **Low Income Penalty**: -1.0 point for income <₹20L
- **Self-Employed Penalty**: -1.5 points
- **Tier-2/3 Penalty**: -1.0 point
- **State-Based Penalty**: -0.5 points for certain states
- **Single Parent/Widow Penalty**: -1.0 point

**Result**: Clear, measurable bias differences for demonstration

## Metrics Accuracy

All metrics are calculated using:
- **Pandas** for data manipulation
- **SciPy** for statistical validation
- **NumPy** for numerical calculations
- Proper statistical tests (t-tests, confidence intervals)
- Accurate group comparisons

## Verification

After setup, verify your data:

1. **Backend API**: http://localhost:8000/docs
   - Check `/api/v1/dashboard` endpoint
   - Should return comprehensive metrics

2. **Frontend Dashboard**: http://localhost:3000/dashboard
   - Should show KPI cards with values
   - Heatmap should display data
   - Top findings should appear

3. **Bias Analysis**: http://localhost:3000/bias-analysis
   - Should show detailed metrics table
   - Filterable by dimension and severity

## Troubleshooting

### No Data Appears
- Ensure backend is running: `cd backend && python -m uvicorn app.main:app --reload`
- Check database file exists: `backend/fairlending.db`
- Verify script completed successfully

### Metrics Look Incorrect
- Ensure profiles are scored (both fair and biased)
- Check metrics calculation ran successfully
- Verify test_run_id in database

### Dashboard Not Loading
- Ensure frontend is running: `cd frontend && npm run dev`
- Check API connection: http://localhost:8000/health
- Verify CORS settings in backend

## Customization

You can customize the number of profiles generated:

```python
# Edit backend/scripts/generate_realistic_data.py
# Change num_profiles parameter (default: 500)

# Or run directly:
cd backend
python scripts/generate_realistic_data.py 1000  # Generate 1000 profiles
```

## Regenerating Data

To regenerate data with fresh profiles:

1. Delete existing database (optional):
   ```bash
   rm backend/fairlending.db  # Mac/Linux
   del backend\fairlending.db  # Windows
   ```

2. Run setup script again:
   ```bash
   setup-showcase.bat  # Windows
   ./setup-showcase.sh  # Mac/Linux
   ```

## Next Steps for Showcase

1. ✅ Run setup script to generate data
2. ✅ Start backend and frontend servers
3. ✅ Navigate through dashboard pages
4. ✅ Demonstrate bias detection
5. ✅ Show human feedback workflow
6. ✅ Demonstrate mitigation process

## Showcase Flow

### Recommended Demonstration Order:

1. **Dashboard Overview** (http://localhost:3000/dashboard)
   - Show KPI cards with pass/fail indicators
   - Explain what each metric means
   - Point out areas needing attention

2. **Bias Analysis** (http://localhost:3000/bias-analysis)
   - Filter by dimension
   - Show detailed comparisons
   - Explain statistical significance

3. **Feedback Page** (http://localhost:3000/feedback)
   - Show how humans can provide feedback
   - Demonstrate annotation workflow

4. **Mitigation Page** (http://localhost:3000/mitigation)
   - Show iterative improvement process
   - Demonstrate before/after comparisons

## Support

For issues or questions:
- Check logs: `backend/app/main.py` console output
- API docs: http://localhost:8000/docs
- Review error messages in browser console (F12)

---

**Ready for Showcase!** 🚀

Your dashboard is now populated with realistic data and ready to demonstrate the Fair Lending AI Validation system.

