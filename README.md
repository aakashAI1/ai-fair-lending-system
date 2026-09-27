# Fair Lending AI Validation Workbench

**GenAI-Powered Human-in-the-Loop Testing for Bias Detection & Mitigation in Education Loan Approvals**

## 📌 Project Overview

This MVP provides a comprehensive validation platform for detecting and mitigating bias in education loan approval AI systems. The platform uses Generative AI to:

- Generate 3,100+ realistic, diverse synthetic student profiles
- Score each profile using both fair and biased models
- Detect bias patterns across 5 dimensions (geographic, income, gender, credit, edge cases)
- Validate findings with human domain experts
- Mitigate bias through iterative GenAI prompt improvements
- Prove fairness improvements with quantified metrics

## 🎯 Key Features

### 1. Synthetic Profile Generation
- GenAI generates realistic Indian student loan profiles
- Geographic diversity (urban Tier-1, rural Tier-2/3)
- Income distribution (₹8L-₹50L)
- CIBIL scores (300-900)
- Educational backgrounds (Engineering, Commerce, Science)
- Edge cases (first-time borrowers, self-employed, widow, etc.)

### 2. Dual-Mode Scoring
- **Fair Scoring**: Evaluates based on academic merit, creditworthiness, and repayment capacity only
- **Biased Scoring**: Simulates unconscious bias (rural penalty, income discrimination, etc.)

### 3. 5-Dimensional Bias Detection
- **Geographic Bias**: Urban vs. Rural, Tier-1 vs. Tier-2/3
- **Income Bias**: High income vs. Low income approval gaps
- **Gender & Co-applicant Bias**: Male vs. Female, different co-applicant requirements
- **Credit Score Logic Bias**: Good credit vs. Fair/Poor credit treatment
- **Robustness & Edge Cases**: Self-employed, government employees, border regions, etc.

### 4. Quantified Bias Metrics
- Approval Rate Parity (target ≥0.95)
- Interest Rate Disparity (target <0.5%)
- Collateral Requirement Gap (target <10%)
- Edge Case Coverage (target ≥95%)
- Overall Fairness Score (target ≥85/100)

### 5. Human-in-the-Loop Validation
- Dashboard with KPI cards, heatmap, and top findings
- Detailed bias analysis with filterable table
- Human feedback form for annotations
- Mitigation page with before/after comparison

### 6. Agentic Mitigation Loop
- GenAI reads human feedback and refines prompts
- Re-scores all profiles with improved prompt
- Recalculates metrics and validates improvement
- Iterative process until target fairness is achieved

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│   FRONTEND (Next.js 14 + React)    │
│   - Dashboard, Bias Analysis,      │
│     Feedback, Mitigation           │
└─────────────────────────────────────┘
            ↓ REST API + WebSocket
┌─────────────────────────────────────┐
│   BACKEND (FastAPI + Python)       │
│   - Profile Generation             │
│   - Scoring (Fair/Biased)          │
│   - Metrics Calculation            │
│   - Mitigation Loop                │
└─────────────────────────────────────┘
    ↓           ↓           ↓
