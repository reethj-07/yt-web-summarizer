"""
Services for content processing: YouTube, Website, and LLM integration.
"""

import os
import tempfile
from typing import List, Optional
import torch
import whisper
import yt_dlp
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain

from logger import setup_logging
from exceptions import (
    YouTubeProcessingException,
    WebsiteProcessingException,
    TranscriptionException,
    SummarizationException,
    GroqAPIException,
)
from config import current_config as config

logger = setup_logging(__name__)


class YouTubeService:
    """Service for processing YouTube videos."""

    @staticmethod
    def download_and_transcribe(
        url: str, whisper_model_size: str = "base"
    ) -> str:
        """
        Download YouTube video and transcribe audio.

        Args:
            url: YouTube URL
            whisper_model_size: Whisper model size (base, small, medium, large)

        Returns:
            Transcribed text

        Raises:
            YouTubeProcessingException: If download fails
            TranscriptionException: If transcription fails
        """
        try:
            logger.info(f"Starting YouTube download: {url}")

            # Configure yt-dlp options
            ydl_opts = {
                "format": "bestaudio[ext=m4a]/bestaudio/best",
                "quiet": False,
                "no_warnings": False,
                "noplaylist": True,
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ],
            }

            with tempfile.TemporaryDirectory() as tmpdir:
                audio_path = os.path.join(tmpdir, "temp_audio.%(ext)s")
                ydl_opts["outtmpl"] = audio_path

                # Download audio
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    logger.info(f"Downloaded: {info.get('title', 'Unknown')}")

                audio_file = os.path.join(tmpdir, "temp_audio.mp3")

                if not os.path.exists(audio_file):
                    raise YouTubeProcessingException(
                        "Audio file not found after download."
                    )

                # Transcribe using Whisper
                logger.info(f"Transcribing with Whisper ({whisper_model_size})...")
                device = (
                    "cuda"
                    if config.WHISPER_DEVICE == "auto" and torch.cuda.is_available()
                    else config.WHISPER_DEVICE
                )
                model = whisper.load_model(whisper_model_size, device=device)
                result = model.transcribe(audio_file)
                transcript = result.get("text", "").strip()

                if not transcript:
                    raise TranscriptionException(
                        "Transcription resulted in empty text."
                    )

                logger.info("Transcription completed successfully")
                return transcript

        except YouTubeProcessingException:
            raise
        except TranscriptionException:
            raise
        except Exception as e:
            logger.error(f"YouTube processing error: {str(e)}")
            raise YouTubeProcessingException(
                f"Failed to process YouTube video: {str(e)}",
                details={"original_error": str(e)},
            )


class WebsiteService:
    """Service for processing website content."""

    @staticmethod
    def load_and_extract(url: str) -> List[Document]:
        """
        Load and extract content from website.

        Args:
            url: Website URL

        Returns:
            List of Document objects

        Raises:
            WebsiteProcessingException: If loading or extraction fails
        """
        try:
            logger.info(f"Loading website content: {url}")

            loader = WebBaseLoader(url)
            docs = loader.load()

            if not docs:
                raise WebsiteProcessingException(
                    "No content found on the website."
                )

            if not docs[0].page_content.strip():
                raise WebsiteProcessingException(
                    "Website content is empty or not readable."
                )

            # Truncate content to manageable size
            for doc in docs:
                if len(doc.page_content) > config.MAX_WEBSITE_CONTENT_LENGTH:
                    doc.page_content = doc.page_content[
                        : config.MAX_WEBSITE_CONTENT_LENGTH
                    ]
                    logger.info(
                        f"Content truncated to {config.MAX_WEBSITE_CONTENT_LENGTH} characters"
                    )

            logger.info(f"Successfully loaded content from website")
            return docs

        except WebsiteProcessingException:
            raise
        except Exception as e:
            logger.error(f"Website processing error: {str(e)}")
            raise WebsiteProcessingException(
                f"Failed to load website content: {str(e)}",
                details={"original_error": str(e)},
            )


class SummarizationService:
    """Service for content summarization using LLM."""

    def __init__(self, api_key: str):
        """
        Initialize summarization service.

        Args:
            api_key: Groq API key
        """
        self.api_key = api_key
        self._llm = None

    def get_llm(self):
        """Get or create LLM instance."""
        if self._llm is None:
            try:
                self._llm = ChatGroq(
                    model=config.GROQ_MODEL,
                    groq_api_key=self.api_key,
                    temperature=0.5,
                    max_retries=config.GROQ_MAX_RETRIES,
                )
            except Exception as e:
                logger.error(f"Failed to initialize ChatGroq: {str(e)}")
                raise GroqAPIException(
                    "Failed to initialize summarization service",
                    details={"original_error": str(e)},
                )
        return self._llm

    def get_summary_prompt(
        self, style: str = "balanced", length: int = 300
    ) -> PromptTemplate:
        """
        Get prompt template for specific summarization style.

        Args:
            style: Summarization style (balanced, bullet_points, executive, technical, simplified)
            length: Target summary length in words

        Returns:
            PromptTemplate object
        """
        prompts = {
            "balanced": f"""Provide a balanced summary of the following content in approximately {length} words. 
Cover the main points clearly and concisely:
Content:{{text}}
Summary:""",
            "bullet_points": f"""Summarize the following content as concise bullet points (5-8 points). 
Focus on key takeaways:
Content:{{text}}
Summary:""",
            "executive": f"""Create an executive summary of the following content in {length} words. 
Include key findings and recommendations:
Content:{{text}}
Summary:""",
            "technical": f"""Provide a technical summary of the following content in {length} words. 
Focus on technical details and specifications:
Content:{{text}}
Summary:""",
            "simplified": f"""Explain the following content in simple terms ({length} words). 
Make it understandable to non-experts:
Content:{{text}}
Summary:""",
        }

        template = prompts.get(style, prompts["balanced"])
        return PromptTemplate(template=template, input_variables=["text"])

    def summarize(
        self,
        docs: List[Document],
        style: str = "balanced",
        length: int = 300,
    ) -> str:
        """
        Summarize documents using LLM.

        Args:
            docs: List of documents to summarize
            style: Summarization style
            length: Target summary length in words

        Returns:
            Summary text

        Raises:
            SummarizationException: If summarization fails
        """
        try:
            logger.info(f"Starting summarization ({style} style, {length} words)")

            if not docs:
                raise SummarizationException("No documents provided for summarization")

            llm = self.get_llm()
            prompt = self.get_summary_prompt(style, length)

            chain = load_summarize_chain(
                llm, chain_type="stuff", prompt=prompt
            )
            summary = chain.run(docs)

            if not summary or not summary.strip():
                raise SummarizationException("Summarization resulted in empty output")

            logger.info("Summarization completed successfully")
            return summary.strip()

        except SummarizationException:
            raise
        except Exception as e:
            logger.error(f"Summarization error: {str(e)}")
            raise SummarizationException(
                f"Failed to summarize content: {str(e)}",
                details={"original_error": str(e)},
            )
