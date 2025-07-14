import validators
import streamlit as st
import re
import os
import torch
import tempfile
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document
import whisper
import yt_dlp

# Load environment
load_dotenv()
os.environ.pop("SSL_CERT_FILE", None)  # Avoid SSL context error

# Streamlit UI
st.set_page_config(page_title="LangChain: Summarize Text From YT or Website", page_icon="🦜")
st.title("🦜 LangChain: Summarize Text From YT or Website")
st.subheader('Summarize URL')

# Sidebar API Key
with st.sidebar:
    groq_api_key = st.text_input("🔑 Groq API Key", value="", type="password")
    whisper_model_size = st.selectbox("🎙 Whisper Model", ["base", "small", "medium", "large"], index=0)

# URL Input
generic_url = st.text_input("Enter YouTube or Website URL", label_visibility="visible")

# Prompt Template
prompt_template = """
Provide a summary of the following content in 300 words:
Content:{text}
"""
prompt = PromptTemplate(template=prompt_template, input_variables=["text"])

# ▶️ Button Click
if st.button("Summarize the Content from YT or Website"):
    if not groq_api_key.strip():
        st.warning("⚠️ Please provide your Groq API key in the sidebar.")
    elif not generic_url.strip():
        st.error("❗ Please provide a URL.")
    elif not validators.url(generic_url):
        st.error("❗ Please enter a valid URL (YouTube or website).")
    else:
        try:
            with st.spinner("⏳ Processing..."):
                st.write(f"🖥 Using device: {'GPU' if torch.cuda.is_available() else 'CPU'}")

                # Initialize LLM
                llm = ChatGroq(model="llama3-8b-8192", groq_api_key=groq_api_key.strip())

                youtube_regex = r"(https?://)?(www\.)?(youtube\.com|youtu\.be)/"

                if re.match(youtube_regex, generic_url.strip()):
                    st.info("📺 Downloading and transcribing YouTube video using Whisper...")

                    ydl_opts = {
                        'format': 'bestaudio[ext=m4a]/bestaudio/best',
                        'outtmpl': None,  # Will be set dynamically
                        'quiet': False,
                        'no_warnings': False, 
                        'noplaylist': True,
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }],
                    }

                    try:
                        with tempfile.TemporaryDirectory() as tmpdir:
                            audio_path = os.path.join(tmpdir, "temp_audio.%(ext)s")
                            ydl_opts['outtmpl'] = audio_path
                            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                                ydl.download([generic_url])
                            audio_file = os.path.join(tmpdir, "temp_audio.mp3")

                            model = whisper.load_model(whisper_model_size, device="cuda" if torch.cuda.is_available() else "cpu")
                            result = model.transcribe(audio_file)
                            transcript = result["text"]

                            docs = [Document(page_content=transcript)]
                    except Exception as yt_error:
                        st.error("❌ Failed to process YouTube video.")
                        st.exception(yt_error)
                        st.stop()

                elif generic_url.strip().startswith("http"):
                    st.info("🌐 Loading website content...")
                    try:
                        loader = WebBaseLoader(generic_url)
                        docs = loader.load()

                        if not docs or not docs[0].page_content.strip():
                            st.warning("⚠️ No text content found.")
                            st.stop()

                        for doc in docs:
                            doc.page_content = doc.page_content[:4000]
                        st.info("ℹ️ Only the first 4000 characters of each page are summarized.")
                    except Exception as web_error:
                        st.error("❌ Failed to load website content.")
                        st.exception(web_error)
                        st.stop()
                else:
                    st.error("❗ Unsupported URL. Please enter a valid YouTube or website URL.")
                    st.stop()

                chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
                output_summary = chain.run(docs)

                st.success("✅ Summary:")
                st.write(output_summary)

        except Exception as e:
            st.error("🚫 Error during summarization.")
            st.exception(e)