┌─────────┐ ┌────────┐ ┌──────────┐
│ GenAI   │ │Database│ │  Cache   │
│(Gemini) │ │(SQLite/PostgreSQL)│ │ (Redis) │
└─────────┘ └────────┘ └──────────┘
```

## 📁 Project Structure

```
fair-lending-validation/
│
├── backend/                          # FastAPI Backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                  # FastAPI app entry point
│   │   ├── config.py                # Configuration & settings
│   │   ├── database.py              # Database connection & session
│   │   ├── models.py                # SQLAlchemy ORM models
│   │   ├── schemas.py               # Pydantic request/response schemas
│   │   │
│   │   ├── api/                     # API routes
│   │   │   ├── deps.py              # Dependency injection (DB sessions)
│   │   │   └── routes/
│   │   │       ├── dashboard.py     # Dashboard data endpoint
│   │   │       ├── feedback.py      # Human feedback endpoints
│   │   │       ├── metrics.py       # Bias metrics calculation
│   │   │       ├── mitigation.py    # Mitigation loop endpoints
│   │   │       ├── profiles.py      # Profile generation & upload
│   │   │       └── scoring.py       # Fair/biased scoring endpoints
│   │   │
│   │   ├── services/                # Business logic layer
│   │   │   ├── file_upload_service.py    # ZIP upload & Prolog parsing
│   │   │   ├── genai_service.py          # GenAI integration (OpenAI/Gemini)
│   │   │   ├── metrics_service.py        # Bias metrics calculation
│   │   │   ├── mitigation_service.py     # Mitigation loop logic
│   │   │   └── scoring_service.py        # Profile scoring logic
│   │   │
│   │   └── websocket/               # WebSocket handlers
│   │       ├── handlers.py          # WebSocket event handlers
│   │       └── manager.py           # Connection management
│   │
│   ├── genai/                       # GenAI prompts & templates
│   │   └── prompts.py               # Prompt templates for profile generation
│   │
│   ├── scripts/                     # Utility scripts
│   │   ├── import_government_data.py    # Import Prolog data files
│   │   └── populate_mock_data.py        # Populate database with mock data
│   │
│   ├── tests/                       # Backend tests
│   │   ├── conftest.py              # Pytest fixtures
│   │   └── test_genai.py            # GenAI service tests
│   │
│   ├── uploads/                     # Uploaded ZIP files (temporary)
│   ├── requirements.txt             # Python dependencies
│   ├── Dockerfile                   # Docker image for backend
│   └── docker-compose.yml           # Docker Compose config
│
├── frontend/                        # Next.js Frontend
│   ├── app/                         # Next.js 14 App Router
│   │   ├── layout.tsx               # Root layout with providers
│   │   ├── page.tsx                 # Home page
│   │   ├── globals.css              # Global styles
│   │   ├── providers.tsx            # React Query & context providers
│   │   │
│   │   ├── dashboard/               # Dashboard page
│   │   │   └── page.tsx             # Main dashboard with KPIs
│   │   │
│   │   ├── bias-analysis/           # Bias analysis page
│   │   │   └── page.tsx             # Filterable bias findings table
│   │   │
│   │   ├── feedback/                # Feedback page
│   │   │   └── page.tsx             # Human feedback form
│   │   │
│   │   └── mitigation/              # Mitigation page
│   │       └── page.tsx             # Before/after comparison
│   │
│   ├── components/                  # React components
│   │   ├── layout/
│   │   │   ├── Header.tsx           # Top navigation header
│   │   │   └── Sidebar.tsx          # Side navigation menu
│   │   │
│   │   ├── dashboard/
│   │   │   ├── DataUpload.tsx       # Drag-and-drop file upload
│   │   │   ├── KPICards.tsx         # KPI metrics cards
│   │   │   ├── BiasHeatmap.tsx      # Bias heatmap visualization
│   │   │   └── TopFindings.tsx      # Top bias findings list
│   │   │
│   │   ├── bias-analysis/
│   │   │   ├── BiasTable.tsx        # Filterable bias findings table
│   │   │   └── ProfileComparison.tsx # Profile detail comparison
│   │   │
│   │   ├── feedback/
│   │   │   └── FeedbackForm.tsx     # Human feedback form component
│   │   │
│   │   ├── mitigation/
│   │   │   ├── MitigationForm.tsx   # Mitigation run form
│   │   │   └── ComparisonTable.tsx  # Before/after metrics comparison
│   │   │
│   │   └── ui/                      # Reusable UI components
│   │       └── card.tsx             # Card component (shadcn/ui style)
│   │
│   ├── lib/                         # Utility libraries
│   │   ├── api-client.ts            # Axios client & API helpers
│   │   ├── utils.ts                 # Utility functions (cn, formatting)
│   │   ├── hooks/
│   │   │   └── useMetrics.ts        # React hook for metrics data
│   │   └── types/
│   │       └── metrics.ts           # TypeScript type definitions
│   │
│   ├── package.json                 # Node.js dependencies
│   ├── tsconfig.json                # TypeScript configuration
│   ├── tailwind.config.ts           # Tailwind CSS configuration
│   ├── next.config.js               # Next.js configuration
│   └── postcss.config.js            # PostCSS configuration
│
├── data_extracted/                  # Extracted government data (Prolog files)
│   ├── student-loan.names          # Student names mapping
│   ├── enrolled.pl                  # Enrollment data
│   ├── male.pl                      # Gender data
│   └── ...                          # Other Prolog fact files
│
├── .gitignore                       # Git ignore rules
├── README.md                        # This file
├── WINDOWS_COMPLETE_GUIDE.md        # Windows setup guide
├── FRONTEND_FIX.md                  # Frontend troubleshooting guide
├── WINDOWS_PYTHON312_FIX.md         # Python 3.12 compatibility fix
│
├── setup-windows.bat               # Windows setup script
├── setup-windows.ps1               # Windows PowerShell setup script
├── setup.sh                        # Mac/Linux setup script
├── start-backend-windows.bat        # Windows backend start script
├── start-frontend-windows.bat       # Windows frontend start script
├── start-backend.sh                 # Mac/Linux backend start script
└── start-frontend.sh                # Mac/Linux frontend start script
```

### Key Files Explained

#### Backend Core Files
- **`app/main.py`**: FastAPI application entry point, route registration, CORS setup
- **`app/models.py`**: SQLAlchemy ORM models (StudentProfile, BiasMetric, TestRun, etc.)
- **`app/schemas.py`**: Pydantic schemas for request/response validation
- **`app/config.py`**: Environment variables, API keys, database URLs
- **`app/database.py`**: Database session factory and connection management

#### Backend Services
- **`services/genai_service.py`**: Handles OpenAI/Gemini API calls for profile generation
- **`services/scoring_service.py`**: Implements fair and biased scoring logic
- **`services/metrics_service.py`**: Calculates bias metrics (approval parity, interest gap, etc.)
- **`services/mitigation_service.py`**: Implements the HITL mitigation loop
- **`services/file_upload_service.py`**: Processes ZIP uploads and imports Prolog data

#### Frontend Core Files
- **`app/layout.tsx`**: Root layout with React Query provider and global styles
- **`app/providers.tsx`**: React Query configuration and context providers
- **`lib/api-client.ts`**: Axios instance with base URL and interceptors
- **`lib/utils.ts`**: Utility functions (class name merging, number formatting)

#### Frontend Components
- **`components/dashboard/`**: Dashboard visualization components
- **`components/bias-analysis/`**: Bias findings table and profile comparison
- **`components/feedback/`**: Human feedback collection form
- **`components/mitigation/`**: Mitigation run form and comparison view

## 💻 Tech Stack

### Backend
- **FastAPI** 0.104 - Web framework
- **Python** 3.11 - Runtime
- **SQLAlchemy** 2.0 - ORM
- **LangChain** 0.0.350 - GenAI orchestration
- **OpenAI/Gemini** - GenAI models
- **PostgreSQL** 15 - Database
- **Redis** 5.0 - Caching
- **Celery** 5.3 - Async tasks

### Frontend
- **Next.js** 14 - React framework
- **TypeScript** 5.3 - Type safety
- **Tailwind CSS** 3.3 - Styling
- **Recharts** 2.10 - Charts
- **React Hook Form** 7.48 - Forms
- **TanStack Query** 5.25 - Server state

## ⚡ Quick Start

**Just want to run it?** See [QUICK_RUN_GUIDE.md](QUICK_RUN_GUIDE.md) - 3 simple steps!

**Need to push changes?** See [GITHUB_PUSH_GUIDE.md](GITHUB_PUSH_GUIDE.md) - Simple workflow!

## 🚀 Getting Started

### Cross-Platform Support ✅

This project works seamlessly on **Windows**, **Mac**, and **Linux**. See [CROSS_PLATFORM_SETUP.md](CROSS_PLATFORM_SETUP.md) for details.

### Windows Users 🪟
👉 **📖 [Complete Step-by-Step Guide](WINDOWS_COMPLETE_GUIDE.md) - From GitHub download to running the app**

**Quick start on Windows:**
1. Install Python 3.11+ and Node.js 18+ (see guide for details)
2. Clone this repository: `git clone https://github.com/aayusharmaaa/hitl-project-testing.git`
3. Run `setup-windows.bat` to install everything (automatically populates sample data!)
4. Edit `backend\.env` and add your Gemini API key (optional - only for GenAI features)
5. Double-click `start-backend-windows.bat` to start backend
6. Double-click `start-frontend-windows.bat` to start frontend (new window)
7. Open http://localhost:3000/dashboard (you'll see sample metrics!)

