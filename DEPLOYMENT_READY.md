# 🚀 Deployment Guide - Production Ready

## Quick Deploy Options

### Option 1: Railway (Backend) + Vercel (Frontend) - **RECOMMENDED** ⭐

**Time**: 10-15 minutes  
**Cost**: Free (Railway $5/month credit, Vercel Hobby plan)

#### Backend Deployment (Railway)

1. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Select your repository
   - **IMPORTANT**: Set **Root Directory** to `backend`

3. **Add PostgreSQL Database**
   - Click "+ New" → "Database" → "Add PostgreSQL"
   - Wait for it to provision
   - Copy the `DATABASE_URL` from the database service (available in Variables tab)

4. **Configure Backend Environment Variables**
   In your Railway backend service, add these variables:
   ```
   DATABASE_URL=<paste-postgres-url-from-database-service>
   SECRET_KEY=<generate-random-secret-key>
   GEMINI_API_KEY=<your-gemini-api-key-optional>
   ENVIRONMENT=production
   DEBUG=False
   CORS_ORIGINS=["https://your-frontend.vercel.app"]
   ```
   
   **To generate SECRET_KEY:**
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

5. **Deploy**
   - Railway will auto-detect Python and install dependencies
   - Deploy starts automatically
   - Wait for deployment to complete
   - Copy your backend URL (e.g., `https://your-project.up.railway.app`)

#### Frontend Deployment (Vercel)

