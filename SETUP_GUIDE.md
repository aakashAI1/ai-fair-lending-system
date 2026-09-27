# Setup Guide - Fair Lending AI Validation MVP

## 🪟 Windows Users

**👉 See [WINDOWS_SETUP.md](WINDOWS_SETUP.md) for complete Windows setup guide**

**Quick Start on Windows:**
1. Run `setup-windows.bat` (double-click it)
2. Edit `backend\.env` and add your API key
3. Run `start-backend-windows.bat` to start backend
4. Run `start-frontend-windows.bat` to start frontend
5. Open http://localhost:3000

## 🐧 Mac/Linux Users

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 15 (or Docker) - Optional, SQLite works for demo
- Redis 5.0 (or Docker) - Optional
- OpenAI API key or Gemini API key

### Step 1: Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env and add your API keys
# OPENAI_API_KEY=your-key-here
# DATABASE_URL=postgresql://postgres:postgres@localhost:5432/fairlending
# REDIS_URL=redis://localhost:6379/0

# Start database and Redis (using Docker)
docker-compose up -d db redis

# Run migrations (tables created automatically on startup)
# Or use: alembic upgrade head

# Start backend server
uvicorn app.main:app --reload --port 8000
```

### Step 2: Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create .env.local
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Start development server
npm run dev
```

### Step 3: Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## Usage Workflow

### 1. Generate Profiles
```bash
# Using API
curl -X POST "http://localhost:8000/api/v1/profiles/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "count": 100,
    "dimensions": ["geographic", "income", "credit"],
    "batch_size": 50
  }'
```

### 2. Score Profiles
```bash
# Fair scoring
curl -X POST "http://localhost:8000/api/v1/scoring/fair" \
  -H "Content-Type: application/json" \
  -d '{
    "scoring_type": "fair",
    "batch_size": 100
  }'

# Biased scoring
curl -X POST "http://localhost:8000/api/v1/scoring/biased" \
  -H "Content-Type: application/json" \
  -d '{
    "scoring_type": "biased",
    "batch_size": 100
  }'
```

### 3. Calculate Metrics
```bash
curl -X POST "http://localhost:8000/api/v1/metrics/calculate" \
  -H "Content-Type: application/json" \
  -d '{
    "test_run_id": "TEST_xxxxxxxx",
    "dimensions": ["geographic", "income", "credit"]
  }'
```

### 4. View Dashboard
- Open http://localhost:3000/dashboard
- View KPI metrics, heatmap, and top findings

### 5. Provide Feedback
- Navigate to http://localhost:3000/feedback
- Select a bias finding
- Provide feedback with root cause analysis

### 6. Run Mitigation
- Navigate to http://localhost:3000/mitigation
- Select feedback to use
- Run mitigation cycle
- View before/after comparison

## Troubleshooting

### Backend Issues

**Database Connection Error**
```bash
# Check PostgreSQL is running
docker ps

# Check connection string in .env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/fairlending
```

**GenAI API Key Error**
```bash
# Make sure API key is set in .env
OPENAI_API_KEY=your-key-here
# Or
GEMINI_API_KEY=your-key-here
```

**Import Errors**
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Frontend Issues

**API Connection Error**
```bash
# Check .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000

# Check backend is running
curl http://localhost:8000/health
```

**Build Errors**
```bash
# Clear cache and reinstall
rm -rf node_modules .next
npm install
npm run build
```

## Docker Deployment

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

## Production Deployment

### Backend (Render/Railway)
1. Connect GitHub repository
2. Set environment variables
3. Deploy

### Frontend (Vercel)
1. Connect GitHub repository
2. Set environment variables
3. Deploy

## Testing

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

## Support

For issues or questions, please refer to:
- README.md - Main documentation
- PROJECT_SUMMARY.md - Feature overview
- API Docs - http://localhost:8000/docs

---

**Happy Coding! 🚀**







