# System Architecture: Fair Lending AI Validation Platform

## Executive Summary

The **Fair Lending AI Validation Platform** is a Human-in-the-Loop (HITL) system designed to detect, analyze, and mitigate bias in education loan approval AI systems. It combines machine learning, deterministic scoring, generative AI (Google Gemini), and statistical analysis to validate fairness across multiple dimensions: Geographic, Income, Credit, and Edge Cases.

---

## 1. System Overview

### 1.1 Architecture Layers

**3-Tier Architecture:**
```
Presentation Layer (Next.js + React + Tailwind) 
    ↕ HTTP/REST + WebSocket
Application Layer (FastAPI + Services) 
    ↕ SQLAlchemy ORM
Data Layer (SQLite + ML Models)
```

**Why This Architecture?**
- Separation of concerns for maintainability
- Independent scalability per layer
- Type-safe API with automatic documentation

### 1.2 Core Workflow

1. **Profile Generation**: GenAI (Gemini) generates realistic Indian student profiles OR CSV import
2. **Dual Scoring**: Each profile scored with Fair (unbiased) and Biased models
3. **Metrics Calculation**: Statistical bias detection across dimensions with p-values
4. **Human Validation**: Domain experts provide feedback on detected biases
5. **Mitigation**: GenAI refines prompts based on feedback, iteratively improving fairness
6. **Dashboard**: Real-time visualization of metrics and findings

---

## 2. Technology Stack

### Backend
- **Python 3.11+**: ML/AI ecosystem, async support
- **FastAPI**: Async web framework, auto API docs, type safety
- **SQLAlchemy**: ORM for database abstraction
- **SQLite**: Zero-config database (PostgreSQL-ready)
- **Pandas/NumPy**: Data manipulation and statistical operations
- **scikit-learn**: ML models (RandomForest by default)
- **scipy**: Statistical tests (t-test, confidence intervals)
- **google-generativeai**: Gemini API integration
- **uvicorn**: ASGI server

### Frontend
- **Next.js 14**: React framework with SSR
- **TypeScript**: Type safety
- **Tailwind CSS**: Utility-first styling
- **React Query**: Data fetching and caching
- **Axios**: HTTP client

---

## 3. Core Components

### 3.1 Backend Services

#### ScoringService (`backend/app/services/scoring_service.py`)
**Purpose**: Orchestrates profile scoring

**Strategy**:
- **Fair Scoring**: Always uses `DeterministicScoringEngine` (unbiased rules)
- **Biased Scoring**: Uses trained `MLScoringModel` if available, else deterministic with simulated bias

**Why**: Enables controlled A/B testing (fair vs biased) with consistent results

#### MLScoringModel (`backend/app/services/ml_scoring_model.py`)
**Purpose**: Machine learning model trained on real loan datasets

**Features**:
- Algorithm: RandomForest (handles non-linearity, interpretable)
- Training: Uses `fair_lending_audit_realistic_500.csv` + `super_loan_dataset_v3_no_interview.csv`
- Bias Learning: ML models learn biases present in training data
- Persistence: Saved as `backend/models/scoring_model.pkl` (model + scaler + encoders)

**Why**: Real-world ML models often learn geographic/income biases from historical data

#### DeterministicScoringEngine (`backend/app/services/deterministic_scoring.py`)
**Purpose**: Rule-based scoring (consistent, explainable, no API dependency)

**Fair Formula** (Unbiased):
- Academic Merit (40%): GPA + educational background bonus
- Creditworthiness (30%): CIBIL score normalized (300-900 → 0-3.0)
- Repayment Capacity (30%): Income-to-loan ratio + employment stability

**Biased Formula** (Simulated):
- Starts with fair score
- Applies penalties: Rural (-2.0), Low income (-1.0), Self-employed (-1.5), Tier-2/3 (-1.0)

**Why**: Provides baseline for comparison, works without GenAI API keys

#### GenAIService (`backend/app/services/genai_service.py`)
**Purpose**: Integration with Google Gemini for profile generation and mitigation

**Operations**:
1. `generate_profiles()`: Batch generation with diversity across dimensions
2. `generate_mitigation_prompt()`: Creates refined prompts based on human feedback

**Provider Selection**: Gemini (preferred) → OpenAI → Mock

**Why Gemini**: Better JSON generation, cost-effective for batch operations

