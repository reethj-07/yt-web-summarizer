# 🚀 Quick Reference Guide

## 📦 Project Files

| File | Purpose | Key Features |
|------|---------|--------------|
| `app.py` | Main Streamlit UI | Refactored, modular, production-ready |
| `config.py` | Configuration management | Environment variables, feature flags |
| `services.py` | Business logic | YouTube, Website, LLM services |
| `utils.py` | Utilities | Validation, caching, rate limiting |
| `logger.py` | Logging system | Structured, colorized, file logging |
| `exceptions.py` | Exception hierarchy | Custom, structured error handling |
| `test_app.py` | Unit tests | 30+ comprehensive tests |

## ⚙️ Environment Variables

### Required
```bash
GROQ_API_KEY=your_key_here
```

### Optional
```bash
# API Configuration
GROQ_MODEL=llama3-8b-8192
GROQ_MAX_RETRIES=3
GROQ_TIMEOUT=30

# Summarization
DEFAULT_SUMMARY_LENGTH=300
MIN_SUMMARY_LENGTH=100
MAX_SUMMARY_LENGTH=1000

# Caching
ENABLE_CACHE=true
CACHE_TTL_SECONDS=3600

# Rate Limiting
ENABLE_RATE_LIMITING=true
RATE_LIMIT_CALLS=10
RATE_LIMIT_PERIOD_SECONDS=60

# Features
ENABLE_HISTORY=true
ENABLE_EXPORT=true
ENABLE_ADVANCED_OPTIONS=true

# Logging
LOG_LEVEL=INFO
ENABLE_FILE_LOGGING=true

# Deployment
ENVIRONMENT=production
```

## 🚀 Quick Commands

### Setup
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### Development
```bash
streamlit run app.py
pytest test_app.py -v
black .
pylint **/*.py
```

### Docker
```bash
docker build -t yt-summarizer .
docker-compose up -d
```

### Deployment
```bash
# GitHub Actions will run automatically on push
# Manual deployment: see DEPLOYMENT.md
```

## 📊 Summary Styles

1. **balanced** - Key points with context (default)
2. **bullet_points** - Quick overview in list format
3. **executive** - High-level summary for decision makers
4. **technical** - Focus on technical details
5. **simplified** - Easy-to-understand explanation

## 🔒 Security Checklist

- [ ] API key in `.env` (never commit)
- [ ] Use `.env.example` as template
- [ ] Enable rate limiting in production
- [ ] Use HTTPS/SSL
- [ ] Validate all inputs
- [ ] Monitor logs for errors
- [ ] Rotate API keys regularly
- [ ] Use strong credentials

## 📈 Performance Tips

1. **Enable Caching** - Set `ENABLE_CACHE=true`
2. **Use GPU** - Set `WHISPER_DEVICE=cuda`
3. **Optimize Model** - Use `base` for speed, `large` for accuracy
4. **Rate Limiting** - Adjust for your load
5. **Monitor Logs** - Check `logs/app.log`

## 🧪 Testing

```bash
# Run all tests
pytest test_app.py -v

# With coverage
pytest test_app.py --cov=. --cov-report=html

# Specific test
pytest test_app.py::TestURLValidator -v

# With output
pytest test_app.py -v -s
```

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Import error | `pip install -r requirements.txt --force-reinstall` |
| GPU not found | `export WHISPER_DEVICE=cpu` |
| FFmpeg missing | `sudo apt install ffmpeg` |
| API error | Check API key and rate limits |
| Slow processing | Reduce Whisper model size |

## 📚 Documentation Map

- **Quick Start** → README.md
- **Production Setup** → PRODUCTION_GUIDE.md
- **Deployment** → DEPLOYMENT.md
- **API Reference** → API.md
- **Contributing** → CONTRIBUTING.md
- **What Changed** → UPGRADE_SUMMARY.md

## 🎯 Common Tasks

### Add New Summary Style
1. Edit `config.py` - Add to `SUMMARY_STYLES`
2. Edit `services.py` - Add prompt in `get_summary_prompt()`
3. Test with `pytest`

### Change Cache Duration
```bash
# In .env
CACHE_TTL_SECONDS=7200  # 2 hours
```

### Enable/Disable Features
```bash
# In .env
ENABLE_HISTORY=true
ENABLE_EXPORT=false
ENABLE_ADVANCED_OPTIONS=true
```

### Adjust Rate Limits
```bash
# In .env
RATE_LIMIT_CALLS=20
RATE_LIMIT_PERIOD_SECONDS=60
```

## 🔗 External Resources

- [Groq Console](https://console.groq.com/)
- [Streamlit Docs](https://docs.streamlit.io/)
- [Docker Docs](https://docs.docker.com/)
- [GitHub Actions](https://github.com/features/actions)

## 📞 Support

- Issues: GitHub Issues tab
- Discussions: GitHub Discussions
- Documentation: See documentation files
- Email: Open issue on GitHub

---

**This is a production-ready application. Always test changes before deploying to production.**
