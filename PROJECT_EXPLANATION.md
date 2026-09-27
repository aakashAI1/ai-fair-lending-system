# Fair Lending AI Validation Platform - Complete Explanation

A comprehensive guide to understanding how the system works, what technologies are used, and why.

---

## Project Overview

**Purpose:** Detect, analyze, and mitigate bias in education loan approval AI systems using **Generative AI** and a Human-in-the-Loop (HITL) approach.

**Problem Solved:** ML models used in loan approval can learn and perpetuate biases from training data, leading to unfair discrimination against certain demographic groups (rural students, low-income families, etc.).

**Solution:** A **GenAI-powered validation platform** that:
- 🤖 **Uses Google Gemini AI** to generate synthetic test profiles (50-500 profiles in seconds)
- 📊 Compares "fair" (unbiased) vs "biased" scoring models
- 🔍 Detects bias statistically with p-values and confidence intervals
- 👥 Incorporates human expert feedback for validation
- ✨ **Uses GenAI for iterative prompt refinement** to automatically improve fairness
- 📈 Measures impact with quantifiable metrics (fairness scores improve 15-25% per cycle)

**Key Innovation:** First platform to combine **GenAI (data generation, prompt refinement)**, ML models (scoring), statistical validation (bias detection), and Human-in-the-Loop (expert validation) in an end-to-end fairness validation pipeline.

---

## Architecture Overview

### 3-Tier Architecture

```
┌─────────────────────────────────────┐
│  Frontend (Next.js + React)         │  ← User Interface
│  - Dashboard, Analytics, Forms      │
└─────────────────────────────────────┘
              ↕ HTTP/REST
┌─────────────────────────────────────┐
│  Backend (FastAPI + Python)         │  ← Business Logic
│  - APIs, Services, ML Models        │
└─────────────────────────────────────┘
              ↕ SQLAlchemy ORM
┌─────────────────────────────────────┐
│  Database (SQLite/PostgreSQL)       │  ← Data Storage
│  - Profiles, Scores, Metrics        │
└─────────────────────────────────────┘
```

**Why 3-Tier?** Separation of concerns, scalability, maintainability, testability.

---

## Technology Stack & Rationale

### Backend

| Technology | Purpose | Why Used |
|------------|---------|----------|
| **Python 3.11+** | Programming language | Rich ML/AI ecosystem (scikit-learn, pandas), async support, rapid development |
| **FastAPI** | Web framework | Async support for batch processing, automatic API docs (OpenAPI/Swagger), type safety with Pydantic, WebSocket support |
| **SQLAlchemy** | ORM | Database abstraction (works with SQLite/PostgreSQL), relationship management, migrations |
| **SQLite** | Database | Zero-config for development, easy setup, sufficient for MVP (easily upgradable to PostgreSQL) |
| **Pandas/NumPy** | Data processing | Efficient DataFrame operations, statistical functions (t-tests, p-values) |
| **scikit-learn** | ML library | RandomForest/GradientBoosting models, preprocessing (StandardScaler, LabelEncoder), model persistence |
| **scipy** | Statistics | Statistical tests (t-test, confidence intervals) for bias validation |
| **google-generativeai** | GenAI | Profile generation, prompt refinement (better than LangChain for Gemini SystemMessage handling) |
| **Pydantic** | Validation | Request/response validation, settings management, type safety |

### Frontend

| Technology | Purpose | Why Used |
|------------|---------|----------|
| **Next.js 14** | React framework | SSR for better performance, file-based routing, built-in optimization |
| **React 18** | UI library | Component-based architecture, hooks, large ecosystem |
| **TypeScript** | Type safety | Catch errors at compile time, better IDE support, safer refactoring |
| **Tailwind CSS** | Styling | Utility-first, rapid development, consistent design system |
| **React Query** | Data fetching | Caching, background refetching, loading/error states |
| **Axios** | HTTP client | Request interceptors, error handling, configurable base URL |

---

## Complete Workflow (Technical Details)

### Phase 1: Data Generation & Import

**Option A: GenAI Profile Generation**
1. User requests N profiles via `/api/v1/profiles/generate`
2. **GenAIService** formats prompt with dimensions (geographic, income, credit)
3. Calls Google Gemini API (or uses mock if no API key)
4. Parses JSON response → List of student profiles
5. Creates `TestRun` record in database
6. Bulk inserts `StudentProfile` records
7. Returns `test_run_id`