#### MetricsService (`backend/app/services/metrics_service.py`)
**Purpose**: Calculates bias metrics with statistical validation

**Metrics**:
1. **Approval Parity**: `Group1_Approval_Rate / Group2_Approval_Rate` (ideal: 1.0)
2. **Interest Rate Disparity**: `|Group1_Interest - Group2_Interest|` (ideal: 0.0)
3. **Collateral Gap**: `|Group1_Collateral% - Group2_Collateral%|` (ideal: 0.0)
4. **Fairness Score** (0-100): Weighted composite (25% approval, 25% interest, 20% collateral, 20% coverage, 10% misc)

**Statistical Validation**: T-test, p-value (< 0.05 = significant), 95% confidence intervals

**Severity**: CRITICAL → HIGH → MEDIUM → LOW (based on thresholds)

---

### 3.2 Database Schema

**Core Tables**:
- **student_profiles**: Synthetic/imported loan profiles (profile_id, financial, academic, geographic data)
- **scoring_results**: Fair and biased scores per profile (score 1-10, approval_decision, interest_rate, collateral_required)
- **bias_metrics**: Calculated metrics per dimension (approval_parity, fairness_score, p-value, t-statistic)
- **human_feedback**: Expert feedback on bias findings (is_discriminatory, root_cause_analysis, suggested_mitigation)
- **mitigation_results**: Iterative mitigation cycles (before/after metrics, improvement_percentage)
- **test_runs**: Groups profiles and metrics by test execution (test_run_id, status, progress)

**Relationships**: Profile → Scores (1:N), BiasMetric → Feedback (1:N), TestRun groups everything

---

### 3.3 API Endpoints

**Profiles** (`/api/v1/profiles`):
- `POST /generate`: Generate synthetic profiles (GenAI)
- `POST /upload`: Import CSV file
- `GET /`: List profiles (pagination)
- `GET /{profile_id}`: Get single profile

**Scoring** (`/api/v1/scoring`):
- `POST /fair`: Score profiles with fair (unbiased) model
- `POST /biased`: Score profiles with biased model
- `GET /results/{profile_id}`: Get scoring results

**Metrics** (`/api/v1/metrics`):
- `POST /calculate`: Calculate bias metrics for test run
- `GET /`: List metrics (filtered by test_run_id, dimension)

**Dashboard** (`/api/v1/dashboard`):
- `GET /`: Aggregated dashboard data (KPIs, top findings, heatmap)

**Feedback** (`/api/v1/feedback`):
- `POST /`: Submit human feedback on bias finding
- `GET /`: List feedback

**Mitigation** (`/api/v1/mitigation`):
- `POST /run`: Run mitigation cycle (GenAI prompt refinement)
- `GET /history/{mitigation_run_id}`: Get mitigation history

---

### 3.4 Frontend Components

**Pages**:
- **Dashboard** (`/dashboard`): KPI cards, bias heatmap, top findings, data upload
- **Bias Analysis** (`/bias-analysis`): Detailed metrics table, profile comparison
- **Feedback** (`/feedback`): Submit human feedback form
- **Mitigation** (`/mitigation`): Run mitigation cycles, view before/after comparisons

**Key Components**:
- **KPICards**: Displays approval parity, interest gap, collateral gap, fairness score (color-coded by severity)
- **BiasHeatmap**: Visual heatmap of bias across dimensions
- **TopFindings**: Lists highest severity findings
- **DataUpload**: CSV file upload with drag-and-drop

---

## 4. Data Flow & Workflows

### 4.1 ML Model Training Pipeline

**Script**: `backend/scripts/train_ml_model.py`

**Steps**:
1. Import datasets (`fair_lending_audit_realistic_500.csv`, `super_loan_dataset_v3_no_interview.csv`)
2. Map to `StudentProfile` format (handles different CSV schemas)
3. Store profiles in database
4. Prepare training data (features: GPA, CIBIL, income, loan amount, education, employment, region, state)
5. Train RandomForest model (target: approval_decision)
6. Score all profiles with:
   - **Fair**: Deterministic scoring (unbiased)
   - **Biased**: ML model predictions with bias penalties
7. Calculate bias metrics across all dimensions
8. Save results to database

**Why**: Trains model on real data patterns, then uses it to simulate biased scoring

### 4.2 Profile Generation Workflow

