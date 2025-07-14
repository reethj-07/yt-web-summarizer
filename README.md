Streamlit YT/Web Summarizer
Summarize YouTube videos or website content into concise, readable text using Streamlit, OpenAI Whisper, and LangChain LLMs.

Features
Summarize YouTube Videos:
Downloads audio, transcribes it with Whisper, and generates a summary.

Summarize Website Content:
Loads and summarizes text content from any public URL.

Modern LLM Integration:
Uses Groq LLM via LangChain for high-quality, customizable summaries.

Device Awareness:
Detects and displays whether your system uses GPU or CPU for Whisper.

User-Friendly UI:
Clean, interactive interface built with Streamlit.

Setup Instructions
1. Clone the Repository
bash
git clone https://github.com/yourusername/yt-web-summarizer.git
cd yt-web-summarizer
2. Create & Activate a Virtual Environment
bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
3. Install Dependencies
bash
pip install -r requirements.txt
4. Set Up API Keys
Obtain a Groq API key from the Groq platform.

You can set it in a .env file or enter it in the app sidebar at runtime.

5. Run the App
bash
streamlit run app.py
How to Use
Start the app (see above).

Enter your Groq API key in the sidebar.

Choose Whisper model size (base, small, medium, large).

Paste a YouTube or website URL in the main input.

Click "Summarize the Content from YT or Website".

Wait for processing:

For YouTube: Downloads audio, transcribes, then summarizes.

For websites: Loads and summarizes page text.

View your summary in the app window.

Example
YouTube:
Paste a link like https://www.youtube.com/watch?v=SLsTskih7_I and get a summary of the video’s content.

Website:
Paste a link like https://en.wikipedia.org/wiki/Artificial_intelligence to summarize the main text.

Notes & Tips
API Key Security: Never share your API key or commit .env files to public repositories.

Requirements:

Python 3.8 or higher recommended.

For best performance, use a CUDA-capable GPU for Whisper.

Troubleshooting:

If you see missing package errors, run pip install -r requirements.txt again.

If you see “Numpy is not available,” ensure you use numpy==1.26.4 and not version 2.x.

.gitignore:
This repo should include a .gitignore to exclude venv/, .env, and other non-source files.

Project Structure
File/Folder	               Purpose
app.py	Main        -   Streamlit app code
requirements.txt  -   All dependencies and versions
.gitignore	   -   Files/folders to exclude from git
README.md	   -   This documentation
 Contributing
Pull requests and issues are welcome! Please open an issue to discuss any major changes.

 License
This project is licensed under the MIT License.

Acknowledgments
OpenAI Whisper

Streamlit

LangChain

yt-dlp

Groq

Enjoy summarizing!
If you have questions or suggestions, open an issue or contact the maintainer via GitHub.