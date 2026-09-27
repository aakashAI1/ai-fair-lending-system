# Current Functionalities: Fair Lending AI Validation Platform

## Overview
The platform is a Human-in-the-Loop (HITL) system for detecting and analyzing bias in education loan approval AI systems. It supports both synthetic profile generation and real data import, with dual scoring (fair vs biased) and statistical bias analysis.

---

## 1. Profile Management

### ✅ GenAI Profile Generation
- **Endpoint**: `POST /api/v1/profiles/generate`
- **Functionality**: 
  - Generates synthetic Indian student loan profiles using Google Gemini AI
  - Supports batch generation with configurable count
  - Ensures diversity across test dimensions (geographic, income, credit, edge cases)
  - Creates realistic profiles with: name, location, financial data, academic data, family structure
  - Automatically creates TestRun record to track the generation batch

### ✅ CSV File Import
- **Endpoint**: `POST /api/v1/profiles/upload`
- **Functionality**:
  - Upload CSV files containing student loan data
  - Supports two dataset formats:
    - `fair_lending_audit_realistic_500.csv` format
    - `super_loan_dataset_v3_no_interview.csv` format
  - Automatically maps CSV columns to StudentProfile schema
  - Handles missing/null values with defaults
  - Validates data before database insertion

### ✅ Profile Listing & Retrieval
- **Endpoints**: 
  - `GET /api/v1/profiles/` - List all profiles (with pagination)
  - `GET /api/v1/profiles/{profile_id}` - Get single profile details
- **Functionality**: View profile data, filter by test dimension

---

## 2. Scoring System

### ✅ Fair (Unbiased) Scoring
- **Endpoint**: `POST /api/v1/scoring/fair`
- **Functionality**:
  - Uses `DeterministicScoringEngine` for rule-based scoring
  - Formula: Academic Merit (40%) + Creditworthiness (30%) + Repayment Capacity (30%)
  - Ignores geographic/income/demographic factors (unbiased)
  - Produces consistent, explainable results
  - Outputs: score (1-10), approval_decision, interest_rate, collateral_required

### ✅ Biased Scoring
- **Endpoint**: `POST /api/v1/scoring/biased`
- **Functionality**:
  - **If ML model trained**: Uses `MLScoringModel.predict_score()` (trained on real loan data)
  - **If ML model not available**: Falls back to `DeterministicScoringEngine.calculate_biased_score()` with simulated bias
  - Applies bias penalties for: rural regions, low income, self-employed, tier-2/3 regions
  - Enables A/B comparison with fair scoring

### ✅ Scoring Results Retrieval
- **Endpoint**: `GET /api/v1/scoring/results/{profile_id}`
- **Functionality**: View scoring results for a specific profile

---

## 3. ML Model Training

### ✅ ML Model Training Script
- **Script**: `backend/scripts/train_ml_model.py`
- **Functionality**:
  - Imports and maps two datasets to StudentProfile format
  - Trains RandomForest classifier on historical loan approval data
  - Features: GPA, CIBIL score, family income, loan amount, education, employment, region, state
  - Saves trained model to `backend/models/scoring_model.pkl`
  - Automatically scores all profiles with both fair and biased models
  - Calculates bias metrics after training
  - Updates TestRun record with results

---

## 4. Bias Metrics Calculation

### ✅ Metrics Calculation
- **Endpoint**: `POST /api/v1/metrics/calculate`
- **Functionality**:
  - Calculates bias metrics across multiple dimensions:
    - **Geographic**: Urban vs Rural, Tier-1 vs Tier-2/3
    - **Income**: High-income (≥₹20L) vs Low-income (<₹15L)
    - **Credit**: Good credit (≥750) vs Fair/Poor credit (<750)
    - **Edge Cases**: Self-employed vs Salaried, Single-parent vs Nuclear
  - Metrics calculated:
    - **Approval Parity**: Ratio of approval rates between groups
    - **Interest Rate Disparity**: Absolute difference in interest rates
    - **Collateral Gap**: Absolute difference in collateral requirements
    - **Overall Fairness Score**: Weighted composite (0-100)
  - **Statistical Validation**:
    - T-test for significance testing
    - P-value calculation (< 0.05 = significant bias)
    - 95% confidence intervals
  - **Severity Classification**: CRITICAL → HIGH → MEDIUM → LOW

### ✅ Metrics Retrieval
- **Endpoint**: `GET /api/v1/metrics/`
- **Functionality**:
  - List all calculated bias metrics
  - Filter by `test_run_id` and `dimension`
  - View detailed metric data including group comparisons

---

## 5. Dashboard & Visualization

### ✅ Dashboard Page
- **Route**: `/dashboard`
- **Functionality**:
  - **KPI Cards**: Displays 4 key metrics
    - Approval Parity
    - Interest Gap
    - Collateral Gap
    - Overall Fairness Score
  - **Bias Heatmap**: Visual representation of bias severity across dimensions
  - **Top Findings**: Shows top 3 highest severity bias findings
  - **Data Upload Component**: Drag-and-drop CSV file upload
  - Real-time data fetching from backend API
  - Shows welcome message if no data available

### ✅ Bias Analysis Page
- **Route**: `/bias-analysis`
- **Functionality**:
  - **Bias Table**: Sortable table of all bias metrics
  - **Profile Comparison**: Compare profiles between groups (e.g., Urban vs Rural)
  - Filter and sort by dimension, severity, fairness score
  - Detailed view of each metric with statistical validation data