**For detailed instructions:** See [WINDOWS_COMPLETE_GUIDE.md](WINDOWS_COMPLETE_GUIDE.md) - Complete step-by-step guide from downloading to running

### Mac/Linux Users 🍎🐧

**Quick start on Mac/Linux:**
1. Install Python 3.11+ and Node.js 18+
2. Clone this repository: `git clone https://github.com/aayusharmaaa/hitl-project-testing.git`
3. Make scripts executable: `chmod +x setup.sh start-backend.sh start-frontend.sh`
4. Run `./setup.sh` to install everything (automatically populates sample data!)
5. Edit `backend/.env` and add your Gemini API key (optional - only for GenAI features)
6. Run `./start-backend.sh` to start backend (in one terminal)
7. Run `./start-frontend.sh` to start frontend (in another terminal)
8. Open http://localhost:3000/dashboard (you'll see sample metrics!)

**For cross-platform compatibility:** See [CROSS_PLATFORM_SETUP.md](CROSS_PLATFORM_SETUP.md)

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 15
- Redis 5.0
- OpenAI API key or Gemini API key

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

5. **Set up database**
   ```bash
   # Start PostgreSQL and Redis (using Docker)
   docker-compose up -d db redis
   
   # Or use local PostgreSQL/Redis
   # Update DATABASE_URL and REDIS_URL in .env
   ```

