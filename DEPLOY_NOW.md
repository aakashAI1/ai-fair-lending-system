# 🚀 Deploy Right Now - Step by Step

## Quick Deploy in 10 Minutes

### Step 1: Deploy Backend (Railway)

1. **Go to Railway**: https://railway.app
   - Sign up with GitHub (free)

2. **New Project**:
   - Click "New Project"
   - "Deploy from GitHub repo"
   - Select your repository
   - **Set Root Directory**: `backend` ⚠️ IMPORTANT

3. **Add PostgreSQL Database**:
   - Click "+ New" → "Database" → "PostgreSQL"
   - Wait 30 seconds for it to provision
   - Copy the `DATABASE_URL` (click on database → Variables tab)

4. **Configure Environment Variables** (Backend service):
   
   Click on your backend service → Variables tab → Add these:
   
   ```
   DATABASE_URL=<paste-postgres-url-here>
   SECRET_KEY=<generate-with-command-below>
   GEMINI_API_KEY=<your-key-optional>
   ENVIRONMENT=production
   DEBUG=False
   CORS_ORIGINS=["https://your-frontend.vercel.app"]
   ```
   
   **Generate SECRET_KEY**:
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

5. **Wait for Deployment**:
   - Railway auto-deploys when you save environment variables
   - Wait 2-3 minutes for build to complete
   - Copy your backend URL (e.g., `https://your-project.up.railway.app`)

### Step 2: Deploy Frontend (Vercel)

1. **Go to Vercel**: https://vercel.com
   - Sign up with GitHub (free)

2. **Import Project**:
   - "Add New" → "Project"
   - Import your GitHub repository
   - **Set Root Directory**: `frontend` ⚠️ IMPORTANT

3. **Environment Variable**:
   ```
   NEXT_PUBLIC_API_URL=<your-railway-backend-url>
   ```
   (e.g., `https://your-project.up.railway.app`)

4. **Deploy**:
   - Click "Deploy"
   - Wait 2-3 minutes
   - Copy your frontend URL (e.g., `https://your-project.vercel.app`)

### Step 3: Update CORS

1. **Go back to Railway** → Backend service → Variables
2. **Update CORS_ORIGINS**:
   ```
   CORS_ORIGINS=["https://your-project.vercel.app"]
   ```
   (Replace with your actual Vercel URL)
3. **Save** - Railway auto-redeploys

### Step 4: Initialize Database

**Using Railway Web Terminal:**

1. Go to Railway → Backend service → "Deployments" tab
2. Click latest deployment → "View Logs"
3. Click "Shell" tab (top right)
4. Run:
   ```bash
   python scripts/populate_mock_data.py
   python scripts/create_default_users.py
   ```

**Or using Railway CLI:**
```bash
npm i -g @railway/cli
railway login
railway link  # Select your project
railway run python scripts/populate_mock_data.py
railway run python scripts/create_default_users.py
```

### Step 5: Test!

1. Visit your Vercel frontend URL
2. Login:
   - **Admin**: `EMP001` / `admin123`
   - **Analyst**: `EMP002` / `analyst123`
3. Verify:
   - ✅ Dashboard loads
   - ✅ Metrics display
   - ✅ Can generate profiles
   - ✅ Can submit feedback

---

## ✅ That's It! Your App is Live!

**Frontend**: https://your-project.vercel.app  
**Backend**: https://your-project.up.railway.app  
**API Docs**: https://your-project.up.railway.app/api/v1/docs

---

## 🎯 Quick Checklist

- [ ] Railway backend deployed
- [ ] PostgreSQL database added
- [ ] Environment variables set
- [ ] Vercel frontend deployed
- [ ] NEXT_PUBLIC_API_URL configured
- [ ] CORS_ORIGINS updated with Vercel URL
- [ ] Database initialized (populate_mock_data.py)
- [ ] Default users created (create_default_users.py)
- [ ] Tested login and dashboard

---

## ⏱️ Total Time: 10-15 minutes

**Need help?** See detailed guide: `DEPLOYMENT_READY.md`