---

## 6. Human-in-the-Loop (HITL) Feedback

### ✅ Feedback Submission
- **Endpoint**: `POST /api/v1/feedback/`
- **Route**: `/feedback`
- **Functionality**:
  - Submit human expert feedback on detected bias findings
  - Fields:
    - Bias metric selection
    - Is discriminatory? (yes/no/partially)
    - Root cause analysis (text)
    - Severity rating (1-5)
    - Suggested mitigation (text)
    - Annotator information (name, role)
  - Links feedback to specific BiasMetric record

### ✅ Feedback Retrieval
- **Endpoint**: `GET /api/v1/feedback/`
- **Functionality**: List all feedback (optionally filtered by bias_metric_id)

---

## 7. Bias Mitigation

### ✅ Mitigation Cycles
- **Endpoint**: `POST /api/v1/mitigation/run`
- **Route**: `/mitigation`
- **Functionality**:
  - Iterative bias mitigation workflow
  - Uses GenAI (Gemini) to generate refined prompts based on human feedback
  - Compares before/after metrics
  - Calculates improvement percentage
  - Stores mitigation history for traceability
  - Supports multiple iterations to incrementally improve fairness

### ✅ Mitigation History
- **Endpoint**: `GET /api/v1/mitigation/history/{mitigation_run_id}`
- **Functionality**: View complete history of mitigation iterations with metrics

---

## 8. Data Management

### ✅ Database Models
- **StudentProfile**: Stores student loan profiles
- **ScoringResult**: Stores fair and biased scoring results
- **BiasMetric**: Stores calculated bias metrics per dimension
- **HumanFeedback**: Stores expert feedback on bias findings
- **MitigationResult**: Stores iterative mitigation cycle results
- **TestRun**: Tracks complete test runs (generation + scoring + metrics)

### ✅ Database Operations
- SQLAlchemy ORM for database operations
- SQLite for development (can switch to PostgreSQL)
- Automatic table creation on startup
- Session management with dependency injection

---

## 9. Utility Scripts

### ✅ Data Checking Scripts
- `check_data.py`: Quick check of database record counts
- `check_api_response.py`: Test dashboard API endpoint
- `check_test_runs.py`: List all TestRun entries
- `check_metrics_values.py`: Verify metric calculations

### ✅ Testing Scripts
- `test_backend_db.py`: Test database connectivity
- `test_gemini_integration.py`: Test GenAI API integration

### ✅ Data Setup Scripts
- `setup_showcase_data.py`: Populate database with sample data
- `populate_mock_data.py`: Generate mock data for testing
- `generate_realistic_data.py`: Generate realistic test data
- `import_government_data.py`: Import government loan data (if available)

---

## 10. Frontend Features

### ✅ Navigation & Layout
- **Sidebar Navigation**: Links to Dashboard, Bias Analysis, Feedback, Mitigation
- **Header**: Shows current page title
- **Responsive Design**: Tailwind CSS for mobile-friendly layout

### ✅ Components
- **KPICards**: Color-coded metric cards (green/yellow/red by severity)
- **BiasHeatmap**: Visual heatmap of bias across dimensions
- **TopFindings**: Card-based display of highest severity findings
- **DataUpload**: Drag-and-drop file upload with validation
- **BiasTable**: Sortable, filterable table of metrics
- **ProfileComparison**: Side-by-side comparison of profile groups

### ✅ Data Fetching
- React Query for API data fetching and caching
- Automatic background refetching
- Loading and error states
- Optimistic updates support

---

## 11. API Documentation

### ✅ Auto-Generated API Docs
- **Swagger UI**: Available at `http://localhost:8000/docs`
- **ReDoc**: Available at `http://localhost:8000/redoc`
- **OpenAPI Schema**: Automatic generation from FastAPI routes

---

## 12. Configuration & Environment

### ✅ Environment Variables
- `GEMINI_API_KEY`: Google Gemini API key for GenAI features
- `DATABASE_URL`: Database connection string (defaults to SQLite)
- `DEBUG`: Debug mode flag
- `CORS_ORIGINS`: Allowed frontend origins

### ✅ Settings Management
- Centralized configuration via Pydantic Settings
- Environment-specific overrides via `.env` file
- Type-safe configuration validation

---

## Current Limitations / Not Yet Implemented

### ⚠️ Gender Bias Dimension
- Enum exists in models but not fully implemented in metrics calculation
- Reserved for future implementation

### ⚠️ Real-time WebSocket Updates
- WebSocket endpoint exists but not fully integrated with frontend
- Dashboard currently uses polling (refresh required)

### ⚠️ Export Functionality
- No PDF/Excel export of metrics and findings
- No report generation

### ⚠️ A/B Testing Dashboard
- Cannot compare multiple test runs side-by-side
- Only shows latest test run

### ⚠️ Model Versioning
- ML model versions not tracked
- No comparison between model versions

---

## Technology Stack Summary

**Backend**:
- Python 3.11+, FastAPI, SQLAlchemy, SQLite
- Pandas, NumPy, scikit-learn, scipy
- Google Gemini AI (google-generativeai)
- uvicorn (ASGI server)

**Frontend**:
- Next.js 14, React 18, TypeScript
- Tailwind CSS, React Query, Axios
- Lucide React (icons)

---

**Last Updated**: Based on current codebase analysis



