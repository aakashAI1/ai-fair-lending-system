# Quick Start Guide

## Windows Users 🪟

**Quick Setup:**
1. Run `setup-windows.bat` (double-click or run in Command Prompt)
2. Edit `backend\.env` and add your Gemini API key
3. Double-click `start-backend-windows.bat` to start backend
4. Double-click `start-frontend-windows.bat` to start frontend (in a new window)
5. Open http://localhost:3000

**Manual Setup:**
```cmd
REM Backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000

REM Frontend (new terminal)
cd frontend
npm install
npm run dev
```

See [WINDOWS_SETUP.md](WINDOWS_SETUP.md) for detailed Windows instructions.

## Mac/Linux Users 🐧

### 1. Start Backend Server
```bash
cd backend
python3 -m uvicorn app.main:app --reload --port 8000 --host 127.0.0.1
```

### 2. Start Frontend Server (in a new terminal)
```bash
cd frontend
npm run dev
```

### 3. Access the Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Configuring API Keys

### Option 1: Create .env file (Recommended)
```bash
cd backend
cp .env.example .env
```

Then edit `.env` and add your API keys:
```env
OPENAI_API_KEY=your-actual-openai-api-key-here
# OR
GEMINI_API_KEY=your-actual-gemini-api-key-here
```

### Option 2: Set Environment Variables
```bash
export OPENAI_API_KEY=your-actual-openai-api-key-here
# OR
export GEMINI_API_KEY=your-actual-gemini-api-key-here
```

## Installing GenAI Dependencies (if using real API)

If you want to use real GenAI instead of mock responses:

```bash
cd backend
pip install langchain langchain-openai openai
# OR for Gemini
pip install langchain langchain-google-genai google-generativeai
```

## Current Status

- ✅ Backend: Fixed and ready
- ✅ Frontend: Fixed and ready
- ✅ Database: SQLite (no setup needed)
- ⚠️ GenAI: Currently using mock responses (will use real API when keys are added)

## Testing the Application

### Generate Test Data
```bash
curl -X POST "http://localhost:8000/api/v1/profiles/generate" \
  -H "Content-Type: application/json" \
  -d '{"count": 10, "dimensions": ["geographic", "income"], "batch_size": 10}'
```

### Score Profiles
```bash
curl -X POST "http://localhost:8000/api/v1/scoring/fair" \
  -H "Content-Type: application/json" \
  -d '{"scoring_type": "fair", "batch_size": 10}'
```

## Notes

- The application currently works with mock data (no API keys needed)
- When you add API keys, the app will automatically switch to using real GenAI
- Database is SQLite (fairlending.db) - no PostgreSQL setup needed
- All endpoints return empty data gracefully when no test data exists







