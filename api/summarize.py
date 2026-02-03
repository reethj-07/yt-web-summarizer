"""
FastAPI backend for Vercel deployment.
Handles content summarization via REST API.
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from config import current_config as config
from services import YouTubeService, WebsiteService, SummarizationService
from utils import URLValidator, APIKeyValidator
from exceptions import AppException
from logger import setup_logging

logger = setup_logging(__name__)

app = FastAPI(title="Content Summarizer API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SummarizeRequest(BaseModel):
    """Request model for summarization."""
    url: str
    api_key: str
    style: str = "balanced"
    length: int = 300
    whisper_model: str = "base"


class SummarizeResponse(BaseModel):
    """Response model for summarization."""
    summary: str
    url_type: str
    word_count: int
    reading_time: int
    status: str = "success"


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok", "service": "content-summarizer"}


@app.post("/summarize", response_model=SummarizeResponse)
async def summarize(request: SummarizeRequest):
    """
    Summarize content from URL.
    
    Args:
        request: SummarizeRequest with URL, API key, and options
        
    Returns:
        SummarizeResponse with summary and metadata
    """
    try:
        # Validate inputs
        if not request.url.strip():
            raise HTTPException(status_code=400, detail="URL is required")
        
        if not request.api_key.strip():
            raise HTTPException(status_code=400, detail="API key is required")
        
        if not URLValidator.is_valid_url(request.url):
            raise HTTPException(status_code=400, detail="Invalid URL format")
        
        if not APIKeyValidator.validate_groq_key(request.api_key):
            raise HTTPException(status_code=400, detail="Invalid API key format")
        
        url_type = URLValidator.get_url_type(request.url)
        if not url_type:
            raise HTTPException(status_code=400, detail="Unsupported URL type")
        
        logger.info(f"Processing {url_type} URL: {request.url[:50]}")
        
        # Initialize service
        service = SummarizationService(request.api_key)
        
        # Process based on URL type
        if url_type == "youtube":
            logger.info("Downloading and transcribing YouTube video...")
            transcript = YouTubeService.download_and_transcribe(
                request.url, 
                request.whisper_model
            )
            from langchain_core.documents import Document
            docs = [Document(page_content=transcript)]
        else:
            logger.info("Loading website content...")
            docs = WebsiteService.load_and_extract(request.url)
        
        # Generate summary
        logger.info(f"Generating {request.style} summary...")
        summary = service.summarize(
            docs,
            style=request.style,
            length=request.length
        )
        
        # Calculate metrics
        word_count = len(summary.split())
        reading_time = max(1, word_count // 200)
        
        logger.info(f"Successfully summarized: {word_count} words")
        
        return SummarizeResponse(
            summary=summary,
            url_type=url_type,
            word_count=word_count,
            reading_time=reading_time,
            status="success"
        )
    
    except HTTPException:
        raise
    except AppException as e:
        logger.error(f"Application error: {e.error_code} - {e.message}")
        raise HTTPException(status_code=422, detail=e.message)
    except Exception as e:
        logger.exception(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/styles")
async def get_styles():
    """Get available summary styles."""
    return {"styles": config.SUMMARY_STYLES}


@app.get("/config")
async def get_config():
    """Get app configuration."""
    return {
        "max_summary_length": config.MAX_SUMMARY_LENGTH,
        "min_summary_length": config.MIN_SUMMARY_LENGTH,
        "default_summary_length": config.DEFAULT_SUMMARY_LENGTH,
        "whisper_models": config.WHISPER_MODELS,
        "summary_styles": config.SUMMARY_STYLES,
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
