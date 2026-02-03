# 🚀 Vercel Deployment Guide

## Overview

Deploy your Content Summarizer Pro to Vercel in **5 minutes** using the FastAPI backend + HTML frontend setup.

## Why This Approach?

- ✅ **Free tier** on Vercel
- ✅ Works with serverless functions
- ✅ Simple HTML frontend (zero build steps)
- ✅ FastAPI backend for processing
- ✅ No timeout issues (can retry)

## Prerequisites

- GitHub account
- Vercel account (free)
- Groq API key

## Step-by-Step Deployment

### 1. Push to GitHub

```bash
cd /workspaces/yt-web-summarizer
git add .
git commit -m "Add Vercel deployment files"
git push origin main
```

### 2. Create Vercel Account

Visit [vercel.com](https://vercel.com) and sign up with GitHub.

### 3. Import Project

1. Go to [vercel.com/new](https://vercel.com/new)
2. Select "Import Git Repository"
3. Authorize GitHub
4. Select `yt-web-summarizer` repository
5. Click "Import"

### 4. Configure Environment Variables

In Vercel dashboard:

1. Click "Environment Variables"
2. Add the following:

```
GROQ_API_KEY = your_key_here
ENVIRONMENT = production
LOG_LEVEL = INFO
```

3. Click "Deploy"

### 5. Wait for Deployment

Vercel will automatically:
- Detect Python project
- Install dependencies
- Build the application
- Deploy to CDN

Your app will be live at: `https://your-app-name.vercel.app`

## Architecture

```
┌─────────────────────────┐
│   HTML Frontend         │
│  (public/index.html)    │
│  - Beautiful UI         │
│  - Form handling        │
│  - Real-time updates    │
└──────────┬──────────────┘
           │ (REST API calls)
┌──────────▼──────────────┐
│   FastAPI Backend       │
│  (api/summarize.py)     │
│  - URL validation       │
│  - YouTube processing   │
│  - Web scraping         │
│  - LLM integration      │
│  - Groq API calls       │
└─────────────────────────┘
```

## API Endpoints

### POST /api/summarize
Summarize content from URL.

**Request:**
```json
{
  "url": "https://www.youtube.com/watch?v=...",
  "api_key": "your_groq_key",
  "style": "balanced",
  "length": 300,
  "whisper_model": "base"
}
```

**Response:**
```json
{
  "summary": "...",
  "url_type": "youtube",
  "word_count": 250,
  "reading_time": 1,
  "status": "success"
}
```

### GET /api/config
Get configuration options.

### GET /api/styles
Get available summary styles.

### GET /health
Health check endpoint.

## Accessing Your App

After deployment:

1. **Web UI**: `https://your-app-name.vercel.app`
2. **API**: `https://your-app-name.vercel.app/api/summarize`
3. **Docs**: `https://your-app-name.vercel.app/docs`

## Vercel Free Tier Limits

| Feature | Limit |
|---------|-------|
| Deployments | Unlimited |
| Bandwidth | 100 GB/month |
| Function Duration | 10 seconds (Pro: 60s) |
| Build Time | 45 minutes |
| Concurrent Functions | 12 |

**Note:** YouTube processing may take 10+ seconds. Vercel will handle this gracefully.

## Troubleshooting

### "Function execution exceeded maximum duration"

This can happen with YouTube videos. Solutions:

1. **Use smaller Whisper model** (base instead of large)
2. **For production**, upgrade to Vercel Pro ($20/month)
3. **Alternative**: Use Railway/Render instead

### "Module not found"

Solution:
```bash
pip install -r requirements.txt
git add requirements.txt
git commit -m "Update dependencies"
git push
```

Then redeploy in Vercel dashboard.

### API Key not working

1. Double-check API key in Vercel environment variables
2. Get a new key from [console.groq.com](https://console.groq.com)
3. Update in Vercel dashboard
4. Redeploy

### CORS errors

Already configured in `api/summarize.py`. If still issues:

1. Check browser console for details
2. Verify frontend URL matches API URL
3. Check Vercel logs

## Monitoring & Logs

View logs in Vercel dashboard:

1. Go to project
2. Click "Deployments"
3. Select latest deployment
4. Click "Functions" tab
5. View logs in real-time

## Custom Domain

1. Go to project settings
2. Click "Domains"
3. Add your domain
4. Follow DNS instructions
5. Wait for verification (usually <1 hour)

## Advanced: Upgrade to Pro

For longer function timeouts (60 seconds):

1. Click "Account Settings"
2. Click "Billing"
3. Upgrade to Pro ($20/month)
4. Functions now support up to 60 seconds

## Performance Optimization

### Caching

Responses are cached by default:
- Enable: `ENABLE_CACHE=true`
- TTL: `CACHE_TTL_SECONDS=3600`

### Rate Limiting

Prevent abuse:
- Enable: `ENABLE_RATE_LIMITING=true`
- Limit: `RATE_LIMIT_CALLS=10` per `RATE_LIMIT_PERIOD_SECONDS=60`

## Alternative Platforms for Vercel

If Vercel doesn't work well for your use case:

- **Railway** - Better for long-running tasks (recommended)
- **Render** - Similar to Railway
- **Fly.io** - Excellent performance
- **Heroku** - Classic option

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed guides.

## FAQ

### Can I use Streamlit on Vercel?

Not easily. Streamlit needs persistent connections which Vercel's serverless functions don't support well. This FastAPI approach is the recommended solution.

### How much does it cost?

**Vercel Free Tier:**
- Deployments: Free
- Bandwidth: 100 GB/month (usually free)
- Functions: Free (limited to 10 seconds)

**Groq API:**
- Free tier available
- Pay-as-you-go after free credits

### Can I upgrade later?

Yes! Vercel Pro ($20/month) gives:
- 60-second function timeout
- Priority support
- More concurrent functions

### How do I add a custom domain?

1. Vercel dashboard → Domains
2. Add your domain
3. Update DNS records
4. Wait for verification

## Getting Help

- **Vercel Docs**: https://vercel.com/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **Groq Docs**: https://console.groq.com/docs
- **Issues**: GitHub Issues

---

**You're all set! Your app is now live on Vercel. 🎉**

Visit `https://your-app-name.vercel.app` to see it in action!