1. **Create Vercel Account**
   - Go to [vercel.com](https://vercel.com)
   - Sign up with GitHub

2. **Import Project**
   - Click "Add New" → "Project"
   - Import your GitHub repository
   - **IMPORTANT**: Set **Root Directory** to `frontend`

3. **Configure Environment Variables**
   ```
   NEXT_PUBLIC_API_URL=<your-railway-backend-url>
   ```

4. **Deploy**
   - Click "Deploy"
   - Vercel automatically builds and deploys
   - Copy your frontend URL (e.g., `https://your-project.vercel.app`)

5. **Update Backend CORS**
   - Go back to Railway backend service
   - Update `CORS_ORIGINS` to include your Vercel URL:
     ```
     CORS_ORIGINS=["https://your-project.vercel.app"]
     ```
   - Railway will auto-redeploy

6. **Initialize Database** (Important!)
   
   **Option A: Using Railway CLI**
   ```bash
   npm i -g @railway/cli
   railway login
   railway link  # Select your Railway project
   railway run python backend/scripts/populate_mock_data.py
   railway run python backend/scripts/create_default_users.py
   ```
   
   **Option B: Using Railway Web Terminal**
   - Go to Railway dashboard → Backend service
   - Click "View Logs" → "Shell" tab
   - Run:
     ```bash
     python scripts/populate_mock_data.py
     python scripts/create_default_users.py
     ```

#### Test Deployment

1. Visit your Vercel frontend URL
2. Login with default credentials:
   - Admin: `EMP001` / `admin123`
   - Analyst: `EMP002` / `analyst123`
3. Verify:
   - ✅ Dashboard loads with metrics
   - ✅ Profile generation works
   - ✅ Bias analysis displays
   - ✅ Feedback submission works

---

### Option 2: Render (Full Stack)

**Time**: 15-20 minutes  
**Cost**: Free (with limitations)

#### Backend (Render)

1. Go to [render.com](https://render.com) → Sign up
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: fair-lending-backend
   - **Root Directory**: `backend`
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add PostgreSQL database: "New +" → "PostgreSQL"
6. Add environment variables (same as Railway)
7. Deploy

#### Frontend (Render)

1. "New +" → "Web Service"
2. Connect repository
3. Configure:
   - **Root Directory**: `frontend`
   - **Environment**: Node
   - **Build Command**: `npm install && npm run build`
   - **Start Command**: `npm start`
4. Add environment variable: `NEXT_PUBLIC_API_URL`
5. Deploy

---

### Option 3: Docker Compose (Self-Hosted)

**Time**: 10 minutes  
**Cost**: Server costs only

```bash
# Clone repository
git clone <your-repo-url>
cd hitl-ai-fair-lending-validation

# Configure environment
cd backend
cp .env.example .env
# Edit .env with your settings

# Deploy with Docker Compose
docker-compose up -d

# Initialize database
docker-compose exec backend python scripts/populate_mock_data.py
docker-compose exec backend python scripts/create_default_users.py
```

**For production**, use a reverse proxy (nginx) and HTTPS (Let's Encrypt).

---

## 🔧 Pre-Deployment Checklist

### ✅ Code Ready
- [x] All features functional
- [x] No critical bugs
- [x] Error handling in place
- [x] Environment variables documented

### ✅ Configuration
- [x] Database migrations ready
- [x] Default users can be created
- [x] Sample data population script ready
- [x] CORS properly configured

### ✅ Security
- [x] SECRET_KEY set (generate new for production)
- [x] API keys in environment variables
- [x] CORS origins restricted
- [x] DEBUG=False in production

---

## 📋 Environment Variables Reference

### Backend (Required)

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/dbname` |
| `SECRET_KEY` | JWT secret key | `your-secret-key-here` |
| `GEMINI_API_KEY` | (Optional) Gemini API key | `your-gemini-key` |
| `ENVIRONMENT` | Environment name | `production` |
| `DEBUG` | Debug mode | `False` |
| `CORS_ORIGINS` | Allowed origins (JSON array) | `["https://your-frontend.vercel.app"]` |

### Frontend (Required)

| Variable | Description | Example |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | `https://your-backend.railway.app` |

---

## 🚨 Common Deployment Issues

### Issue 1: CORS Errors
**Solution**: Make sure `CORS_ORIGINS` in backend includes your exact frontend URL (with `https://`)

### Issue 2: Database Empty
**Solution**: Run initialization scripts:
```bash
python scripts/populate_mock_data.py
python scripts/create_default_users.py
```

### Issue 3: Frontend Can't Connect to Backend
**Solution**: 
- Verify `NEXT_PUBLIC_API_URL` is correct
- Check backend is running (visit `/health` endpoint)
- Verify CORS configuration

### Issue 4: Port Issues
**Solution**: 
- Railway/Render: Use `$PORT` environment variable
- Update `uvicorn` command to use `--port $PORT` or `--port 8000`

---

## 📊 Post-Deployment Verification

1. **Health Check**
   - Visit: `https://your-backend-url/api/v1/health`
   - Should return: `{"status": "ok"}`

2. **API Docs**
   - Visit: `https://your-backend-url/api/v1/docs`
   - Should show Swagger UI

3. **Frontend**
   - Visit your frontend URL
   - Should load login page
   - Login works
   - Dashboard displays metrics

4. **Database**
   - Check if profiles exist
   - Check if metrics are calculated
   - Verify default users created

---

## 🎯 Recommended: Railway + Vercel

**Why?**
- ✅ Fastest deployment (10-15 min)
- ✅ Free tier available
- ✅ Auto-deploy from GitHub
- ✅ Easy environment variable management
- ✅ Built-in PostgreSQL
- ✅ Excellent documentation

**Quick Start Command:**
```bash
# Backend: Railway
# 1. Go to railway.app → New Project → GitHub repo → Root: backend
# 2. Add PostgreSQL → Copy DATABASE_URL
# 3. Add env vars → Deploy

# Frontend: Vercel  
# 1. Go to vercel.com → New Project → GitHub repo → Root: frontend
# 2. Add NEXT_PUBLIC_API_URL → Deploy

# Initialize DB
railway run python scripts/populate_mock_data.py
railway run python scripts/create_default_users.py
```

---

## ✅ Ready to Deploy!

Your project is **production-ready**:
- ✅ All features functional
- ✅ Error handling in place
- ✅ Security configured
- ✅ Database initialization ready
- ✅ Environment variables documented

**Next Steps:**
1. Choose deployment platform (Railway + Vercel recommended)
2. Follow the steps above
3. Initialize database
4. Test and verify

**Estimated Time**: 15-20 minutes for full deployment