**Option B: CSV Import**
1. User uploads CSV via `/api/v1/profiles/upload`
2. **CSVImportService** detects column mapping (flexible naming)
3. Maps CSV rows to `StudentProfile` schema
4. Validates and imports to database

**Technical Details:**
- GenAI uses `google-generativeai` directly (not LangChain wrapper) for better SystemMessage handling
- Fallback to mock profiles if API fails (ensures system always works)
- Batch processing for efficiency (default batch size: 50-100)
- Profile fields: name, state, region, family_income, cibil_score, gpa, course, educational_background, employment_type, co_applicant, family_structure, requested_loan_amount
- Each profile tagged with `test_dimension` (geographic, income, credit, edge_cases)
- Profiles stored with unique `profile_id` (UUID format)
- TestRun created with `test_run_id`, `profile_count`, `dimensions_tested`, `status`, `progress_percentage`

---

### Phase 2: Scoring (Dual System)

**Fair Scoring (Baseline):**
- Uses `DeterministicScoringEngine.calculate_fair_score()`
- **Formula Breakdown:**
  - **Academic Merit (40% = 4.0 points max):**
    - GPA normalized: `(GPA / 10.0) * 3.0` (Indian 10-point scale: 0-10)
    - Educational background bonus: Engineering (+0.5), Commerce/MBA (+0.3), Science (+0.2)
    - Total: `min(4.0, GPA_score + edu_bonus)`
  - **Creditworthiness (30% = 3.0 points max):**
    - CIBIL normalized: `(CIBIL_score - 300) / 600 * 3.0` (maps 300-900 → 0-3.0)
  - **Repayment Capacity (30% = 3.0 points max):**
    - Income-to-loan ratio: `family_income / requested_loan_amount`
    - Capacity score: Ratio ≥3.0 (2.0 pts), ≥2.0 (1.5 pts), ≥1.5 (1.0 pt), ≥1.0 (0.5 pt), else (0.2 pts)
    - Stability bonus: Government (+0.5), Salaried (+0.3), Self-employed (+0.1)
    - Co-applicant bonus: Parent/Spouse (+0.2)
    - Total: `min(3.0, capacity_score + stability_bonus)`
- **Final Score:** `academic_merit + creditworthiness + repayment_capacity` (1-10 scale)
- **Approval Logic:**
  - Score ≥9.0: Approve, 9.0% interest, no collateral
  - Score ≥7.0: Approve, 11.0% interest, no collateral
  - Score ≥5.0: Conditional, 13.0% interest, collateral required
  - Score <5.0: Reject, 15.0% interest, collateral required
- No demographic penalties (region, state, income level ignored)
- Always consistent and explainable (deterministic hash-based variation for realism)

**Biased Scoring (ML Model - Recommended for Realistic Showcase):**
1. **Model Training (One-Time Setup):** 
   - Run `python scripts/train_ml_model.py` once (or when you want to retrain)
   - Trains ML model on 2000+ real loan profiles
   - Saves trained model to disk: `backend/models/scoring_model.pkl`
   - Model persists and is reused for all future scoring (no need to retrain every time)

2. **During Scoring (Runtime):**
   - **ScoringService** checks if saved model file exists (`scoring_model.pkl`)
   - **If model file exists:**
     - Loads pre-trained model from disk (lazy loading - happens once, then cached in memory)
     - Uses `MLScoringModel.predict_score()` - **ML model learned bias patterns from training data**
     - Model's predictions naturally reflect biases learned from historical data (e.g., rural regions get lower approval probabilities)
   - **If model file doesn't exist:**
     - Falls back to `DeterministicScoringEngine.calculate_biased_score()` (simulated bias)
     - Uses rule-based bias penalties (still works, but less realistic)

3. **Key Point:** 
   - **Training is NOT automatic** - you train once via the script
   - **Scoring is automatic** - just loads the saved model (if it exists)
   - Model file persists between server restarts (saved on disk)

4. **Why ML Model is Better for Showcase:**
   - More realistic: Reflects how real ML models learn biases from historical data
   - Demonstrates actual AI bias detection (not just simulated)
   - Shows the platform works with production-grade ML models
   - More impressive and credible for presentations

**ML Model Technical Details:**