6. **Run database migrations**
   ```bash
   # The app will create tables automatically on startup
   # Or use Alembic for migrations
   ```

7. **Start backend server**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   ```bash
   # Create .env.local
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

4. **Start development server**
   ```bash
   npm run dev
   ```

5. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## 📖 Usage Guide

### 1. Generate Profiles
- Use the API endpoint: `POST /api/v1/profiles/generate`
- Specify count, dimensions, and batch size
- Profiles are generated using GenAI and saved to database

### 2. Score Profiles
- Score with fair model: `POST /api/v1/scoring/fair`
- Score with biased model: `POST /api/v1/scoring/biased`
- Results are stored in database

### 3. Calculate Metrics
- Calculate bias metrics: `POST /api/v1/metrics/calculate`
- Metrics are calculated for all dimensions
- Results include statistical validation

### 4. Provide Feedback
- Use the Feedback page in the UI
- Select a bias finding and provide annotations
- Submit feedback with root cause analysis and suggestions

### 5. Run Mitigation
- Use the Mitigation page in the UI
- Select feedback to use for improvement
- Run mitigation cycle to refine prompts
- View before/after comparison

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📊 API Endpoints

### Profiles
- `POST /api/v1/profiles/generate` - Generate synthetic profiles
- `GET /api/v1/profiles/` - List profiles
- `GET /api/v1/profiles/{profile_id}` - Get profile

### Scoring
- `POST /api/v1/scoring/fair` - Score with fair model
- `POST /api/v1/scoring/biased` - Score with biased model
- `GET /api/v1/scoring/results` - Get scoring results
- `GET /api/v1/scoring/comparison/{profile_id}` - Get profile comparison

### Metrics
- `POST /api/v1/metrics/calculate` - Calculate bias metrics
- `GET /api/v1/metrics/{test_run_id}` - Get metrics for test run
- `GET /api/v1/metrics/` - List all metrics

### Feedback
- `POST /api/v1/feedback/` - Submit feedback
- `GET /api/v1/feedback/` - List feedback
- `GET /api/v1/feedback/{feedback_id}` - Get feedback

### Mitigation
- `POST /api/v1/mitigation/run` - Run mitigation cycle
- `GET /api/v1/mitigation/history/{mitigation_run_id}` - Get mitigation history
- `GET /api/v1/mitigation/` - List mitigations

### Dashboard
- `GET /api/v1/dashboard/` - Get dashboard data

## 🐳 Docker Deployment

### Backend
```bash
cd backend
docker-compose up -d
```

### Frontend
```bash
cd frontend
docker build -t fair-lending-frontend .
docker run -p 3000:3000 fair-lending-frontend
```

## 📝 Configuration

### Environment Variables

#### Backend (.env)
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `OPENAI_API_KEY` - OpenAI API key
- `GEMINI_API_KEY` - Gemini API key (alternative)
- `SECRET_KEY` - Secret key for security
- `CORS_ORIGINS` - CORS allowed origins (JSON array)

#### Frontend (.env.local)
- `NEXT_PUBLIC_API_URL` - Backend API URL

## 🔒 Security

- API keys stored in environment variables
- Input validation using Pydantic schemas
- CORS configured for allowed origins
- Database connection pooling
- Error handling and logging

## 📈 Monitoring

- Logging with structured logs
- Error tracking (Sentry integration ready)
- WebSocket for real-time updates
- Health check endpoint: `GET /health`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is part of a Deloitte capstone project.

## 👥 Authors

Built for Deloitte Capstone Project - GenAI-Powered Fairness Validation

## 🙏 Acknowledgments

- Deloitte for project guidance
- OpenAI for GPT-4 API
- Google for Gemini API
- FastAPI and Next.js communities

## 📞 Support

For issues and questions, please open an issue on GitHub.

## 🚀 Future Enhancements

- [ ] Real-time WebSocket updates for scoring progress
- [ ] Export functionality (CSV, PDF)
- [ ] Advanced visualization with Recharts
- [ ] Multi-user support with authentication
- [ ] Prompt versioning and history
- [ ] A/B testing for prompt variations
- [ ] Integration with actual loan approval systems
- [ ] Advanced statistical analysis
- [ ] Machine learning model integration
- [ ] Automated report generation

---

**Note**: This is an MVP for demonstration purposes. For production use, additional security, scalability, and compliance measures should be implemented.







