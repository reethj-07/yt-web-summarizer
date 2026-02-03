---
title: YT Web Summarizer
emoji: 🎬
colorFrom: purple
colorTo: pink
sdk: streamlit
sdk_version: "1.40.2"
app_file: app.py
pinned: false
license: mit
python_version: "3.10"
---

# 🎬 YT Web Summarizer

AI-powered tool to transform YouTube videos and web articles into concise, actionable summaries.

## ✨ Features

- 🎥 **YouTube Transcription** - Automatic audio extraction and transcription using OpenAI Whisper
- 🌐 **Website Summarization** - Extract and summarize content from any web article
- 🎨 **5 Summary Styles** - Bullet points, paragraphs, key insights, Q&A format, or executive summary
- ⚡ **Smart Caching** - Reduce API costs by ~70% with intelligent caching system
- 🛡️ **Rate Limiting** - Built-in protection against excessive API usage
- 📊 **Statistics** - Word count, reading time, and content type analysis
- 💾 **Export Options** - Download summaries as text files or copy to clipboard
- 📜 **History Tracking** - Keep track of your recent summaries
- 🚀 **GPU Support** - Automatic GPU detection for faster video processing

## 🚀 Quick Start

### 1. Get Your Groq API Key (Free)
- Visit [console.groq.com](https://console.groq.com/)
- Sign up for a free account
- Generate an API key

### 2. Use the App
- Enter your Groq API key in the sidebar
- Paste any YouTube URL or website URL
- Choose your summary style and length
- Click "✨ Summarize Content"
- Export or save your summary

**Note**: Your API key is stored only for your session and never saved permanently.


## 🎨 Summary Styles

| Style | Description | Best For |
|-------|-------------|----------|
| 📍 **Bullet Points** | Quick, scannable list of key points | Fast reference, meeting notes |
| 📝 **Paragraph** | Flowing narrative summary | Reports, blog posts |
| 💡 **Key Insights** | Most important takeaways | Executive reviews |
| ❓ **Q&A Format** | Question and answer pairs | Training, FAQs |
| 📊 **Executive Summary** | Business-focused overview | Decision makers |

## 🎙️ Whisper Model Selection

| Model | Speed | Accuracy | Use Case |
|-------|-------|----------|----------|
| Tiny | ⚡⚡⚡ | ⭐⭐ | Short videos, quick tests |
| **Base** | ⚡⚡ | ⭐⭐⭐ | **Recommended - Best balance** |
| Small | ⚡ | ⭐⭐⭐⭐ | Longer content, better accuracy |
| Medium | 🐌 | ⭐⭐⭐⭐⭐ | Professional transcription |
| Large | 🐌🐌 | ⭐⭐⭐⭐⭐ | GPU required, highest quality |

## 📊 Tech Stack

- **AI Model**: Groq Cloud (Llama-3.3-70b-versatile)
- **Transcription**: OpenAI Whisper
- **Framework**: Streamlit + LangChain
- **Video Processing**: yt-dlp
- **Web Scraping**: BeautifulSoup4

## 💡 Pro Tips

✅ Use **base** Whisper model for optimal speed/accuracy  
✅ Summaries of 200-300 words are typically most focused  
✅ Cache automatically saves recent summaries for instant access  
✅ GPU acceleration activates automatically when available  
✅ Works with any public YouTube video or web article

## 🏗️ Architecture

Built with production-ready Python:
- **Modular Design**: 7 focused modules (services, utils, config, logging, exceptions)
- **Error Handling**: Comprehensive exception hierarchy
- **Type Safety**: Full type hints throughout codebase
- **Testing**: 30+ unit tests with 80%+ coverage
- **Logging**: Structured logging with color-coded output
- **Configuration**: Environment-based settings with feature flags

## 📦 Installation (Local Development)

```bash
# Clone repository
git clone https://github.com/reethj-07/yt-web-summarizer.git
cd yt-web-summarizer

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Add your GROQ_API_KEY to .env

# Run app
streamlit run app.py
```

## 🌐 Live Demo

Try it now: [Hugging Face Spaces](https://huggingface.co/spaces/attentionseeker/genai-youtube-web-summarizer)

## 📝 License

MIT License - Free to use and modify

## 🤝 Contributing

Issues and pull requests welcome on [GitHub](https://github.com/reethj-07/yt-web-summarizer)

---

**Built with ❤️ using Streamlit, LangChain, and Groq**