```
User Request → POST /api/v1/profiles/generate
    ↓
GenAIService.generate_profiles()
    ├─→ Format prompt with dimensions
    ├─→ Call Gemini API (batch processing)
    ├─→ Parse JSON response
    └─→ Return profile list
    ↓
Create TestRun record
    ↓
Save StudentProfile records to database
    ↓
Return response with test_run_id
```

**GenAI Prompt** (`backend/genai/prompts.py`): Instructs Gemini to generate diverse, realistic Indian student profiles across all test dimensions (geographic, income, credit, edge cases) with specific requirements for diversity and edge cases.

### 4.3 Scoring Workflow

```
POST /api/v1/scoring/fair OR /biased
    ↓
ScoringService.score_profiles()
    ├─→ Query StudentProfiles from database
    ├─→ For each profile:
    │   ├─→ FAIR: DeterministicScoringEngine.calculate_fair_score()
    │   └─→ BIASED: MLScoringModel.predict_score() (if trained) OR DeterministicScoringEngine.calculate_biased_score()
    └─→ Save ScoringResult records
    ↓
Return batch response
```

**Fair Scoring**: Formula-based, ignores geography/income/demographics

**Biased Scoring (ML)**: 
1. Predict approval probability using trained model
2. Convert to score (1-10) based on probability
3. Apply bias penalties for rural/low-income profiles
4. Determine approval_decision, interest_rate, collateral_required

### 4.4 Metrics Calculation Workflow

```
POST /api/v1/metrics/calculate
    ↓
MetricsService.calculate_bias_metrics()
    ├─→ Load StudentProfiles + ScoringResults (fair and biased)
    ├─→ Create Pandas DataFrame
    ├─→ For each TestDimension (Geographic, Income, Credit, Edge Cases):
    │   ├─→ Group profiles (e.g., Urban vs Rural)
    │   ├─→ Calculate group metrics:
    │   │   ├─→ Approval parity (ratio)
    │   │   ├─→ Interest rate disparity (absolute difference)
    │   │   ├─→ Collateral gap (absolute difference %)
    │   │   └─→ Statistical tests (t-test, p-value, 95% CI)
    │   ├─→ Calculate overall fairness score (weighted composite)
    │   ├─→ Determine severity (CRITICAL/HIGH/MEDIUM/LOW)
    │   └─→ Create BiasMetric record
    └─→ Save all BiasMetrics to database
```

**Statistical Tests**: Independent samples t-test compares mean scores between groups. P-value < 0.05 indicates statistically significant bias (not random noise).

### 4.5 Human-in-the-Loop Workflow

```
User views bias finding → Submit feedback
    ↓
POST /api/v1/feedback/
    ├─→ Create HumanFeedback record
    └─→ Link to BiasMetric
    ↓
User initiates mitigation
    ↓
POST /api/v1/mitigation/run
    ├─→ Load HumanFeedback
    ├─→ GenAIService.generate_mitigation_prompt()
    │   ├─→ Format prompt with feedback, metrics, root cause
    │   ├─→ Call Gemini API
    │   └─→ Parse refined prompt
    ├─→ Store MitigationResult (before metrics)
    ├─→ Re-score profiles (if applicable)
    ├─→ Re-calculate metrics
    ├─→ Calculate improvement percentages
    └─→ Store MitigationResult (after metrics + improvement)
```

**Mitigation Prompt** (`backend/genai/prompts.py`): Provides context about bias finding, human feedback, root cause analysis, and asks Gemini to generate improved scoring prompt that addresses the identified bias.

---

## 5. Scoring Mechanisms

### 5.1 Fair Scoring (Deterministic)

**Formula**: `Total Score = Academic Merit (40%) + Creditworthiness (30%) + Repayment Capacity (30%)`

**Components**:
- **Academic Merit**: `(GPA / 10.0) * 3.0` + educational background bonus (Engineering: +0.5, Commerce: +0.3, Science: +0.2) (Indian 10-point scale)
- **Creditworthiness**: `((CIBIL - 300) / 600) * 3.0` (normalizes 300-900 to 0-3.0)
- **Repayment Capacity**: Income-to-loan ratio scoring + employment stability bonus + co-applicant bonus

**Output Mapping**:
- Score 9-10: Approve (9% interest, no collateral)
- Score 7-8: Approve (11% interest, optional collateral)
- Score 5-6: Conditional (13% interest, collateral required)
- Score 3-4: Reject likely
- Score 1-2: Reject