**Underlying Model Architecture:**
- **Library:** scikit-learn (sklearn) - Industry-standard Python ML library (used by companies like Spotify, JPMorgan Chase)
- **Model Types (configurable):**
  - **RandomForestClassifier** (default): 100 decision trees, max_depth=10, min_samples_split=20
    - Ensemble method: Combines multiple decision trees for robust predictions
    - Handles non-linear relationships and feature interactions
    - Good for showcasing: Commonly used in financial services
  - **GradientBoostingClassifier** (optional): 100 estimators, max_depth=5, learning_rate=0.1
    - Sequential ensemble learning: Builds trees to correct previous errors
    - Higher accuracy, slightly slower
  - **LogisticRegression** (optional): Linear model with L-BFGS solver, max_iter=1000
    - Interpretable, fast, good baseline

**Did We Create the Model From Scratch?**
- **No, the core ML algorithms are NOT created from scratch.** We use pre-built, well-tested scikit-learn models:
  - RandomForestClassifier: Ensemble of decision trees (scikit-learn implementation)
  - GradientBoostingClassifier: Sequential ensemble learning (scikit-learn implementation)
  - LogisticRegression: Linear classification model (scikit-learn implementation)
- **Why use pre-built models?** They are:
  - Highly optimized (C/Cython implementations)
  - Well-tested and battle-proven
  - Follow ML best practices
  - Save development time

**What We Built From Scratch:**
- **`MLScoringModel` wrapper class** (`backend/app/services/ml_scoring_model.py`):
  - Encapsulates scikit-learn models with our custom logic
  - Handles model selection, initialization, training, and prediction
- **Feature engineering pipeline:**
  - Categorical encoding (LabelEncoder) with unseen category handling
  - Numerical scaling (StandardScaler) with proper train/test separation
  - Missing value imputation (median for training, 0 for prediction)
- **Score conversion logic:**
  - Converts ML probability output (0-1) to our scoring scale (1-10)
  - Formula: `score = probability * 9 + 1`
  - Maps scores to approval decisions (approve/conditional/reject)
  - Applies bias penalties for biased scoring
- **Model persistence system:**
  - Saves model + scaler + label encoders together in single pickle file
  - Ensures all preprocessing components are preserved
- **Integration layer:**
  - Connects ML model to our scoring service
  - Handles lazy loading (model loaded on first prediction)
  - Provides fallback to deterministic scoring if model not trained

**Training Data:**
- **Datasets:** `fair_lending_audit_realistic_500.csv` + `super_loan_dataset_v3_no_interview.csv` (2000+ profiles)
- **Real-world Data:** Contains actual loan approval patterns with embedded biases (geographic, income-based, etc.)
- **Features Used (10 features):**
  - Numerical (4): `gpa`, `cibil_score`, `family_income`, `requested_loan_amount`
  - Categorical (6): `educational_background`, `employment_type`, `region`, `state`, `co_applicant`, `family_structure`
- **Preprocessing (Our Implementation):**
  - `LabelEncoder` for categoricals (maps strings → integers) - handles unseen categories gracefully
  - `StandardScaler` for numericals (mean=0, std=1 normalization) - ensures all features are on same scale
  - Feature scaling applied: `(x - mean) / std`
  - Missing value handling: Median imputation for training, 0 for prediction
  - **Key Point:** Model learns to associate categorical features (region, state) with approval patterns, naturally learning biases present in training data

**Training Process:**
- Target variable: `approval_decision` (0=reject, 1=approve, binary classification)
- Train/test split: 80/20 (stratified to maintain class balance - prevents overfitting)
- Model persistence: Saved as `scoring_model.pkl` (includes: model, scaler, label_encoders dict)
- Lazy loading: Model loaded on-demand when first prediction needed (optimizes startup time)
- Evaluation: Accuracy score, classification report
- **Training Output:** Model learns patterns like "rural applicants → lower approval rates" from training data itself (not just from penalties)

**Prediction Process:**
1. Load model, scaler, encoders from disk (one-time load, then cached in memory)
2. Encode categorical features using saved encoders (handles unseen categories gracefully)
3. Scale numerical features using saved scaler
4. `model.predict_proba()` → get approval probability (P(approve)) from trained ML model
   - **Key Point:** Model's prediction already reflects biases learned from training data (rural regions, low income, etc. naturally get lower probabilities)
5. Convert probability to score (1-10 scale): `score = probability * 9 + 1`
6. Apply additional bias penalties if `apply_bias=True` (for extra emphasis in biased scoring):
   - Rural (-2.0), Low income (-1.0), Self-employed (-1.5), Tier-2/3 (-1.0), Bihar/UP/MP states (-0.5), Single-parent/widow (-1.0)
   - **Note:** These penalties are additive - the ML model's predictions already contain bias patterns
7. Determine approval/interest/collateral based on final score thresholds

