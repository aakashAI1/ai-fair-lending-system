# AI Fair Lending Validation System

A collaborative Deloitte Capstone project that explores how a human-in-the-loop workflow can test education-loan scoring systems for potential group disparities. The application compares fair and deliberately biased scoring approaches over synthetic student profiles, measures differences across selected dimensions, and supports feedback-led mitigation iterations.

## Problem

Loan scoring systems can treat applicants differently across demographic or financial groups. Teams need ways to probe such behavior, quantify observed disparities, review results, and iterate on mitigations before considering a system for real-world use.

## What the System Does

The web application generates synthetic Indian student-loan profiles, evaluates profiles using fair and biased scoring modes, calculates group-comparison metrics, and presents findings for review. Users can provide feedback and run iterative mitigation; GenAI prompt refinement is used when configured, with a deterministic fallback available.

## Key Features

- Generate up to 10,000 profiles per request, with a default of **3,100+ synthetic student profiles**.
- Compare **fair and biased scoring** outputs for the same profiles.
- Examine potential disparities across **geographic, income, gender, credit, and edge-case** dimensions.
- Calculate quantified metrics including approval parity, interest-rate disparity, collateral gap, edge-case coverage, and an overall fairness score.
- Support **human-in-the-loop validation** through findings review and feedback submission.
- Iterate on mitigation prompts, re-score profiles, and compare before-and-after metrics. GenAI integration is optional; mock responses and deterministic refinement are supported when a provider is not configured.

## Architecture

```text
Next.js web interface
       │ REST API and WebSocket
       ▼
FastAPI backend ─── SQLAlchemy ─── SQLite by default
       │
       ├── Profile generation and scoring services
       ├── Bias metrics and mitigation services
       └── Optional OpenAI or Gemini integration
```

## Tech Stack

- **Frontend:** Next.js 14, React 18, TypeScript, Tailwind CSS, TanStack Query, Axios, Recharts
- **Backend:** Python 3.11.7, FastAPI, Uvicorn, Pydantic, SQLAlchemy
- **Data and modeling:** pandas, NumPy, SciPy, scikit-learn
- **Storage:** SQLite by default; PostgreSQL configuration is also present
- **Optional GenAI:** OpenAI or Google Gemini through LangChain/provider libraries; mock behavior is available without API credentials

## Core Workflow

1. Generate synthetic student profiles or import data through the available profile workflows.
2. Score profiles in fair and biased modes.
3. Calculate and review metrics across the selected test dimensions.
4. Submit human feedback on findings.
5. Run mitigation iterations, re-score profiles, and review the metric comparison.

## Project Structure

```text
backend/
  app/api/routes/       API endpoints for profiles, scoring, metrics, feedback, and mitigation
  app/services/         Generation, scoring, metrics, and mitigation logic
  app/models.py         SQLAlchemy data models
  app/config.py         Backend configuration and environment variables
  requirements.txt      Python dependencies
frontend/
  app/                  Next.js pages and application layout
  components/           Dashboard, profile, feedback, and mitigation UI
  package.json          Frontend scripts and dependencies
data_extracted/         Included source data files
```

## Local Setup

Requirements: Python **3.11.7**, Node.js **18.17 or later** (Node 20 LTS recommended), and npm.

Install backend dependencies and start the API:

```bash
cd backend
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000 --host 127.0.0.1
```

In a second terminal, install frontend dependencies and start the web application:

```bash
cd frontend
npm ci
npm run dev
```

Open [http://localhost:3000](http://localhost:3000). The backend API is at [http://localhost:8000](http://localhost:8000), with interactive documentation at [http://localhost:8000/docs](http://localhost:8000/docs). SQLite is used by default; no separate database setup is needed for a basic local run.

## API Key Security

GenAI API keys are read from environment variables (`OPENAI_API_KEY` or `GEMINI_API_KEY`) or a local `backend/.env` file. Start from `backend/.env.example` if needed, replace placeholders locally, and never commit actual keys. The app can run without a provider key using mock responses.

## Project Context

This repository represents a **collaborative Deloitte Capstone project**. It is intended to demonstrate an approach to AI fairness validation and human review; contribution was collaborative, not solely authored by one person.

## Future Improvements

- Add broader automated coverage for API workflows, scoring comparisons, and metric calculations.
- Improve configuration and onboarding documentation for local and deployment environments.
- Expand validation datasets and evaluation approaches, with domain-expert review.
- Strengthen operational safeguards and monitoring before any real-world evaluation.

## Disclaimer

This is a capstone and validation system for demonstration and experimentation. It is **not** a real lending decision system, does not make credit decisions for actual applicants, and should not be used to approve or reject loan applications.