**Why Deterministic**: Always produces same output for same input (reproducible, explainable, no API dependency)

### 5.2 Biased Scoring (ML Model)

**Process**:
1. **Feature Preparation**: 
   - Categorical encoding (educational_background, employment_type, region, state)
   - StandardScaler for numeric features (GPA, CIBIL, income, loan amount)
2. **Prediction**: `predict_proba()` returns approval probability (0-1)
3. **Score Conversion**: `score = 1.0 + (approval_prob * 9.0)` (maps 0-1 to 1-10)
4. **Bias Application** (if `apply_bias=True`):
   - Rural region: -2.0 points
   - Low income (<₹20L): -1.0 points
   - Tier-2/3: -1.0 points
5. **Output Mapping**: Same as fair scoring (score → approval_decision, interest_rate, collateral)

**Why ML for Bias**: Real-world ML models trained on historical data learn patterns including biases (e.g., geographic discrimination, income bias)

---

## 6. Bias Metrics Calculation

### 6.1 Dimension-Specific Grouping

**Geographic**:
- Urban (tier1) vs Rural (tier2/tier3)
- Tier-1 vs Tier-2/3

**Income**:
- High income (≥₹20L) vs Low income (<₹15L)

**Credit**:
- Good credit (≥750) vs Fair credit (650-750) vs Poor credit (<600)

**Edge Cases**:
- Self-employed vs Salaried
- Single-parent vs Nuclear family

### 6.2 Metric Formulas

**Approval Parity**: 
```
Approval_Parity = Group1_Approval_Rate / Group2_Approval_Rate
```
- Ideal: 1.0 (perfect parity)
- < 1.0: Group1 approved less than Group2 (bias against Group1)
- > 1.0: Group1 approved more than Group2 (bias against Group2)

**Interest Rate Disparity**:
```
Interest_Disparity = |Group1_Avg_Interest - Group2_Avg_Interest|
```
- Ideal: 0.0 (no disparity)

**Collateral Gap**:
```
Collateral_Gap = |Group1_Collateral% - Group2_Collateral%|
```
- Ideal: 0.0 (no gap)

**Overall Fairness Score** (0-100):
```
Fairness = (Approval_Score * 0.25) + (Interest_Score * 0.25) + 
           (Collateral_Score * 0.20) + (Coverage_Score * 0.20) + (Misc * 0.10)
```
Where each component score is normalized to 0-100 based on ideal values.

### 6.3 Statistical Validation

**T-Test**: Independent samples t-test compares mean scores between groups
```
t_statistic, p_value = scipy.stats.ttest_ind(group1_scores, group2_scores)
```

**Interpretation**:
- **p-value < 0.05**: Statistically significant (bias is real, not random)
- **p-value ≥ 0.05**: Not statistically significant (could be random variation)

**Confidence Intervals**: 95% CI for difference in means provides range estimate of bias magnitude

**Why Statistical Tests**: Ensures detected biases are statistically valid, not artifacts of small sample sizes or random noise

---

## 7. GenAI Integration

### 7.1 Profile Generation

**Prompt Template** (`backend/genai/prompts.py`):
- Instructs Gemini to generate realistic Indian student loan profiles
- Requires diversity across: geography, income, credit, education, employment, family structure
- Specifies edge cases to include (5% minimum)
- Output format: JSON array with exact schema

**Why GenAI**: Enables generation of diverse, realistic profiles without manual data collection, covers edge cases that might not exist in training data

### 7.2 Mitigation Prompt Generation

**Prompt Template**:
- Input: Bias finding description, human feedback, root cause analysis, current metrics
- Task: Generate refined scoring prompt that addresses identified bias
- Output: Improved prompt text + reasoning + expected improvements

**Why GenAI for Mitigation**: Leverages LLM understanding of fairness principles to generate nuanced prompt refinements that humans might miss

### 7.3 Error Handling

**Retry Logic**: Exponential backoff (3 attempts) via `tenacity` library
**Fallback**: Mock responses if API fails or no API key configured
**Batch Processing**: Rate limiting between batches (1 second delay)

---

## 8. Human-in-the-Loop Workflow

### 8.1 Feedback Collection

**Process**:
1. User views bias finding in dashboard/analysis page
2. Submits feedback via form:
   - Is discriminatory? (yes/no/partially)
   - Root cause analysis (text)
   - Severity rating (1-5)
   - Suggested mitigation (text)
   - Annotator info (name, role)

