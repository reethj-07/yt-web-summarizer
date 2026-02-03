"""
Main Streamlit application for YT Web Summarizer.
Production-ready with advanced features, error handling, and caching.
"""

import streamlit as st
import torch
from datetime import datetime
from typing import Optional

from config import current_config as config
from logger import setup_logging
from exceptions import (
    AppException,
    ValidationException,
    RateLimitException,
)
from utils import (
    URLValidator,
    APIKeyValidator,
    SimpleCache,
    RateLimiter,
    sanitize_text,
    format_timestamp,
    estimate_reading_time,
)
from services import (
    YouTubeService,
    WebsiteService,
    SummarizationService,
)
from langchain_core.documents import Document

logger = setup_logging(__name__)

# Initialize session state
if "cache" not in st.session_state:
    st.session_state.cache = SimpleCache(ttl_seconds=config.CACHE_TTL_SECONDS)
if "rate_limiter" not in st.session_state:
    st.session_state.rate_limiter = RateLimiter(
        config.RATE_LIMIT_CALLS, config.RATE_LIMIT_PERIOD_SECONDS
    )
if "history" not in st.session_state:
    st.session_state.history = [] if config.ENABLE_HISTORY else None
if "summarization_service" not in st.session_state:
    st.session_state.summarization_service = None


