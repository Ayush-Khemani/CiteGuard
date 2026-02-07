# 🚀 CiteGuard - Vercel Deployment Guide

**Status:** Ready for live deployment on Vercel  
**Last Updated:** February 7, 2026

---

## 📋 Quick Start (10 minutes)

### Step 1: Set Up Database (Supabase - Free Postgres)

1. Go to [supabase.com](https://supabase.com)
2. Sign up or log in
3. Click "New Project"
4. Fill in:
   - **Name:** citeguard
   - **Database Password:** Create a strong password (save it!)
   - **Region:** Closest to your users
5. Click "Create new project"
6. Wait for setup (2-3 minutes)
7. Go to **Settings → Database → Connection String**
8. Copy the PostgreSQL connection string (it will look like):
   ```
   postgresql://postgres:YOUR_PASSWORD@db.RANDOM.supabase.co:5432/postgres
   ```
9. Keep this handy - you'll need it in Vercel!

### Step 2: Set Up Redis Cache (Upstash - Free Redis)

1. Go to [upstash.com](https://upstash.com)
2. Sign up or log in
3. Click "Create Database"
4. Fill in:
   - **Name:** citeguard-redis
   - **Type:** Redis
   - **Region:** Same as Supabase (recommended)
5. Click "Create"
6. Go to **Details** tab
7. Copy the **Redis URL** (it will look like):
   ```
   redis://:YOUR_PASSWORD@YOUR_ENDPOINT.upstash.io:XXXXX
   ```
8. Keep this handy!

### Step 3: Deploy to Vercel

1. **Go to [vercel.com/dashboard](https://vercel.com/dashboard)**
2. Click **"Add New..." → "Project"**
3. Click **"Import Git Repository"**
4. Search for your GitHub repo (Anti Plagrisim Detector)
5. Click **"Import"**
6. Configure the project:
   - **Framework Preset:** Python (or "Other")
   - **Root Directory:** `./` (leave as default)
   - **Build Command:** Leave blank (Vercel will auto-detect)
   - **Output Directory:** Leave blank

### Step 4: Add Environment Variables in Vercel

1. Scroll down to **"Environment Variables"**
2. Add these variables (one by one):

| Variable | Value | Where to find |
|----------|-------|---------------|
| `DATABASE_URL` | Your Supabase PostgreSQL URL | Supabase → Settings |
| `REDIS_URL` | Your Upstash Redis URL | Upstash → Details |
| `SECRET_KEY` | Create a random strong string | Generate: `openssl rand -hex 32` |
| `OPENAI_API_KEY` | Your OpenAI API key (optional) | openai.com/api-keys |
| `ANTHROPIC_API_KEY` | Your Anthropic API key (optional) | console.anthropic.com |
| `DEBUG` | `False` | (type as shown) |
| `LOG_LEVEL` | `INFO` | (type as shown) |

**Example for SECRET_KEY:**
```
Generate in terminal: python -c "import secrets; print(secrets.token_hex(32))"
```

3. Each time you add a variable, it's saved automatically

### Step 5: Deploy!

1. Click the **"Deploy"** button
2. Wait for the build to complete (2-5 minutes)
3. Once complete, you'll see a green checkmark ✅
4. Click the **Production URL** (looks like `https://your-app.vercel.app`)
5. **Your app is LIVE! 🎉**

---

## ✅ Verify Your Deployment

1. **Visit your Vercel URL** (e.g., `https://citeguard.vercel.app`)
2. You should see the CiteGuard web interface
3. Test the API: Visit `https://your-domain.vercel.app/docs`
4. Test plagiarism detection with sample text

---

## 🔧 Troubleshooting

### "502 Bad Gateway" Error
**Solution:** Check if environment variables are set correctly
1. Go to Vercel → Project Settings → Environment Variables
2. Verify `DATABASE_URL` and `REDIS_URL` are correctly set
3. Redeploy: Click "Deployments" → Latest → Click "..." → "Redeploy"

### Database Connection Timeout
**Solution:** Whitelist Vercel's IP addresses
1. In Supabase: Go to **Settings → Network** 
2. Add Vercel IP: `0.0.0.0/0` (allows all IPs)
3. Or add specific Vercel region IPs from documentation

### "Module not found" Error
**Solution:** The `requirements.txt` might need updating
1. Ensure all dependencies are in `backend/requirements.txt`
2. Commit and push changes to GitHub
3. Redeploy on Vercel

---

## 🌐 Custom Domain (Optional but Recommended)

1. **Buy a domain** (Namecheap, GoDaddy, etc.) - ~$10/year
2. **Or get free domain:**
   - Freenom: freenom.com (free, but limited)
   - EU domains: eu.org (free if you contribute)
3. **Connect to Vercel:**
   - Go to Vercel Project → Settings → Domains
   - Enter your domain
   - Follow DNS configuration steps
   - Usually takes 1-5 minutes to activate

**Popular free domain options:**
- YourName.eu.org
- YourName.tk (Freenom)

---

## 🔒 Security Checklist

- [ ] Set `DEBUG=False` in production environment
- [ ] Use strong `SECRET_KEY` (minimum 32 characters)
- [ ] Enable HTTPS (automatic on Vercel ✅)
- [ ] Add API rate limiting (configured in backend)
- [ ] Set up monitoring with Vercel Analytics
- [ ] Regularly update dependencies

---

## 📊 Update & Redeploy

Whenever you make changes:

1. **Commit and push to GitHub:**
   ```bash
   git add .
   git commit -m "Update: feature description"
   git push origin main
   ```

2. **Vercel will automatically redeploy** (watch in Vercel Dashboard)

3. **Or manual redeploy:**
   - Go to Vercel Dashboard → Deployments
   - Click latest deployment
   - Click "..." → "Redeploy"

---

## 🚨 Important Notes

### Vercel Limitations with Python

⚠️ **Vercel has these limits for Python serverless functions:**
- **Execution timeout:** 10 seconds (60 seconds for Pro)
- **Memory:** 3GB max
- **Cold start:** May take 5-10 seconds first request

### For Long-Running Tasks

If you need processing longer than 10 seconds (e.g., analyzing large documents):
- Use **Celery** with Upstash Redis (already configured)
- Or deploy backend separately to Railway/Render/Heroku

---

## 📞 Support & Next Steps

1. **Monitor your deployment:** 
   - Check Vercel Dashboard → Analytics
   - Set up error alerts

2. **Scale up (if needed):**
   - Upgrade to Vercel Pro ($20/month) for better performance
   - Upgrade database to Supabase Pro for more connections

3. **Add Chrome Extension:**
   - Update `manifest.json` with your live domain
   - Upload to Chrome Web Store

---

## ✨ You're Live!

Your CiteGuard Anti-Plagiarism Detector is now accessible to everyone on the internet! 🎉

- **Website:** `https://your-domain.vercel.app`
- **API Docs:** `https://your-domain.vercel.app/docs`
- **API Base:** `https://your-domain.vercel.app/api/v1`

Share the link with students and educators worldwide!

