# 🚀 Single Deployment Guide - Deploy Everything Together

There are several ways to deploy both frontend and backend together in one deployment:

---

## Option 1: Railway - Multiple Services (EASIEST) ⭐ **RECOMMENDED**

Railway allows you to deploy all services (backend, frontend, database) in **one project** with a single click.

### Steps:

1. **Go to Railway**: https://railway.app → Sign up with GitHub

2. **Create New Project**:
   - Click "New Project"
   - "Deploy from GitHub repo"
   - Select your repository

3. **Add Database** (First Service):
   - Click "+ New" → "Database" → "PostgreSQL"
   - Wait for provisioning
   - Copy `DATABASE_URL` from Variables tab

4. **Add Backend Service**:
   - Click "+ New" → "GitHub Repo" → Select same repo
   - **Set Root Directory**: `backend`
   - Add environment variables:
     ```
     DATABASE_URL=<from-database-service>
     SECRET_KEY=<generate-random-key>
     GEMINI_API_KEY=<optional>
     ENVIRONMENT=production
     DEBUG=False
     CORS_ORIGINS=["https://your-backend.up.railway.app"]
     ```
   - Deploy! Copy backend URL

5. **Add Frontend Service**:
   - Click "+ New" → "GitHub Repo" → Select same repo
   - **Set Root Directory**: `frontend`
   - Add environment variable:
     ```
     NEXT_PUBLIC_API_URL=<your-backend-url>
     ```
   - Deploy! Copy frontend URL

6. **Update CORS**:
   - Go to backend service → Variables
   - Update `CORS_ORIGINS`: `["https://your-frontend.up.railway.app"]`
   - Auto-redeploys

7. **Initialize Database**:
   - Backend service → "View Logs" → "Shell" tab
   - Run:
     ```bash
     python scripts/populate_mock_data.py
     python scripts/create_default_users.py
     ```

**✅ All services in one Railway project dashboard!**

---

## Option 2: Render - Full Stack Deployment

Similar to Railway, deploy everything in one Render project.

### Steps:

1. **Go to Render**: https://render.com → Sign up

2. **Create PostgreSQL Database**:
   - "New +" → "PostgreSQL"
   - Copy internal database URL

3. **Create Backend Web Service**:
   - "New +" → "Web Service"
   - Connect GitHub repo
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Add environment variables (same as Railway)
   - Deploy

4. **Create Frontend Web Service**:
   - "New +" → "Web Service"
   - Connect same repo
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Start Command**: `npm start`
   - Add `NEXT_PUBLIC_API_URL` environment variable
   - Deploy

**✅ All services visible in one Render dashboard!**

---

## Option 3: Serve Frontend from Backend (True Single Deployment)

Build the frontend and serve it as static files from FastAPI. **One URL, one service!**

### Implementation:

I'll create a modified backend that serves the built frontend. This allows deploying just the backend and everything works together.

**Advantages:**
- ✅ Single deployment URL
- ✅ No CORS issues
- ✅ Easier to manage
- ✅ Lower cost (one service)

**Disadvantages:**
- ⚠️ Frontend rebuilds require backend redeployment
- ⚠️ Less flexible for separate frontend updates

### Steps (I can implement this):

1. Build frontend: `cd frontend && npm run build`
2. Copy build output to backend static directory
3. Configure FastAPI to serve static files
4. Deploy only backend service

---

## Option 4: Docker Compose on Cloud Platform

Deploy entire stack using Docker Compose on platforms that support it.

### Platforms:

1. **DigitalOcean App Platform**:
   - Supports docker-compose files
   - One-click deployment
   - Auto-scaling

2. **AWS ECS/Fargate**:
   - Supports docker-compose
   - Enterprise-grade
   - More complex setup

3. **Google Cloud Run**:
   - Supports containers
   - Serverless
   - Pay-per-use

4. **Fly.io**:
   - Docker-based
   - Simple deployment
   - Global edge network

### Using Docker Compose:

The existing `backend/docker-compose.yml` can be enhanced to include frontend:

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    # ... existing config

  redis:
    image: redis:7-alpine
    # ... existing config

  backend:
    build: ./backend
    # ... existing config

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      NEXT_PUBLIC_API_URL: http://backend:8000
    depends_on:
      - backend
```

**Deploy to DigitalOcean:**
1. Create DigitalOcean account
2. Create "App Platform" project
3. Connect GitHub repo
4. Select docker-compose.yml
5. Deploy!

---

## Option 5: Single VPS Server

Deploy everything on one virtual server (DigitalOcean Droplet, AWS EC2, Linode, etc.).

### Steps:

1. **Create VPS**:
   - Choose Ubuntu 22.04
   - Minimum: 2GB RAM, 1 vCPU

2. **SSH into server**:
   ```bash
   ssh root@your-server-ip
   ```

3. **Install Docker & Docker Compose**:
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sh get-docker.sh
   apt install docker-compose -y
   ```

4. **Clone repository**:
   ```bash
   git clone https://github.com/aayusharmaaa/project-deployment.git
   cd project-deployment
   ```

5. **Create production docker-compose.yml** (I can create this)

6. **Deploy**:
   ```bash
   docker-compose up -d
   ```

7. **Setup reverse proxy (nginx)** for HTTPS:
   - Install nginx
   - Configure SSL with Let's Encrypt
   - Point domain to your server

---

## ⭐ Recommendation: **Option 1 (Railway)**

**Why Railway?**
- ✅ All services in one dashboard
- ✅ Automatic HTTPS
- ✅ Environment variables management
- ✅ Easy database setup
- ✅ Free tier available
- ✅ Auto-deploy from GitHub
- ✅ Simple and fast

**Time to deploy:** 15-20 minutes  
**Cost:** Free tier available ($5 credit/month)

---

## Quick Comparison

| Option | Complexity | Cost | Single URL | Best For |
|--------|-----------|------|-----------|----------|
| **Railway** | ⭐ Easy | Free tier | ❌ Separate URLs | **Quick deployment** |
| **Render** | ⭐ Easy | Free tier | ❌ Separate URLs | Quick deployment |
| **Frontend from Backend** | ⭐⭐ Medium | Free tier | ✅ Yes | Simple apps |
| **Docker Compose (Cloud)** | ⭐⭐⭐ Medium | $5-20/mo | ✅ Yes | Production |
| **VPS** | ⭐⭐⭐⭐ Hard | $5-10/mo | ✅ Yes | Full control |

---

## Next Steps

1. **For easiest deployment**: Use **Option 1 (Railway)** - see `DEPLOY_NOW.md`
2. **For single URL**: I can implement **Option 3** (serve frontend from backend)
3. **For production**: Use **Option 4** or **Option 5** with Docker Compose

**Would you like me to:**
- ✅ Implement Option 3 (serve frontend from backend)?
- ✅ Create production docker-compose.yml?
- ✅ Help with Railway deployment?
