# 🎯 Content Summarizer Pro - Production Guide

A professional-grade content summarization platform that transforms YouTube videos and websites into concise, actionable summaries using AI.

## 🚀 Features

### Core Features
- **📺 YouTube Summarization**: Auto-transcribe videos and generate summaries
- **🌐 Website Content Summarization**: Extract and summarize web content
- **🤖 Multiple AI Models**: Support for various LLM providers (Groq)
- **🎨 Customizable Summaries**: 5 different summary styles
- **⚡ Smart Caching**: Avoid reprocessing identical content
- **📊 Analytics Dashboard**: Track usage and performance metrics
- **🔒 Secure API Key Management**: Built-in validation and security

### Advanced Features
- **🎚️ Rate Limiting**: Prevent API abuse and cost overruns
- **📚 Summary History**: Track all previous summaries
- **📥 Multiple Export Formats**: Download summaries as text, JSON, or Markdown
- **🌍 Multi-Language Support**: Process content in different languages
- **⚙️ Advanced Configuration**: Feature flags and environment-based settings
- **📊 Performance Metrics**: Reading time estimation and word count statistics
- **🔄 Smart Retries**: Automatic error recovery with exponential backoff
- **📝 Comprehensive Logging**: Debug and monitor application behavior

## 📋 Requirements