**Why HITL**: 
- Domain experts (loan officers) understand context better than algorithms
- Validates AI-detected biases (reduces false positives)
- Provides domain-specific insights for root cause analysis

### 8.2 Mitigation Cycle

**Iterative Process**:
1. Select bias finding with human feedback
2. GenAI generates refined prompt based on feedback
3. (Optional) Re-score profiles with new prompt
4. Re-calculate metrics
5. Compare before/after metrics
6. Calculate improvement percentage
7. Store MitigationResult with full history

**Why Iterative**: Multiple cycles allow incremental improvements, each cycle learns from previous results

**Traceability**: Full history stored (prompt versions, metrics, improvements) enables rollback and auditing

---

## 9. Deployment Architecture

### 9.1 Development Setup

**Backend**:
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

**Frontend**:
```bash
cd frontend
npm install
npm run dev  # Runs on http://localhost:3000
```

**ML Training**:
```bash
cd backend
python scripts/train_ml_model.py
```

**Environment Variables** (`backend/.env`):
```
GEMINI_API_KEY=your-key-here
DATABASE_URL=sqlite:///./fairlending.db
DEBUG=True
```

### 9.2 Production Considerations

**Database**: Switch from SQLite to PostgreSQL by changing `DATABASE_URL`

**Scaling**:
- **Backend**: Deploy FastAPI with uvicorn/gunicorn behind nginx
- **Frontend**: Next.js can be built as static site or SSR with Node.js
- **ML Models**: Store in cloud storage (S3, GCS) for distributed access

**Security**:
- API key management via environment variables (never commit to repo)
- CORS configuration restricts origins
- Rate limiting on API endpoints
- Input validation via Pydantic schemas

**Monitoring**:
- Logging: Structured logs (JSON format) for aggregation
- Metrics: Track API response times, error rates
- Alerts: Monitor ML model prediction latency

### 9.3 File Structure

```
hitl-ai-fair-lending-validation/
├── backend/
│   ├── app/
│   │   ├── api/routes/          # API endpoints
│   │   ├── services/            # Business logic (scoring, metrics, genai)
│   │   ├── models.py            # SQLAlchemy models
│   │   ├── schemas.py           # Pydantic schemas
│   │   ├── config.py            # Configuration
│   │   └── main.py              # FastAPI app
│   ├── scripts/
│   │   └── train_ml_model.py    # ML training script
│   ├── models/                  # Saved ML models
│   ├── genai/
│   │   └── prompts.py           # GenAI prompt templates
│   └── requirements.txt
├── frontend/
│   ├── app/                     # Next.js pages
│   ├── components/              # React components
│   ├── lib/                     # Utilities (api-client)
│   └── package.json
└── *.csv                        # Training datasets (root level)
```

---

## 10. Key Design Decisions

### Why Deterministic for Fair Scoring?
- Provides consistent baseline (same input → same output)
- No API dependency (works offline)
- Explainable (formula-based, not black box)

### Why ML Model for Biased Scoring?
- Simulates real-world ML models that learn biases from training data
- More realistic than simulated bias (based on actual patterns)

### Why Gemini Over OpenAI?
- Better structured JSON generation
- More cost-effective for batch operations
- Direct API handles SystemMessage better than LangChain wrapper

### Why SQLite for Development?
- Zero configuration (no separate database server)
- File-based (easy backup/restore)
- Sufficient for MVP/testing

### Why FastAPI?
- Async support for concurrent batch processing
- Automatic OpenAPI docs (Swagger UI)
- Type safety with Pydantic
- Fast performance

### Why Next.js?
- Server-side rendering (better initial load)
- File-based routing (simple structure)
- TypeScript support
- Performance optimizations (code splitting, image optimization)

---

## 11. Future Enhancements

1. **Gender Bias Dimension**: Add gender field to profiles and implement gender-based metrics
2. **Real-time WebSocket Updates**: Push metric updates to dashboard as they're calculated
3. **A/B Testing Dashboard**: Compare multiple test runs side-by-side
4. **Export Reports**: PDF/Excel export of metrics and findings
5. **Model Versioning**: Track ML model versions and their impact on bias metrics
6. **Automated Retraining**: Trigger ML model retraining when new data is imported
7. **Advanced Statistical Methods**: Add more sophisticated bias detection (e.g., demographic parity, equalized odds)

---

**End of System Architecture Documentation**




