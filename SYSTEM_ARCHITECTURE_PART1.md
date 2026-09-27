# System Architecture: Fair Lending AI Validation Platform

## Executive Summary

The **Fair Lending AI Validation Platform** is a Human-in-the-Loop (HITL) system designed to detect, analyze, and mitigate bias in education loan approval AI systems. It combines machine learning, deterministic scoring, generative AI, and statistical analysis to validate fairness across multiple dimensions.

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Architecture Layers](#architecture-layers)
3. [Core Components](#core-components)
4. [Data Flow & Workflows](#data-flow--workflows)
5. [Technology Stack](#technology-stack)
6. [Database Schema](#database-schema)
7. [API Architecture](#api-architecture) → See Part 2
8. [Frontend Architecture](#frontend-architecture) → See Part 2
9. [ML Model Training Pipeline](#ml-model-training-pipeline) → See Part 2
10. [Scoring Mechanisms](#scoring-mechanisms) → See Part 2
11. [Bias Metrics Calculation](#bias-metrics-calculation) → See Part 2
12. [GenAI Integration](#genai-integration) → See Part 2
13. [Human-in-the-Loop Workflow](#human-in-the-loop-workflow) → See Part 2
14. [Deployment Architecture](#deployment-architecture) → See Part 2

---

## 1. System Overview

### 1.1 Purpose
The system validates education loan approval AI systems for bias across five dimensions:
- **Geographic Bias**: Urban vs Rural, Tier-1 vs Tier-2/3 regions
- **Income Bias**: High-income (≥₹20L) vs Low-income (<₹15L) families
- **Credit Bias**: Good credit (≥750) vs Fair/Poor credit (<750)
- **Gender Bias**: (Reserved for future implementation)
- **Edge Cases**: Self-employed vs Salaried, Single-parent vs Nuclear families

### 1.2 Key Capabilities
1. **Synthetic Profile Generation**: Using Google Gemini AI to generate realistic Indian student loan profiles
2. **Dual Scoring System**: Fair (unbiased) vs Biased scoring comparison
3. **Statistical Bias Detection**: Comprehensive metrics with p-values, confidence intervals
4. **Human Feedback Integration**: Loan officers and consultants provide domain expertise
5. **Iterative Mitigation**: GenAI-powered prompt refinement based on feedback
6. **Real-time Dashboard**: Visualization of bias metrics and findings

---

## 2. Architecture Layers

The system follows a **3-tier architecture**:

```
┌─────────────────────────────────────────┐
│         Presentation Layer              │
│   (Next.js React Frontend + Tailwind)  │
└─────────────────────────────────────────┘
                  ↕ HTTP/REST + WebSocket
┌─────────────────────────────────────────┐
│         Application Layer               │
│   (FastAPI Backend + Services)         │
└─────────────────────────────────────────┘
                  ↕ SQLAlchemy ORM
┌─────────────────────────────────────────┐
│         Data Layer                      │
│   (SQLite Database + ML Models)        │
└─────────────────────────────────────────┘
```

### Why This Architecture?
- **Separation of Concerns**: Clear boundaries between UI, business logic, and data
- **Scalability**: Each layer can scale independently
- **Maintainability**: Changes in one layer don't affect others
- **Testability**: Each layer can be tested in isolation

---

## 3. Core Components

### 3.1 Backend Components

#### 3.1.1 FastAPI Application (`backend/app/main.py`)
**Purpose**: Main application entry point and HTTP server

**Why Used**:
- **Async Support**: Handles concurrent requests efficiently for batch processing
- **Automatic API Documentation**: OpenAPI/Swagger docs at `/docs`
- **Type Safety**: Pydantic models ensure data validation
- **WebSocket Support**: Real-time updates for dashboard metrics

**Key Responsibilities**:
- Initializes database on startup
- Configures CORS middleware for frontend communication
- Registers all API routers (profiles, scoring, metrics, feedback, mitigation, dashboard)
- Sets up WebSocket endpoint for real-time metrics updates
- Global exception handling with logging

#### 3.1.2 Database Layer (`backend/app/database.py`)
**Purpose**: SQLAlchemy ORM configuration and session management

**Why Used**:
- **SQLAlchemy ORM**: Provides abstraction over SQL, making database operations Pythonic
- **Session Management**: Dependency injection pattern for FastAPI (via `get_db()`)
- **SQLite for Development**: Zero-configuration database, easy setup
- **PostgreSQL Ready**: Can switch to PostgreSQL by changing `DATABASE_URL`

**Key Features**:
- Connection pooling for production databases
- Automatic table creation on startup
- Session lifecycle management (create on request, close on completion)

#### 3.1.3 Data Models (`backend/app/models.py`)
**Purpose**: SQLAlchemy ORM models representing database tables

**Why Used**:
- **Type Safety**: Enforces data structure at database level
- **Relationships**: Foreign keys and relationships (e.g., Profile → Scores → Metrics)
- **Enums**: Type-safe enumerations (TestDimension, ScoringType, SeverityLevel)
- **Metadata Tracking**: Created/updated timestamps for audit trails

**Core Models**:

1. **StudentProfile**: Stores synthetic or imported student loan profiles
   - **Why**: Central entity for all scoring operations
   - **Key Fields**: profile_id, financial data (income, CIBIL), academic data (GPA, course), geographic data (region, state)

2. **ScoringResult**: Stores scoring outcomes for each profile
   - **Why**: Enables comparison between fair and biased scoring
   - **Key Fields**: score (1-10), approval_decision, interest_rate, collateral_required, scoring_type (FAIR/BIASED)

3. **BiasMetric**: Stores calculated bias metrics per dimension
   - **Why**: Aggregated metrics for dashboard visualization and analysis
   - **Key Fields**: approval_parity, interest_rate_disparity, collateral_gap, fairness_score, statistical validation (p-value, t-statistic)

4. **HumanFeedback**: Stores human expert feedback on bias findings
   - **Why**: HITL validation - domain experts validate AI-detected biases
   - **Key Fields**: is_discriminatory, root_cause_analysis, suggested_mitigation, annotator info

5. **MitigationResult**: Stores results of iterative mitigation cycles
   - **Why**: Track improvements in fairness over time
   - **Key Fields**: prompt_version, before/after metrics, improvement percentages

6. **TestRun**: Groups profiles and metrics by test execution
   - **Why**: Organize multiple test runs and compare results over time

#### 3.1.4 Configuration Management (`backend/app/config.py`)
**Purpose**: Centralized configuration using Pydantic Settings

**Why Used**:
- **Environment Variables**: Secure handling of API keys and secrets
- **Type Safety**: Pydantic validates types at runtime
- **Default Values**: Sensible defaults for development
- **Environment-Specific**: Can override via `.env` file or environment variables

**Key Settings**:
- GenAI API keys (Gemini/OpenAI)
- Database URL
- CORS origins for frontend
- ML model thresholds and parameters

---

### 3.2 Service Layer Components

#### 3.2.1 ScoringService (`backend/app/services/scoring_service.py`)
**Purpose**: Orchestrates profile scoring using multiple scoring engines

**Why Used**:
- **Abstraction**: Hides complexity of choosing between ML, deterministic, or GenAI scoring
- **Batch Processing**: Handles scoring of multiple profiles efficiently
- **Fallback Logic**: Automatically falls back to deterministic scoring if ML model unavailable
- **Database Integration**: Saves results directly to database

**Scoring Strategy**:
1. **Fair Scoring**: Always uses `DeterministicScoringEngine.calculate_fair_score()` (unbiased rules)
2. **Biased Scoring**: 
   - If ML model trained: Uses `MLScoringModel.predict_score()` with bias
   - Else: Uses `DeterministicScoringEngine.calculate_biased_score()` (simulated bias)

**Why This Approach**:
- **Deterministic for Fair**: Ensures fair scoring is always consistent and explainable
- **ML for Biased**: Real-world ML models often learn biases from training data
- **Fallback**: Deterministic biased scoring simulates common biases even without ML model

#### 3.2.2 MLScoringModel (`backend/app/services/ml_scoring_model.py`)
**Purpose**: Machine learning model for loan approval prediction

**Why Used**:
- **Real-World Patterns**: Learns patterns from actual loan datasets
- **Bias Learning**: ML models often learn biases present in training data (e.g., geographic, income)
- **Flexibility**: Supports multiple algorithms (RandomForest, GradientBoosting, LogisticRegression)

**Model Architecture**:
- **Features**: GPA, CIBIL score, family income, loan amount, educational background, employment type, region, state
- **Preprocessing**: Label encoding for categoricals, StandardScaler for numeric features
- **Training**: Uses scikit-learn with train/test split
- **Bias Application**: Applies additional penalties to rural/low-income profiles post-prediction

**Why RandomForest by Default**:
- Handles non-linear relationships
- Feature importance for interpretability
- Robust to outliers
- Fast training and prediction

**Model Persistence**:
- Saved as `backend/models/scoring_model.pkl`
- Includes model, scaler, and label encoders
- Loaded on-demand (lazy loading) for performance

#### 3.2.3 DeterministicScoringEngine (`backend/app/services/deterministic_scoring.py`)
**Purpose**: Rule-based scoring that provides consistent, reproducible results

**Why Used**:
- **No API Dependency**: Works without GenAI API keys
- **Fast**: No network calls, instant results
- **Explainable**: Clear formula-based scoring logic
- **Deterministic**: Same input always produces same output
- **Baseline**: Provides ground truth for fair scoring

**Fair Scoring Formula** (Unbiased):
- **Academic Merit (40%)**: GPA normalized (0-4.0) + educational background bonus
- **Creditworthiness (30%)**: CIBIL score normalized (300-900 → 0-3.0)
- **Repayment Capacity (30%)**: Income-to-loan ratio + employment stability + co-applicant support

**Biased Scoring Formula** (Simulated Bias):
- Starts with fair score
- Applies penalties:
  - Rural regions: -2.0 points
  - Low income (<₹20L): -1.0 point
  - Self-employed: -1.5 points
  - Tier-2/3 regions: -1.0 point
  - Certain states (Bihar, UP, MP): -0.5 points
  - Single-parent/widow: -1.0 point

**Why Deterministic**:
- Enables A/B testing (fair vs biased) with controlled variables
- Provides predictable results for demonstration
- No randomness ensures consistent bias metrics

#### 3.2.4 GenAIService (`backend/app/services/genai_service.py`)
**Purpose**: Integration with Generative AI (Google Gemini) for profile generation and mitigation

**Why Used**:
- **Realistic Profile Generation**: Creates diverse, realistic Indian student profiles
- **Prompt Refinement**: Generates improved prompts for bias mitigation
- **Flexibility**: Supports both OpenAI (GPT-4) and Google Gemini

**Provider Selection Logic**:
1. Checks for `GEMINI_API_KEY` (preferred)
2. Falls back to `OPENAI_API_KEY`
3. Uses mock responses if no API key configured

**Why Gemini Preferred**:
- Better performance for structured JSON generation
- More cost-effective for batch operations
- Direct API (google-generativeai) has better SystemMessage handling than LangChain wrapper

**Key Operations**:
1. **generate_profiles()**: Batch generation of student profiles with specified dimensions
2. **score_profile()**: GenAI-based scoring (currently not primary, used for advanced scenarios)
3. **generate_mitigation_prompt()**: Creates refined prompts based on human feedback

**Retry Logic**:
- Uses `tenacity` library for exponential backoff
- Handles API rate limits gracefully
- 3 retry attempts with increasing delays

**Error Handling**:
- Falls back to mock responses if API fails
- Logs errors for debugging
- Continues processing even if individual requests fail

#### 3.2.5 MetricsService (`backend/app/services/metrics_service.py`)
**Purpose**: Calculates bias metrics and performs statistical validation

**Why Used**:
- **Quantitative Bias Detection**: Converts qualitative differences into measurable metrics
- **Statistical Rigor**: Uses scipy.stats for p-values, t-tests, confidence intervals
- **Multi-Dimensional Analysis**: Analyzes bias across geographic, income, credit, and edge case dimensions

**Metrics Calculated**:

1. **Approval Parity**: Ratio of approval rates between groups
   - Formula: `Group1_Approval_Rate / Group2_Approval_Rate`
   - Ideal: 1.0 (perfect parity)
   - Why: Measures whether one group is systematically denied loans

2. **Interest Rate Disparity**: Absolute difference in average interest rates
   - Formula: `|Group1_Avg_Interest - Group2_Avg_Interest|`
   - Ideal: 0.0 (no disparity)
   - Why: Detects if disadvantaged groups pay higher interest

3. **Collateral Gap**: Absolute difference in collateral requirement percentages
   - Formula: `|Group1_Collateral% - Group2_Collateral%|`
   - Ideal: 0.0 (no gap)
   - Why: Identifies if certain groups face higher collateral requirements

4. **Overall Fairness Score** (0-100): Weighted composite metric
   - Approval Parity component: 25%
   - Interest Gap component: 25%
   - Collateral Gap component: 20%
   - Edge Case Coverage: 20%
   - Misc: 10%
   - Why: Single number to compare fairness across test runs

**Statistical Validation**:
- **T-Test**: Compares mean scores between groups (independent samples t-test)
- **P-Value**: Probability that observed difference is due to chance
  - < 0.05: Statistically significant (likely bias)
- **Confidence Intervals**: 95% CI for difference in means
- **Why**: Ensures detected biases are statistically valid, not random noise

**Dimension-Specific Logic**:

- **Geographic**: Compares Urban vs Rural, Tier-1 vs Tier-2/3
- **Income**: Compares High-income (≥₹20L) vs Low-income (<₹15L)
- **Credit**: Compares Good credit (≥750) vs Fair/Poor credit (<750)
- **Edge Cases**: Compares Self-employed vs Salaried, Single-parent vs Nuclear

**Severity Classification**:
- **CRITICAL**: Approval parity < 0.70, Interest gap > 2.0%, Collateral gap > 30%, Fairness < 50
- **HIGH**: Approval parity < 0.85, Interest gap > 1.0%, Collateral gap > 20%, Fairness < 70
- **MEDIUM**: Approval parity < 0.95, Interest gap > 0.5%, Collateral gap > 10%, Fairness < 85
- **LOW**: All thresholds met

**Why Pandas/NumPy**:
- Efficient handling of large datasets
- Built-in statistical functions
- Easy groupby operations for dimension analysis

#### 3.2.6 CSVImportService (`backend/app/services/csv_import_service.py`)
**Purpose**: Imports student profiles from uploaded CSV files

**Why Used**:
- **Real Data Integration**: Allows uploading real-world loan datasets
- **Format Flexibility**: Handles various CSV formats with mapping functions
- **Validation**: Ensures data integrity before database insertion

**Process**:
1. Validates CSV format
2. Maps CSV columns to StudentProfile fields
3. Handles missing/null values
4. Creates TestRun entry
5. Bulk inserts profiles into database

---

### 3.3 API Route Components

#### 3.3.1 Profiles Router (`backend/app/api/routes/profiles.py`)
**Purpose**: Handles profile generation and management

**Endpoints**:
- `POST /api/v1/profiles/generate`: Generate synthetic profiles using GenAI
- `GET /api/v1/profiles/`: List all profiles (pagination)
- `GET /api/v1/profiles/{profile_id}`: Get single profile
- `POST /api/v1/profiles/upload`: Upload CSV file for import

**Why Separate Router**:
- **Modularity**: Profile operations isolated from scoring/metrics
- **RESTful Design**: Follows REST principles for resource management
- **Dependency Injection**: Database session injected via FastAPI Depends

#### 3.3.2 Scoring Router (`backend/app/api/routes/scoring.py`)
**Purpose**: Handles profile scoring operations

**Endpoints**:
- `POST /api/v1/scoring/fair`: Score profiles using fair (unbiased) model
- `POST /api/v1/scoring/biased`: Score profiles using biased model
- `GET /api/v1/scoring/results/{profile_id}`: Get scoring results for a profile

**Why Separate Endpoints**:
- **Clarity**: Explicit distinction between fair and biased scoring
- **Batch Processing**: Supports scoring multiple profiles in one request
- **Background Tasks**: Can trigger async processing for large batches

#### 3.3.3 Metrics Router (`backend/app/api/routes/metrics.py`)
**Purpose**: Calculates and retrieves bias metrics

**Endpoints**:
- `POST /api/v1/metrics/calculate`: Calculate bias metrics for a test run
- `GET /api/v1/metrics/`: List all metrics (filtered by test_run_id, dimension)

**Why POST for Calculate**:
- **State Mutation**: Creates new BiasMetric records
- **Heavy Computation**: Metrics calculation is computationally intensive
- **Explicit Trigger**: Requires explicit invocation, not automatic

#### 3.3.4 Dashboard Router (`backend/app/api/routes/dashboard.py`)
**Purpose**: Aggregates data for frontend dashboard

**Endpoints**:
- `GET /api/v1/dashboard`: Get comprehensive dashboard data (KPIs, top findings, heatmap)

**Response Structure**:
- **KPIs**: Overall fairness metrics (approval parity, interest gap, collateral gap, fairness score)
- **Top Findings**: Highest severity bias findings with details
- **Heatmap Data**: Bias metrics organized by dimension and group comparison
- **Test Run Info**: Latest test run ID and last updated timestamp

**Why Aggregated Endpoint**:
- **Performance**: Single request instead of multiple API calls
- **Consistency**: Ensures all data is from same test run
- **Caching**: Frontend can cache entire response

**Logic**:
1. Gets latest TestRun (or specified test_run_id)
2. Aggregates BiasMetrics by dimension
3. Calculates overall KPIs (weighted averages)
4. Sorts findings by severity
5. Formats heatmap data for visualization

#### 3.3.5 Feedback Router (`backend/app/api/routes/feedback.py`)
**Purpose**: Manages human-in-the-loop feedback

**Endpoints**:
- `POST /api/v1/feedback/`: Submit feedback on a bias finding
- `GET /api/v1/feedback/`: List all feedback (optionally filtered by bias_metric_id)

**Why HITL**:
- **Domain Expertise**: Loan officers understand context better than algorithms
- **Validation**: Human validation ensures false positives don't trigger unnecessary mitigation
- **Root Cause Analysis**: Humans can identify underlying causes (e.g., data quality, model design)

#### 3.3.6 Mitigation Router (`backend/app/api/routes/mitigation.py`)
**Purpose**: Handles iterative bias mitigation cycles

**Endpoints**:
- `POST /api/v1/mitigation/run`: Run mitigation cycle (GenAI prompt refinement)
- `GET /api/v1/mitigation/history/{mitigation_run_id}`: Get mitigation history
- `GET /api/v1/mitigation/`: List all mitigation runs

**Mitigation Workflow**:
1. User selects bias finding and provides human feedback
2. GenAI generates refined prompt based on feedback
3. Re-score profiles with new prompt
4. Calculate new metrics
5. Compare before/after results
6. Store MitigationResult with improvement metrics

**Why Iterative**:
- **Continuous Improvement**: Multiple cycles refine prompts incrementally
- **Learning**: Each cycle learns from previous results
- **Traceability**: Full history of changes enables rollback

---

### 3.4 Frontend Components

#### 3.4.1 Next.js Framework
**Purpose**: React-based web framework for frontend

**Why Next.js**:
- **Server-Side Rendering (SSR)**: Better SEO and initial load time
- **File-Based Routing**: Automatic routing from file structure
- **API Integration**: Built-in support for API routes (not used here, backend is separate)
- **TypeScript Support**: Type safety for React components
- **Performance**: Automatic code splitting, image optimization

#### 3.4.2 React Query (`@tanstack/react-query`)
**Purpose**: Data fetching and caching for React

**Why Used**:
- **Caching**: Reduces API calls, improves performance
- **Background Refetching**: Automatically refreshes stale data
- **Loading/Error States**: Built-in state management for async operations
- **Optimistic Updates**: Can update UI before API confirms

**Usage**:
- Dashboard data fetching
- Metrics listing
- Mitigation history queries

#### 3.4.3 Tailwind CSS
**Purpose**: Utility-first CSS framework

**Why Used**:
- **Rapid Development**: Pre-built utility classes
- **Consistency**: Design system ensures UI consistency
- **Responsive**: Built-in responsive breakpoints
- **Customization**: Easy to customize colors, spacing, etc.

#### 3.4.4 Key Frontend Components

**Dashboard Page** (`frontend/app/dashboard/page.tsx`):
- **Purpose**: Main landing page showing bias metrics
- **Features**: KPI cards, bias heatmap, top findings, data upload
- **Data Fetching**: Uses React Query to fetch from `/api/v1/dashboard`

**KPICards Component**:
- **Purpose**: Displays key metrics (approval parity, interest gap, collateral gap, fairness score)
- **Visualization**: Color-coded cards (green/yellow/red) based on severity

**BiasHeatmap Component**:
- **Purpose**: Visual heatmap of bias across dimensions
- **Visualization**: Color intensity represents severity (darker = more biased)

**TopFindings Component**:
- **Purpose**: Lists highest severity bias findings
- **Details**: Shows group comparisons, metrics, severity badges

**DataUpload Component**:
- **Purpose**: Allows uploading CSV files for profile import
- **Features**: Drag-and-drop, file validation, upload progress

**BiasAnalysis Page** (`frontend/app/bias-analysis/page.tsx`):
- **Purpose**: Detailed analysis of bias metrics
- **Features**: Sortable table, profile comparison view

**Feedback Page** (`frontend/app/feedback/page.tsx`):
- **Purpose**: Submit human feedback on bias findings
- **Features**: Form with bias metric selection, feedback text, severity rating

**Mitigation Page** (`frontend/app/mitigation/page.tsx`):
- **Purpose**: Run and view mitigation cycles
- **Features**: Mitigation form, before/after comparison table

#### 3.4.5 API Client (`frontend/lib/api-client.ts`)
**Purpose**: Axios-based HTTP client for backend communication

**Why Axios**:
- **Interceptors**: Can add auth tokens, error handling globally
- **Request/Response Transformation**: Automatic JSON parsing
- **Error Handling**: Centralized error handling logic
- **Base URL**: Configurable base URL for different environments

---

## 4. Data Flow & Workflows

### 4.1 Profile Generation & Import Workflow

```
User Action (Frontend)
    ↓
POST /api/v1/profiles/generate
    ↓
ProfilesRouter.generate_profiles()
    ↓
GenAIService.generate_profiles()
    ├─→ Format prompt with dimensions
    ├─→ Call Gemini API (or mock)
    ├─→ Parse JSON response
    └─→ Return profile list
    ↓
Create TestRun record
    ↓
For each profile:
    ├─→ Create StudentProfile record
    └─→ Save to database
    ↓
Return ProfileGenerationResponse
```

**Why This Flow**:
- **GenAI Integration**: Leverages Gemini for realistic, diverse profiles
- **Batch Processing**: Generates multiple profiles in parallel
- **Test Run Tracking**: Groups profiles by test run for organization
- **Database Persistence**: All profiles stored for future analysis

### 4.2 Scoring Workflow

```
User Action (Frontend) OR Training Script
    ↓
POST /api/v1/scoring/fair OR /scoring/biased
    ↓
ScoringRouter.score_fair() OR score_biased()
    ↓
ScoringService.score_profiles()
    ├─→ Query StudentProfiles from database
    ├─→ For each profile:
    │   ├─→ If FAIR scoring:
    │   │   └─→ DeterministicScoringEngine.calculate_fair_score()
    │   └─→ If BIASED scoring:
    │       ├─→ If ML model available:
    │       │   └─→ MLScoringModel.predict_score() with bias
    │       └─→ Else:
    │           └─→ DeterministicScoringEngine.calculate_biased_score()
    └─→ Save ScoringResult to database
    ↓
Return ScoringBatchResponse
```

**Why This Flow**:
- **Dual Scoring**: Enables comparison between fair and biased outcomes
- **Flexible Engine Selection**: Automatically chooses best available scoring method
- **Database Storage**: All scores persisted for metrics calculation
- **Batch Efficiency**: Processes multiple profiles in one request

### 4.3 Metrics Calculation Workflow

```
User Action (Frontend) OR Training Script
    ↓
POST /api/v1/metrics/calculate
    ↓
MetricsRouter.calculate_metrics()
    ↓
MetricsService.calculate_bias_metrics()
    ├─→ Load StudentProfiles
    ├─→ Load ScoringResults (fair and biased)
    ├─→ Create Pandas DataFrame
    ├─→ For each TestDimension:
    │   ├─→ Group profiles by dimension criteria
    │   ├─→ Calculate group metrics:
    │   │   ├─→ Approval parity
    │   │   ├─→ Interest rate disparity
    │   │   ├─→ Collateral gap
    │   │   └─→ Statistical tests (t-test, p-value, CI)
    │   ├─→ Calculate overall fairness score
    │   ├─→ Determine severity
    │   └─→ Create BiasMetric record
    └─→ Save all BiasMetrics to database
    ↓
Return MetricsSummaryResponse
```

**Why This Flow**:
- **Aggregated Analysis**: Analyzes all profiles together for statistical power
- **Multi-Dimensional**: Calculates metrics for each bias dimension
- **Statistical Rigor**: Includes p-values and confidence intervals
- **Severity Classification**: Categorizes findings for prioritization

### 4.4 Dashboard Data Flow

```
User Opens Dashboard (Frontend)
    ↓
GET /api/v1/dashboard
    ↓
DashboardRouter.get_dashboard()
    ├─→ Get latest TestRun
    ├─→ Query BiasMetrics for test_run_id
    ├─→ Aggregate KPIs:
    │   ├─→ Calculate weighted averages
    │   ├─→ Get worst metrics for each KPI
    │   └─→ Determine overall severity
    ├─→ Get top findings (sorted by severity)
    ├─→ Format heatmap data (by dimension → group comparison)
    └─→ Return DashboardResponse
    ↓
Frontend Renders:
    ├─→ KPICards (metrics)
    ├─→ BiasHeatmap (heatmap data)
    └─→ TopFindings (sorted findings)
```

**Why This Flow**:
- **Single Request**: All dashboard data in one API call (performance)
- **Latest Data**: Always shows most recent test run
- **Pre-aggregated**: Backend does heavy lifting, frontend just displays
- **Consistent Snapshot**: All data from same test run (no inconsistencies)

### 4.5 Human-in-the-Loop Feedback Workflow

```
User Views Bias Finding (Frontend)
    ↓
User Submits Feedback (Frontend)
    ↓
POST /api/v1/feedback/
    ↓
FeedbackRouter.submit_feedback()
    ├─→ Create HumanFeedback record
    ├─→ Link to BiasMetric
    └─→ Save to database
    ↓
User Initiates Mitigation (Frontend)
    ↓
POST /api/v1/mitigation/run
    ↓
MitigationRouter.run_mitigation()
    ├─→ Load HumanFeedback
    ├─→ GenAIService.generate_mitigation_prompt()
    │   ├─→ Format prompt with feedback
    │   ├─→ Call Gemini API
    │   └─→ Parse refined prompt
    ├─→ Store MitigationResult (before metrics)
    ├─→ Re-score profiles with new prompt (if applicable)
    ├─→ Re-calculate metrics
    ├─→ Calculate improvement percentages
    └─→ Store MitigationResult (after metrics)
    ↓
Return MitigationResponse
```

**Why This Flow**:
- **Expert Validation**: Human experts validate AI-detected biases
- **Context-Aware Mitigation**: Feedback provides context for prompt refinement
- **Iterative Improvement**: Multiple cycles refine prompts incrementally
- **Traceability**: Full history of changes enables auditing

---

## 5. Technology Stack

### 5.1 Backend Stack

| Technology | Purpose | Why Used |
|------------|---------|----------|
| **Python 3.11+** | Programming language | ML/AI ecosystem, async support, rapid development |
| **FastAPI** | Web framework | Async support, automatic API docs, type safety |
| **SQLAlchemy** | ORM | Database abstraction, relationships, migrations |
| **SQLite** | Database | Zero-config, easy setup, sufficient for MVP |
| **Pydantic** | Data validation | Type safety, settings management, request/response models |
| **Pandas** | Data manipulation | Efficient DataFrame operations, statistical functions |
| **NumPy** | Numerical computing | Array operations, statistical calculations |
| **scikit-learn** | ML library | RandomForest, preprocessing, model persistence |
| **scipy** | Scientific computing | Statistical tests (t-test, confidence intervals) |
| **google-generativeai** | Gemini API | Profile generation, prompt refinement |
| **langchain** | LLM framework | (Optional) Alternative GenAI integration |
| **uvicorn** | ASGI server | Production-ready async server for FastAPI |

### 5.2 Frontend Stack

| Technology | Purpose | Why Used |
|------------|---------|----------|
| **Next.js 14** | React framework | SSR, file-based routing, performance |
| **React 18** | UI library | Component-based, hooks, ecosystem |
| **TypeScript** | Type safety | Catch errors at compile time, better IDE support |
| **Tailwind CSS** | Styling | Utility-first, rapid development, responsive |
| **Axios** | HTTP client | Request interceptors, error handling |
| **React Query** | Data fetching | Caching, background refetching, loading states |
| **Lucide React** | Icons | Consistent icon library |

### 5.3 Development Tools

| Tool | Purpose |
|------|---------|
| **Git** | Version control |
| **.env files** | Environment variable management |
| **Virtual Environment** | Python dependency isolation |
| **npm/yarn** | Node.js package management |

---

## 6. Database Schema

### 6.1 Entity Relationship Diagram

```
StudentProfile (1) ────< (N) ScoringResult
    │
    │
    └───> (N) BiasMetric (via test_run_id)

BiasMetric (1) ────< (N) HumanFeedback

MitigationResult (N) ────> (1) TestRun
```

### 6.2 Table Details

**student_profiles**:
- Primary Key: `id` (Integer, auto-increment)
- Unique: `profile_id` (String, indexed for fast lookup)
- Indexes: `region`, `test_dimension` (for filtering)
- Relationships: One-to-many with `scoring_results`

**scoring_results**:
- Primary Key: `id`
- Foreign Key: `profile_id` → `student_profiles.id`
- Indexes: `profile_id`, `scoring_type` (for queries)
- Key Fields: `score`, `approval_decision`, `interest_rate`, `collateral_required`
- Relationships: Many-to-one with `student_profiles`

**bias_metrics**:
- Primary Key: `id`
- Indexes: `test_run_id`, `dimension`, `severity` (for filtering/sorting)
- Key Fields: `approval_parity`, `interest_rate_disparity`, `collateral_gap`, `overall_fairness_score`
- Statistical Fields: `p_value`, `t_statistic`, `confidence_interval_lower/upper`
- Relationships: One-to-many with `human_feedback`

**human_feedback**:
- Primary Key: `id`
- Foreign Key: `bias_metric_id` → `bias_metrics.id`
- Key Fields: `is_discriminatory`, `root_cause_analysis`, `suggested_mitigation`
- Relationships: Many-to-one with `bias_metrics`

**mitigation_results**:
- Primary Key: `id`
- Index: `mitigation_run_id` (for grouping iterations)
- Key Fields: 
  - `mitigation_run_id` (String, unique identifier for a mitigation cycle)
  - `iteration_number` (Integer, tracks iteration within a mitigation run)
  - `prompt_version` (String, version identifier for the prompt used)
  - `prompt_text` (Text, the actual prompt text)
  - `prompt_changes` (Text, description of changes from previous iteration)
  - Before Metrics: `before_fairness_score`, `before_approval_parity`, `before_interest_gap`, `before_collateral_gap`
  - After Metrics: `after_fairness_score`, `after_approval_parity`, `after_interest_gap`, `after_collateral_gap`
  - Improvement: `improvement_percentage`, `target_achieved` (Boolean)
  - Feedback Tracking: `feedback_ids` (JSON array of HumanFeedback IDs that influenced this iteration)
- Relationships: None (links to TestRun via test_run_id conceptually, but not enforced by FK)

**Why MitigationResult Structure**:
- **Before/After Metrics**: Enables comparison to measure improvement
- **Iteration Tracking**: Allows multiple refinement cycles within one mitigation run
- **Prompt Versioning**: Tracks which prompt version achieved which results
- **Feedback Linkage**: Links back to human feedback that triggered the mitigation
- **Improvement Metrics**: Quantifies whether mitigation was successful

**test_runs**:
- Primary Key: `id`
- Unique: `test_run_id` (String, indexed for fast lookup)
- Key Fields:
  - `test_run_id` (String, unique identifier like "TEST_20240101_120000")
  - `profile_count` (Integer, expected number of profiles)
  - `dimensions_tested` (JSON array, list of TestDimension values)
  - Status Tracking: `status` (String: pending, generating, scoring, completed, failed)
  - Progress: `progress_percentage` (Float, 0.0-100.0)
  - Results Summary: `total_profiles_generated`, `total_profiles_scored`, `total_metrics_calculated`
  - Error Handling: `error_message` (Text, nullable)
  - Timestamps: `created_at`, `completed_at` (DateTime, nullable)
- Relationships: Conceptually one-to-many with BiasMetric and MitigationResult (via test_run_id)

**Why TestRun Structure**:
- **Test Organization**: Groups all profiles, scores, and metrics from one test execution
- **Progress Tracking**: Enables monitoring of long-running test processes
- **Status Management**: Allows cancellation and error recovery
- **Audit Trail**: Timestamps enable tracking of test execution history
- **Result Aggregation**: Summary fields provide quick overview of test outcomes

**Database Design Principles**:
- **Normalization**: Separate tables for different entity types (profiles, scores, metrics)
- **Indexing**: Strategic indexes on frequently queried fields (profile_id, test_run_id, dimension, severity)
- **Audit Fields**: Created/updated timestamps on all tables for traceability
- **Flexibility**: JSON fields for extensible data (dimensions_tested, feedback_ids)
- **Referential Integrity**: Foreign keys ensure data consistency (except test_run_id which is string-based for flexibility)

---

**Continue to [Part 2: SYSTEM_ARCHITECTURE_PART2.md](./SYSTEM_ARCHITECTURE_PART2.md) for:**
- API Architecture (detailed endpoint documentation)
- Frontend Architecture (component structure and routing)
- ML Model Training Pipeline (step-by-step training process)
- Scoring Mechanisms (detailed algorithms)
- Bias Metrics Calculation (formulas and statistical methods)
- GenAI Integration (prompt engineering and API usage)
- Human-in-the-Loop Workflow (complete HITL process)
- Deployment Architecture (production setup and scaling)