def configure_page():
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title=config.PAGE_TITLE,
        page_icon=config.PAGE_ICON,
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(
        """
        <style>
        .main { padding: 2rem; }
        .stButton > button { width: 100%; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header():
    """Render application header."""
    col1, col2 = st.columns([0.8, 0.2])
    with col1:
        st.title(config.PAGE_TITLE)
        st.markdown("**Transform any content into concise, actionable summaries**")
    with col2:
        device_info = "🚀 GPU" if torch.cuda.is_available() else "💻 CPU"
        st.metric("Device", device_info)


def render_sidebar():
    """Render sidebar with configuration options."""
    with st.sidebar:
        st.header("⚙️ Configuration")

        # API Key
        api_key = st.text_input(
            "🔑 Groq API Key",
            type="password",
            help="Get your API key from https://console.groq.com/",
        )

        # Whisper Model
        whisper_model = st.selectbox(
            "🎙️ Whisper Model (YouTube)",
            config.WHISPER_MODELS,
            index=config.WHISPER_MODELS.index(config.DEFAULT_WHISPER_MODEL),
            help="Larger models are more accurate but slower",
        )

        # Summarization Options
        st.markdown("---")
        st.subheader("📝 Summary Options")

        summary_style = st.selectbox(
            "Style",
            config.SUMMARY_STYLES,
            index=0,
            help="Choose how the summary should be formatted",
        )

        summary_length = st.slider(
            "Length (words)",
            min_value=config.MIN_SUMMARY_LENGTH,
            max_value=config.MAX_SUMMARY_LENGTH,
            value=config.DEFAULT_SUMMARY_LENGTH,
            step=50,
        )

        # Advanced Options
        if config.ENABLE_ADVANCED_OPTIONS:
            st.markdown("---")
            st.subheader("🔬 Advanced Options")
            language = st.selectbox("Content Language", config.SUPPORTED_LANGUAGES)
        else:
            language = config.DEFAULT_LANGUAGE

        return {
            "api_key": api_key,
            "whisper_model": whisper_model,
            "summary_style": summary_style,
            "summary_length": summary_length,
            "language": language,
        }


def validate_inputs(config_dict: dict, url: str) -> tuple[bool, Optional[str]]:
    """
    Validate user inputs.

    Args:
        config_dict: Configuration dictionary from sidebar
        url: URL to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    # Validate API key
    if not config_dict["api_key"].strip():
        return False, "⚠️ Please provide your Groq API key in the sidebar."

    if not APIKeyValidator.validate_groq_key(config_dict["api_key"]):
        return False, "❌ Invalid Groq API key format."

    # Validate URL
    if not url.strip():
        return False, "❌ Please provide a URL."

    if not URLValidator.is_valid_url(url):
        return False, "❌ Please enter a valid URL."

    url_type = URLValidator.get_url_type(url)
    if not url_type:
        return False, "❌ Unsupported URL. Please enter a YouTube or website URL."

    return True, None


def add_to_history(entry: dict) -> None:
    """Add entry to history."""
    if config.ENABLE_HISTORY and st.session_state.history is not None:
        entry["timestamp"] = datetime.now()
        st.session_state.history.append(entry)
        logger.info(f"Added to history: {entry['url'][:50]}")


def render_history():
    """Render summarization history."""
    if config.ENABLE_HISTORY and st.session_state.history:
        with st.expander("📚 History", expanded=False):
            for i, entry in enumerate(reversed(st.session_state.history)):
                col1, col2, col3 = st.columns([0.5, 0.3, 0.2])
                with col1:
                    st.caption(entry["url"][:40] + "...")
                with col2:
                    st.caption(format_timestamp(entry["timestamp"]))
                with col3:
                    if st.button("View", key=f"history_{i}"):
                        st.session_state.selected_history = i


def main():
    """Main application logic."""
    configure_page()
    render_header()

    # Sidebar
    config_dict = render_sidebar()

    # Main content
    st.markdown("---")

    # URL Input
    col1, col2 = st.columns([0.85, 0.15])
    with col1:
        url = st.text_input(
            "Enter URL",
            placeholder="https://www.youtube.com/watch?v=... or https://example.com",
            label_visibility="collapsed",
        )
    with col2:
        st.write("")  # Spacing
        st.write("")  # Spacing

    # Render history
    render_history()

    st.markdown("---")

    # Summarize button
    if st.button(
        "✨ Summarize Content", use_container_width=True, type="primary"
    ):
        # Validate inputs
        is_valid, error_msg = validate_inputs(config_dict, url)
        if not is_valid:
            st.error(error_msg)
            st.stop()

        # Check rate limiting
        if config.ENABLE_RATE_LIMITING:
            try:
                if not st.session_state.rate_limiter.is_allowed():
                    retry_after = st.session_state.rate_limiter.get_retry_after()
                    st.error(
                        f"⏱️ Rate limited. Please wait {retry_after} seconds before trying again."
                    )
                    st.stop()
            except RateLimitException as e:
                st.error(f"⏱️ {e.message}")
                st.stop()

        # Check cache
        cache_key = f"{url}_{config_dict['summary_style']}_{config_dict['summary_length']}"
        cached_result = st.session_state.cache.get(cache_key)

        try:
            with st.spinner("⏳ Processing..."):
                # Device info
                device_type = "GPU" if torch.cuda.is_available() else "CPU"
                st.info(f"🖥️ Using device: {device_type}")

                if cached_result:
                    st.success("✅ Loaded from cache (recent summary)")
                    summary = cached_result
                else:
                    # Initialize summarization service
                    if (
                        st.session_state.summarization_service is None
                        or st.session_state.summarization_service.api_key
                        != config_dict["api_key"]
                    ):
                        st.session_state.summarization_service = SummarizationService(
                            config_dict["api_key"]
                        )

                    service = st.session_state.summarization_service
                    url_type = URLValidator.get_url_type(url)

                    # Process based on URL type
                    if url_type == "youtube":
                        st.info("📺 Downloading and transcribing YouTube video...")
                        transcript = YouTubeService.download_and_transcribe(
                            url, config_dict["whisper_model"]
                        )
                        docs = [Document(page_content=transcript)]
                    else:
                        st.info("🌐 Loading website content...")
                        docs = WebsiteService.load_and_extract(url)

                    # Summarize
                    st.info("🤖 Generating summary...")
                    summary = service.summarize(
                        docs,
                        style=config_dict["summary_style"],
                        length=config_dict["summary_length"],
                    )

                    # Cache result
                    st.session_state.cache.set(cache_key, summary)

                # Display results
                st.success("✅ Summary Generated")

                # Create result container
                result_col1, result_col2 = st.columns([0.75, 0.25])

                with result_col1:
                    st.markdown("### 📄 Summary")
                    st.write(summary)

                with result_col2:
                    st.markdown("### 📊 Statistics")
                    word_count = len(summary.split())
                    reading_time = estimate_reading_time(summary)
                    st.metric("Words", word_count)
                    st.metric("Reading Time", f"{reading_time} min")
                    st.metric("URL Type", url_type.capitalize())

                # Add to history
                add_to_history(
                    {
                        "url": url,
                        "summary": summary,
                        "style": config_dict["summary_style"],
                        "url_type": url_type,
                    }
                )

                # Export options
                if config.ENABLE_EXPORT:
                    st.markdown("---")
                    st.markdown("### 📥 Export Options")

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        if st.button("📋 Copy to Clipboard", use_container_width=True):
                            st.code(summary, language="text")
                            st.success("Copied!")

                    with col2:
                        if st.download_button(
                            "📄 Download as Text",
                            summary,
                            file_name=f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                            mime="text/plain",
                            use_container_width=True,
                        ):
                            pass

                    with col3:
                        if st.button("🔄 New Summary", use_container_width=True):
                            st.rerun()

        except ValidationException as e:
            st.error(f"❌ Input Error: {e.message}")
            logger.warning(f"Validation error: {e.error_code}")
        except RateLimitException as e:
            st.error(f"⏱️ Rate Limit: {e.message}")
            if e.retry_after:
                st.info(f"Please try again in {e.retry_after} seconds")
        except AppException as e:
            st.error(f"❌ Error: {e.message}")
            logger.error(f"Application error: {e.error_code} - {e.message}")
        except Exception as e:
            st.error("🚫 An unexpected error occurred.")
            logger.exception(f"Unexpected error: {str(e)}")
            with st.expander("🔧 Technical Details"):
                st.code(str(e))


if __name__ == "__main__":
    main()


