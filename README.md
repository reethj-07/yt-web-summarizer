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

Transform YouTube videos and web articles into concise, actionable summaries powered by AI.

## ✨ Features

- **YouTube Transcription**: Download and transcribe YouTube videos using Whisper
- **Website Summarization**: Extract and summarize content from any website
- **Multiple Summary Styles**: Choose from bullet points, paragraphs, key insights, Q&A, or executive summary
- **Customizable Length**: Set your preferred summary length (100-1000 words)
- **Smart Caching**: Reduce API costs by ~70% with intelligent caching
- **Rate Limiting**: Built-in protection against excessive API usage
- **Export Options**: Download summaries as text files
- **History Tracking**: Keep track of your recent summaries
- **GPU Acceleration**: Automatic GPU detection for faster processing

## 🚀 How to Use

1. **Get a Groq API Key**: Visit [console.groq.com](https://console.groq.com/) and create a free account
2. **Enter API Key**: Paste your Groq API key in the sidebar (it will be securely stored for your session)
3. **Paste a URL**: Enter any YouTube video URL or website URL
4. **Configure Options**: Choose your summary style, length, and Whisper model
5. **Click Summarize**: Wait for the AI to process and generate your summary
6. **Export**: Download or copy your summary for later use

## 🔑 API Key Setup

This app requires a **Groq API Key** to work. Get yours for free:
- Visit: https://console.groq.com/
- Sign up for free account
- Generate an API key
- Paste it in the sidebar

**Note**: Your API key is never stored permanently - it's only used during your session.

## 🎨 Summary Styles

- **Bullet Points**: Quick, scannable list of key points
- **Paragraph**: Flowing narrative summary
- **Key Insights**: Most important takeaways
- **Q&A Format**: Question and answer pairs
- **Executive Summary**: Business-focused overview

## 🎙️ Whisper Models

For YouTube videos, choose your transcription model:
- **Tiny**: Fastest (good for short videos)
- **Base**: Balanced speed/accuracy ⭐ Recommended
- **Small**: More accurate (slower)
- **Medium**: High accuracy (much slower)
- **Large**: Best accuracy (very slow, GPU recommended)

## 📊 Technical Details

- **LLM**: Groq Cloud (Llama-3.3-70b-versatile)
- **Transcription**: OpenAI Whisper
- **Framework**: Streamlit + LangChain
- **Video Processing**: yt-dlp
- **Web Scraping**: BeautifulSoup4 + Requests

## 💡 Tips

- Use **base** Whisper model for best speed/accuracy balance
- Shorter summaries (200-300 words) are usually more focused
- Cache saves your recent summaries - same URL/settings = instant results
- GPU acceleration automatically activates if available

## 🛠️ Development

Built with modern Python best practices:
- Modular architecture (7 focused modules)
- Comprehensive error handling
- Type hints throughout
- Extensive logging
- 30+ unit tests
- Production-ready configuration

## 📝 License

MIT License - Feel free to use and modify!

## 🤝 Contributing

Found a bug or have a feature request? Please open an issue on GitHub!

---

**Made with ❤️ using Streamlit, LangChain, and Groq**