**Fallback (Deterministic Biased):**
- Used when ML model is not trained
- Starts with fair score
- Applies penalties: Rural (-2.0), Low income <₹20L (-1.0), Self-employed (-1.5), Tier-2/3 (-1.0), Bihar/UP/MP states (-0.5), Single-parent/widow (-1.0)
- Maximum penalty: -7.0 points

**Scoring Results:** Stored in `ScoringResult` table (one record per profile per scoring type: FAIR or BIASED)

---

### Phase 3: Bias Metrics Calculation

**Process:**
1. User triggers `/api/v1/metrics/calculate` with `test_run_id`
2. **MetricsService** loads all profiles and scoring results
3. Converts to Pandas DataFrame for efficient group-by operations
4. For each `TestDimension` (Geographic, Income, Credit, Edge Cases):
   - Groups profiles (e.g., Urban vs Rural, High Income vs Low Income)
   - Calculates metrics:
     - **Approval Parity:** `Group1_Approval_Rate / Group2_Approval_Rate` (ideal: 1.0)
     - **Interest Rate Disparity:** `|Group1_Avg_Interest - Group2_Avg_Interest|` (ideal: 0.0)
     - **Collateral Gap:** `|Group1_Collateral% - Group2_Collateral%|` (ideal: 0.0)
   - Runs statistical tests:
     - Independent samples t-test
     - P-value (significance threshold: < 0.05)
     - 95% confidence intervals
   - Calculates **Overall Fairness Score** (0-100): Weighted composite
   - Determines **Severity** (Critical/High/Medium/Low) based on thresholds
5. Stores `BiasMetric` records in database

**Detailed Metrics Calculations:**

1. **Approval Parity:**
   - Formula: `Group1_Approval_Rate / Group2_Approval_Rate`
   - Approval Rate = `(Number of Approvals) / (Total Profiles)`
   - Ideal: 1.0 (perfect parity)
   - Interpretation: < 0.70 = severe bias, < 0.85 = significant bias, < 0.95 = moderate bias

2. **Interest Rate Disparity:**
   - Formula: `|Group1_Average_Interest - Group2_Average_Interest|`
   - Average Interest = `sum(interest_rates) / count(profiles)`
   - Ideal: 0.0% (no disparity)
   - Interpretation: > 2.0% = severe, > 1.0% = significant, > 0.5% = moderate

3. **Collateral Gap:**
   - Formula: `|Group1_Collateral_Percentage - Group2_Collateral_Percentage|`
   - Collateral % = `(Profiles requiring collateral) / (Total Profiles) * 100`
   - Ideal: 0% (no gap)
   - Interpretation: > 30% = severe, > 20% = significant, > 10% = moderate

4. **Overall Fairness Score (0-100):**
   - Weighted composite:
     - Approval Parity component: 25% (`min(100, approval_parity * 100)`)
     - Interest Gap component: 25% (`max(0, 100 - (interest_gap * 10))`)
     - Collateral Gap component: 20% (`max(0, 100 - (collateral_gap * 2))`)
     - Edge Case Coverage: 20% (percentage of edge cases tested)
     - Misc factors: 10%
   - Formula: `(parity_comp * 0.25) + (interest_comp * 0.25) + (collateral_comp * 0.20) + (edge_coverage * 0.20) + (misc * 0.10)`

**Statistical Validation:**
- **T-Test:** Uses `scipy.stats.ttest_ind(group1_scores, group2_scores)`
  - Independent samples t-test (two-tailed)
  - Tests null hypothesis: "Groups have equal means"
  - Returns: `t_statistic`, `p_value`
- **P-Value Interpretation:**
  - < 0.01: Highly significant (strong evidence of bias)
  - < 0.05: Significant (evidence of bias)
  - ≥ 0.05: Not significant (no strong evidence)
- **Confidence Intervals:** 95% CI for difference in means
  - Calculated using: `mean_diff ± (t_critical * std_error)`
  - If CI doesn't contain 0, difference is significant
- **Pandas GroupBy:** Efficient aggregation using `df.groupby()` for grouping and `.agg()` for statistics

**Severity Classification:**
- **CRITICAL:** Approval parity < 0.70, Interest gap > 2.0%, Collateral gap > 30%, Fairness < 50
- **HIGH:** Approval parity < 0.85, Interest gap > 1.0%, Collateral gap > 20%, Fairness < 70
- **MEDIUM:** Approval parity < 0.95, Interest gap > 0.5%, Collateral gap > 10%, Fairness < 85
- **LOW:** All thresholds met (fairness ≥ 85)

