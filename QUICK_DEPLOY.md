# ⚡ Quick Deployment Guide

**Fastest way to deploy:** Vercel (Frontend) + Railway (Backend)

## 🚀 **5-Minute Deployment**

### **Step 1: Deploy Backend (Railway)**

1. Go to [railway.app](https://railway.app) → Sign up with GitHub
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. **Important**: Set **Root Directory** to `backend`
5. Add PostgreSQL: Click "+ New" → "Database" → "Add PostgreSQL"
6. Copy the PostgreSQL `DATABASE_URL` from the database service
7. In backend service, add environment variables:
   ```
   DATABASE_URL=<paste-postgres-url-here>
   GEMINI_API_KEY=<your-gemini-api-key>
   ENVIRONMENT=production
   DEBUG=False
   CORS_ORIGINS=["https://your-frontend.vercel.app"]
   ```
8. Railway auto-deploys! Copy your backend URL

### **Step 2: Deploy Frontend (Vercel)**

1. Go to [vercel.com](https://vercel.com) → Sign up with GitHub
2. Click "Add New" → "Project"
3. Import your GitHub repository
4. **Important**: Set **Root Directory** to `frontend`
5. Add environment variable:
   ```
   NEXT_PUBLIC_API_URL=<your-railway-backend-url>
   ```
6. Click "Deploy" → Vercel builds and deploys automatically!
7. Copy your frontend URL

### **Step 3: Connect Frontend & Backend**

1. Go back to Railway backend environment variables
2. Update `CORS_ORIGINS`:
   ```
   CORS_ORIGINS=["https://your-frontend.vercel.app"]
   ```
3. Redeploy backend (Railway auto-redeploys on env var change)

### **Step 4: Initialize Database**

Using Railway CLI:
```bash
npm i -g @railway/cli
railway login
railway link  # Link to your Railway project
railway run python scripts/populate_mock_data.py
```

Or use Railway's web terminal:
- Go to Railway dashboard → Backend service → "Deployments" → Click latest → "View Logs" → Use terminal

### **Done! 🎉**

Visit your Vercel frontend URL and test:
- ✅ Dashboard loads
- ✅ Profile generation works
- ✅ Bias metrics display

---

## 📝 **Environment Variables Checklist**

### **Backend (Railway)**
- [ ] `DATABASE_URL` (from Railway PostgreSQL)
- [ ] `GEMINI_API_KEY`
- [ ] `ENVIRONMENT=production`
- [ ] `DEBUG=False`
- [ ] `CORS_ORIGINS` (with your Vercel URL)

### **Frontend (Vercel)**
- [ ] `NEXT_PUBLIC_API_URL` (your Railway backend URL)

---

## 🔧 **Troubleshooting**

**CORS Error?**
- Make sure `CORS_ORIGINS` in Railway includes your exact Vercel URL (with `https://`)

**Database Empty?**
- Run `railway run python scripts/populate_mock_data.py`

**Backend Not Starting?**
- Check Railway logs: Dashboard → Backend → "Deployments" → View logs
- Verify all environment variables are set

**Frontend Can't Connect?**
- Verify `NEXT_PUBLIC_API_URL` in Vercel matches your Railway backend URL
- Check Railway backend is running (visit backend URL + `/health`)

---

## 💰 **Cost**

- **Vercel**: Free (Hobby plan)
- **Railway**: Free ($5 credit/month)
- **Total**: $0/month for small projects ✅

---

**Need more details?** See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)
