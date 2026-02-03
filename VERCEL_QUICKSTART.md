# ✨ Vercel Deployment - Quick Start

## 🚀 Deploy in 5 Minutes

### Step 1: Commit & Push
```bash
cd /workspaces/yt-web-summarizer
git add .
git commit -m "Add Vercel deployment"
git push origin main
```

### Step 2: Connect Vercel

1. Visit [vercel.com/new](https://vercel.com/new)
2. Click "Import Git Repository"
3. Select your `yt-web-summarizer` repo
4. Click "Import"

### Step 3: Add Environment Variables

In Vercel dashboard, add:

```
GROQ_API_KEY = your_groq_key_here
ENVIRONMENT = production
```

Get your free Groq key: [console.groq.com](https://console.groq.com/)

### Step 4: Deploy

Click "Deploy" button and wait ~2 minutes.

### ✅ Done!

Your app is now live at: `https://your-project.vercel.app`

---

## 📁 What Changed?

**New Files:**
- `api/summarize.py` - FastAPI backend
- `api/index.py` - Vercel handler
- `public/index.html` - Beautiful frontend
- `vercel.json` - Vercel config

**What Works:**
- ✅ Full summarization on Vercel
- ✅ Free tier friendly
- ✅ Beautiful web UI
- ✅ YouTube + Website support
- ✅ 5 summary styles

---

## 🎯 Key URLs

| URL | Purpose |
|-----|---------|
| `https://your-app.vercel.app` | Web UI |
| `https://your-app.vercel.app/api/summarize` | API endpoint |
| `https://your-app.vercel.app/docs` | API documentation |
| `https://your-app.vercel.app/health` | Health check |

---

## ⚡ Architecture

```
Frontend (HTML/JS)  →  FastAPI Backend  →  Groq API
         ↓                    ↓                 ↓
  Beautiful UI      Business Logic      LLM Processing
```

---

## 📝 Environment Variables

Required:
```env
GROQ_API_KEY=your_key
```

Optional:
```env
ENVIRONMENT=production
LOG_LEVEL=INFO
ENABLE_CACHE=true
ENABLE_RATE_LIMITING=true
```

---

## 🔧 Testing Locally

Before deploying:

```bash
# Install FastAPI requirements
pip install fastapi uvicorn

# Run locally
python -m uvicorn api.index:app --reload

# Open in browser
http://localhost:8000
```

---

## ❌ Common Issues

### "Function timeout"
YouTube videos can take >10 seconds. Solutions:
1. Use smaller Whisper model (base)
2. Upgrade to Vercel Pro ($20/month)
3. Use Railway instead

### "Module not found"
```bash
pip install -r requirements.txt
git add requirements.txt
git commit -m "Fix dependencies"
git push
```

### "API key not working"
1. Get key from [console.groq.com](https://console.groq.com/)
2. Update in Vercel environment variables
3. Redeploy

---

## 📞 Support

- Full guide: [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md)
- API docs: Visit `/docs` on your deployed app
- Issues: GitHub Issues

---

**Your Vercel app is live! 🎉**

See [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md) for advanced options.