- Python 3.9+
- CUDA 11.8+ (optional, for GPU acceleration)
- API Key from [Groq](https://console.groq.com/)
- FFmpeg (for audio processing)

## 🔧 Installation

### 1. Quick Start (Development)

```bash
# Clone repository
git clone https://github.com/reethj-07/yt-web-summarizer.git
cd yt-web-summarizer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your Groq API key

# Run application
streamlit run app.py
```

### 2. Docker Deployment

```bash
# Build image
docker build -t yt-summarizer .

# Run container
docker run -p 8501:8501 \
  -e GROQ_API_KEY=your_key_here \
  yt-summarizer

# Or use docker-compose
docker-compose up -d
```

### 3. Cloud Deployment (Streamlit Cloud)

1. Fork the repository
2. Connect to Streamlit Cloud
3. Configure secrets in Streamlit dashboard
4. Deploy directly from GitHub

## 🎯 Usage

### Basic Usage

1. **Start the app**:
   ```bash
   streamlit run app.py
   ```

2. **Configure settings** in the sidebar:
   - Enter your Groq API key
   - Select Whisper model size (base/small/medium/large)
   - Choose summary style (balanced/bullet_points/executive/technical/simplified)
   - Adjust summary length

3. **Paste URL** and click "✨ Summarize Content"

4. **Export results** in your preferred format

### Advanced Usage

#### Custom Summary Styles

```python
# Balanced (default)
# Key points with context

# Bullet Points
# Quick overview in list format

# Executive
# High-level summary for decision makers

# Technical
# Focus on technical details and specifications

# Simplified
# Easy-to-understand explanation
```

#### Programmatic Usage

```python
from services import YouTubeService, SummarizationService
from utils import URLValidator

# Initialize service
service = SummarizationService(api_key="your_groq_key")

# Process YouTube
transcript = YouTubeService.download_and_transcribe(url, "base")

# Summarize
summary = service.summarize(docs, style="executive", length=300)
```

## 🏗️ Architecture

### Project Structure

```
yt-web-summarizer/
├── app.py                 # Main Streamlit application
├── config.py             # Configuration management
├── logger.py             # Logging utilities
├── exceptions.py         # Custom exceptions
├── utils.py              # Utility functions
├── services.py           # Core services (YouTube, Website, LLM)
├── test_app.py           # Unit tests
├── requirements.txt      # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose setup
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
└── .github/
    └── workflows/
        └── ci-cd.yml     # GitHub Actions CI/CD
```

### Component Overview

#### Config (`config.py`)
- Centralized configuration management
- Environment-based settings (development/production)
- Feature flags for gradual rollout
- Default values and validation

#### Services (`services.py`)
- **YouTubeService**: Download, transcribe audio
- **WebsiteService**: Load and extract web content
- **SummarizationService**: LLM-based content summarization

#### Utilities (`utils.py`)
- **URLValidator**: Validate and categorize URLs
- **APIKeyValidator**: Validate API credentials
- **SimpleCache**: In-memory caching with TTL
- **RateLimiter**: Request rate limiting
- **Text utilities**: Sanitization, reading time, formatting

#### Error Handling (`exceptions.py`)
- Custom exception hierarchy
- Structured error information
- Debugging support

## ⚙️ Configuration

### Environment Variables

Create `.env` file based on `.env.example`:

```env
# Groq API
GROQ_API_KEY=your_key_here
GROQ_MODEL=llama3-8b-8192

# Whisper
WHISPER_DEVICE=auto  # cuda, cpu, or auto

# Summarization
DEFAULT_SUMMARY_LENGTH=300
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

# Environment
ENVIRONMENT=production
```

### Feature Flags

Control features via environment variables:

- `ENABLE_CACHE`: Smart caching of summaries
- `ENABLE_RATE_LIMITING`: API rate limiting
- `ENABLE_HISTORY`: Summary history tracking
- `ENABLE_EXPORT`: Export functionality
- `ENABLE_ANALYTICS`: Usage analytics

## 🧪 Testing

```bash
# Run all tests
pytest test_app.py -v

# With coverage
pytest test_app.py --cov=. --cov-report=html

# Run specific test
pytest test_app.py::TestURLValidator -v
```

## 🔒 Security Best Practices

1. **Never commit `.env` files**: Use `.env.example` as template
2. **Rotate API keys regularly**: Update keys in Streamlit secrets
3. **Use strong API keys**: Only use official Groq API keys
4. **Enable rate limiting**: Prevent abuse in production
5. **Monitor logs**: Check logs for suspicious activity
6. **Use HTTPS**: Always use HTTPS in production
7. **Validate inputs**: All inputs are validated before processing

## 🐛 Troubleshooting

### Common Issues

#### "numpy is not available"
```bash
pip install numpy==2.2.6
```

#### GPU not detected
```bash
# Check CUDA availability
python -c "import torch; print(torch.cuda.is_available())"

# Set device manually
export WHISPER_DEVICE=cuda
```

#### Rate limit exceeded
- Wait the specified time before retrying
- Adjust `RATE_LIMIT_CALLS` and `RATE_LIMIT_PERIOD_SECONDS`

#### YouTube download fails
- Ensure FFmpeg is installed
- Check internet connection
- Verify URL is accessible

## 📊 Performance Optimization

### Caching Strategy
- Results cached for 1 hour (configurable)
- Cache key: `url + style + length`
- Automatic cleanup on expiration

### Rate Limiting
- Default: 10 calls per 60 seconds
- Adjustable via environment variables
- Per-user tracking available

### GPU Acceleration
- Automatic GPU detection
- Fallback to CPU if CUDA unavailable
- Configurable via `WHISPER_DEVICE`

## 🚀 Deployment

### Streamlit Cloud
1. Push code to GitHub
2. Create Streamlit Cloud account
3. Connect repository
4. Add Groq API key to secrets
5. Deploy with one click

### Docker
```bash
docker-compose up -d
# Access at http://localhost:8501
```

### Production Checklist
- [ ] Use production environment (`ENVIRONMENT=production`)
- [ ] Enable rate limiting
- [ ] Configure file logging
- [ ] Set up monitoring/alerting
- [ ] Use strong API keys
- [ ] Enable HTTPS/SSL
- [ ] Configure backup strategy
- [ ] Set up health checks

## 📈 Monitoring & Analytics

### Available Metrics
- Summary count
- Average processing time
- Cache hit rate
- API usage
- Error rates

### Logging
- All operations logged to `logs/app.log`
- Configurable log level
- Structured exception information

## 🤝 Contributing

1. Fork repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Make changes and test: `pytest`
4. Commit: `git commit -m "Add amazing feature"`
5. Push: `git push origin feature/amazing-feature`
6. Open Pull Request

## 📝 License

MIT License - see LICENSE file for details

## 🙋 Support

- **Documentation**: See `/docs` folder
- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Email**: reethj-07@github.com

## 🔗 Resources

- [Groq API Documentation](https://console.groq.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [LangChain Documentation](https://python.langchain.com/)
- [OpenAI Whisper](https://github.com/openai/whisper)

---

**Last Updated**: February 2026
**Version**: 2.0.0 (Production Release)
