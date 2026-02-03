# Hugging Face Spaces Deployment Guide

## 🚀 Quick Deployment (5 Minutes)

### Step 1: Create Hugging Face Account
1. Go to [huggingface.co](https://huggingface.co/)
2. Click "Sign Up" and create a free account
3. Verify your email

### Step 2: Create a New Space
1. Click your profile → "New Space"
2. Fill in the details:
   - **Space name**: `yt-web-summarizer` (or your preferred name)
   - **License**: MIT
   - **Select SDK**: Streamlit
   - **Space hardware**: CPU Basic (free)
   - **Visibility**: Public (for free hosting)

3. Click "Create Space"

### Step 3: Upload Files

You have two options:

#### Option A: Git Upload (Recommended)
```bash
# Clone your space
git clone https://huggingface.co/spaces/YOUR_USERNAME/yt-web-summarizer
cd yt-web-summarizer

# Copy all files from your project
cp /workspaces/yt-web-summarizer/*.py .
cp /workspaces/yt-web-summarizer/requirements.txt .
cp /workspaces/yt-web-summarizer/packages.txt .
cp /workspaces/yt-web-summarizer/HF_README.md ./README.md

# Commit and push
git add .
git commit -m "Initial deployment"
git push
```

#### Option B: Web Upload
1. In your Space, click "Files and versions"
2. Click "Add file" → "Upload files"
3. Upload these files:
   - `app.py`
   - `config.py`
   - `services.py`
   - `utils.py`
   - `logger.py`
   - `exceptions.py`
   - `requirements.txt`
   - `packages.txt`
   - `HF_README.md` (rename to `README.md`)
4. Commit changes

### Step 4: Configure README
The `HF_README.md` file contains the proper YAML header for Hugging Face Spaces. Make sure it's renamed to `README.md` in your space.

### Step 5: Wait for Build
- Hugging Face will automatically build your app
- This takes 2-5 minutes
- Watch the build logs in the "Logs" tab
- Once complete, your app will be live!

### Step 6: Access Your App
Your app will be available at:
```
https://huggingface.co/spaces/YOUR_USERNAME/yt-web-summarizer
```

## 🔧 Configuration

### Environment Variables (Optional)
If you want to pre-configure settings:

1. Go to your Space settings
2. Add secrets/variables:
   - `GROQ_API_KEY`: Your default API key (not recommended - users should provide their own)
   - `ENVIRONMENT`: `production`

### Space Settings
- **Hardware**: CPU Basic (free) - sufficient for most use cases
- **Upgrade Options**: 
  - CPU Upgrade: €0.03/hour (faster processing)
  - T4 GPU: €0.60/hour (for large Whisper models)

## 📊 Features on Hugging Face Spaces

✅ **Always-On**: No cold starts, instant response
✅ **Free Hosting**: Completely free for public spaces
✅ **Automatic HTTPS**: Secure connection out of the box
✅ **Community Sharing**: Easy to share and embed
✅ **Version Control**: Git-based versioning
✅ **Analytics**: Built-in usage analytics
✅ **Easy Updates**: Just push to update

## 🎯 Best Practices

### For Free Tier:
1. Use **base** Whisper model (best speed/accuracy balance)
2. Keep summaries reasonable length (200-500 words)
3. Enable caching to reduce API costs
4. Public spaces are always free

### For Better Performance:
1. Upgrade to CPU Upgrade (€0.03/hour)
2. Use GPU for large Whisper models
3. Add more system RAM if needed

## 🔒 Security Notes

**Important**: Users should provide their own Groq API keys. Never hardcode API keys in public spaces.

Your app is configured to:
- Request API key from users (stored only in session)
- Validate API key format
- Rate limit requests
- Cache results to minimize API calls

## 🐛 Troubleshooting

### Build Fails
- Check `requirements.txt` for package conflicts
- Ensure all Python files are valid
- Check build logs for specific errors

### App Crashes
- Verify all dependencies in `requirements.txt`
- Check `packages.txt` for system dependencies (ffmpeg is required)
- Review app logs in Hugging Face

### Slow Performance
- Use smaller Whisper model (tiny or base)
- Reduce summary length
- Consider upgrading hardware

### API Errors
- Ensure users provide valid Groq API key
- Check Groq service status
- Verify rate limiting settings

## 📈 Monitoring

Monitor your Space:
1. Go to your Space dashboard
2. Check "Analytics" tab for:
   - Total views
   - Unique users
   - Usage patterns
3. Review "Logs" for errors

## 🔄 Updating Your App

To update:
```bash
# Make changes locally
# Then push to HF
git add .
git commit -m "Update: description of changes"
git push
```

Hugging Face will automatically rebuild and redeploy.

## 🌟 Making Your Space Popular

1. **Good README**: The HF_README.md is pre-configured with:
   - Clear description
   - Usage instructions
   - Feature highlights
   - Screenshots (add your own)

2. **Tags**: Add relevant tags in Space settings:
   - `summarization`
   - `nlp`
   - `youtube`
   - `llm`
   - `groq`

3. **Community**: 
   - Share on Twitter/LinkedIn
   - Add to Hugging Face collections
   - Respond to user feedback

## 💰 Cost Estimate

**Hugging Face Spaces**: FREE (public)
**Groq API**: 
- Free tier: Generous limits
- Users provide their own keys
- Caching reduces costs by ~70%

**Total Cost**: $0/month for you! Users pay for their own API usage.

## 🎉 You're Done!

Your app is now live and accessible to anyone in the world!

**Share your Space**: 
```
https://huggingface.co/spaces/YOUR_USERNAME/yt-web-summarizer
```

---

**Need help?** Check Hugging Face Spaces documentation or open an issue on GitHub!