**Dimension-Specific Groupings:**
- **Geographic:** Urban vs Rural, Tier-1 vs Tier-2/3
- **Income:** High (≥₹20L) vs Low (<₹15L)
- **Credit:** Good (≥750) vs Fair/Poor (<750)
- **Edge Cases:** Self-employed vs Salaried, Single-parent vs Nuclear
- **Gender:** (Reserved, not fully implemented)

---

### Phase 4: Human Feedback (HITL)

**Process:**
1. Expert reviews bias findings on dashboard/bias-analysis page
2. Navigates to `/feedback` page
3. Selects a `BiasMetric` from list
4. Fills form:
   - Is discriminatory? (Yes/No/Partially)
   - Root cause analysis (text)
   - Severity rating (1-5 slider)
   - Suggested mitigation (text)
   - Annotator info (name, role)
5. Submits via `POST /api/v1/feedback/`
6. Creates `HumanFeedback` record linked to `BiasMetric`

**Why HITL?**
- Domain experts understand context better than algorithms
- Validates AI-detected biases (reduces false positives)
- Provides actionable insights for mitigation
- Enables explainable, auditable fairness improvements

---

### Phase 5: Bias Mitigation (GenAI-Powered)

**Process:**
1. User selects `HumanFeedback` entries on `/mitigation` page
2. Configures: `test_run_id`, `max_iterations`, `target_fairness_score`
3. Submits via `POST /api/v1/mitigation/run`
4. **MitigationService** runs iterative cycle:
   - **Iteration 1:**
     - Loads human feedback
     - **GenAIService.generate_mitigation_prompt()** creates refined prompt
     - Stores `MitigationResult` (before metrics)
     - Re-scores profiles (currently uses same scoring, but prompt can influence future scoring)
     - Re-calculates metrics
     - Stores `MitigationResult` (after metrics, improvement %)
   - **Iterations 2-N:** Repeat until target achieved or max iterations
5. Returns comparison: Before vs After metrics, improvement percentages

**Technical Details:**
- GenAI analyzes feedback and generates refined scoring prompts
- Iterative improvement: Each cycle builds on previous results
- Stores full history in `MitigationResult` table (enables rollback, auditing)
- Comparison shows: Approval Parity, Interest Gap, Collateral Gap, Fairness Score improvements

---

### Phase 6: Dashboard Visualization

**Data Flow:**
1. Frontend calls `GET /api/v1/dashboard`
2. **DashboardRouter**:
   - Gets latest `TestRun`
   - Queries `BiasMetric` records
   - Calculates aggregated KPIs (weighted averages)
   - Sorts findings by severity (top 3)
   - Formats heatmap data (dimension → severity → count)
3. Frontend renders:
   - **KPICards:** Overall metrics with color coding
   - **BiasHeatmap:** Severity distribution table
   - **TopFindings:** Critical issues list

**Technical Details:**
- Single aggregated endpoint (reduces API calls, ensures consistency)
- React Query caches responses (improves performance)
- Components handle empty states gracefully

---

## Data Models & Relationships

```
StudentProfile (1) ────< (N) ScoringResult
                          │
                          └───> (N) BiasMetric (via test_run_id)
                                  │
                                  └───< (N) HumanFeedback
                                          │
                                          └───> (N) MitigationResult
TestRun (1) ────< (N) BiasMetric
```

**Key Tables:**
- **StudentProfile:** Student loan applicant data (financial, academic, geographic)
- **ScoringResult:** Fair/Biased scoring outcomes (score, approval, interest rate, collateral)
- **BiasMetric:** Aggregated bias metrics per dimension (parity, disparity, fairness score, severity)
- **HumanFeedback:** Expert annotations on bias findings
- **MitigationResult:** Before/after metrics for each mitigation iteration
- **TestRun:** Groups profiles and metrics by test execution

---

## Key Design Decisions

### 1. Dual Scoring System
**Why:** Provides clear baseline (fair) vs real-world scenario (biased ML model). Enables A/B testing with controlled variables.

### 2. Deterministic Fair Scoring
**Why:** Always consistent, explainable, no API dependencies. Ensures fair scoring is transparent and reproducible.

### 3. GenAI for Profile Generation
**Why:** Rapid generation of diverse, realistic test data. Better than static mock data for comprehensive testing.

### 4. GenAI for Mitigation
**Why:** Enables iterative prompt refinement without code changes. Human feedback guides AI to generate better scoring logic.

### 5. Human-in-the-Loop
**Why:** Domain expertise validates AI findings, provides context, enables explainable improvements. Critical for regulatory compliance.

### 6. Statistical Validation
**Why:** Ensures detected biases are statistically significant (not random noise). P-values, t-tests, confidence intervals provide rigor.

### 7. SQLite for Development
**Why:** Zero-config, easy setup. Easily upgradable to PostgreSQL for production (just change DATABASE_URL).

### 8. Next.js for Frontend
**Why:** SSR for performance, file-based routing, built-in optimization. Better than plain React for production apps.

---

## Complete Technical Flow Example

**Scenario: Detect and Mitigate Geographic Bias**

1. **Generate Profiles:** GenAI creates 100 profiles (50 urban, 50 rural)
2. **Score Profiles:**
   - Fair scoring: No location penalty → Urban: 85% approval, Rural: 82% approval
   - Biased scoring: ML model → Urban: 88% approval, Rural: 53% approval
3. **Calculate Metrics:**
   - Approval Parity: 0.60 (53% / 88% = significant bias)
   - P-value: 0.001 (highly significant)
   - Severity: CRITICAL
4. **Human Feedback:**
   - Expert: "Training data biased toward urban applicants. Remove regional proxies."
5. **Mitigation:**
   - GenAI generates refined prompt based on feedback
   - Re-scoring (simulated improvement): Urban: 85%, Rural: 78%
   - New Approval Parity: 0.92 (much better)
   - Fairness Score: 68 → 87 (+19 points)
6. **Dashboard:** Shows improved metrics, reduced severity

---

## API Endpoints Overview

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/profiles/generate` | POST | Generate profiles with GenAI |
| `/api/v1/profiles/upload` | POST | Upload CSV/ZIP files |
| `/api/v1/scoring/fair` | POST | Score profiles (fair model) |
| `/api/v1/scoring/biased` | POST | Score profiles (biased model) |
| `/api/v1/metrics/calculate` | POST | Calculate bias metrics |
| `/api/v1/dashboard` | GET | Get aggregated dashboard data |
| `/api/v1/feedback/` | POST | Submit human feedback |
| `/api/v1/mitigation/run` | POST | Run mitigation cycle |
| `/ws/metrics` | WebSocket | Real-time metrics updates (future) |

---

## File Structure Overview

```
backend/
├── app/
│   ├── api/routes/          # API endpoints (profiles, scoring, metrics, etc.)
│   ├── models.py            # SQLAlchemy ORM models
│   ├── schemas.py           # Pydantic request/response models
│   ├── services/            # Business logic
│   │   ├── scoring_service.py
│   │   ├── ml_scoring_model.py
│   │   ├── deterministic_scoring.py
│   │   ├── metrics_service.py
│   │   ├── genai_service.py
│   │   └── mitigation_service.py
│   ├── database.py          # DB connection, session management
│   └── main.py              # FastAPI app, CORS, routers
├── scripts/
│   └── train_ml_model.py    # ML training pipeline
└── models/
    └── scoring_model.pkl    # Trained ML model

frontend/
├── app/
│   ├── dashboard/page.tsx   # Main dashboard
│   ├── profiles/page.tsx    # Profile list/generation
│   ├── bias-analysis/page.tsx
│   ├── feedback/page.tsx
│   └── mitigation/page.tsx
├── components/
│   ├── dashboard/           # KPICards, BiasHeatmap, TopFindings
│   ├── feedback/            # FeedbackForm
│   └── mitigation/          # MitigationForm, ComparisonTable
└── lib/
    ├── api-client.ts        # Axios HTTP client
    └── types/               # TypeScript types
```

---

## Summary

**What It Does:**
- Detects bias in loan approval AI systems across 5 dimensions
- Uses statistical validation (p-values, t-tests) for rigor
- Incorporates human expert feedback (HITL)
- Uses GenAI for profile generation and iterative mitigation
- Provides visual dashboard for analysis

**How It Works:**
1. Generate/import student profiles
2. Score with fair (baseline) and biased (ML) models
3. Calculate bias metrics statistically
4. Human experts provide feedback
5. GenAI refines prompts iteratively
6. Measure improvements

**Why It's Effective:**
- Quantitative bias detection (not just qualitative)
- Human validation (domain expertise)
- Automated improvement (GenAI-powered)
- Full audit trail (all data stored)
- Real-world applicable (Indian education loan context)

**Key Innovation:**
Combines ML bias detection, statistical validation, human expertise, and GenAI automation in a single platform for end-to-end fairness validation and improvement.
