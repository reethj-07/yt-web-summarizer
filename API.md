# API Documentation

## Overview

Content Summarizer Pro provides a modular architecture with well-designed service classes and utility functions for content processing and summarization.

## Module Reference

### `services.py`

Core services for content processing.

#### YouTubeService

```python
class YouTubeService:
    @staticmethod
    def download_and_transcribe(url: str, whisper_model_size: str = "base") -> str:
        """Download and transcribe YouTube video."""
```

**Parameters:**
- `url` (str): YouTube URL
- `whisper_model_size` (str): Model size (base, small, medium, large)

**Returns:**
- Transcribed text (str)

**Raises:**
- `YouTubeProcessingException`: Download or transcription failed
- `TranscriptionException`: Whisper transcription failed

**Example:**
```python
from services import YouTubeService

transcript = YouTubeService.download_and_transcribe(
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    whisper_model_size="base"
)
print(transcript)
```

#### WebsiteService

```python
class WebsiteService:
    @staticmethod
    def load_and_extract(url: str) -> List[Document]:
        """Load and extract content from website."""
```

**Parameters:**
- `url` (str): Website URL

**Returns:**
- List of LangChain Document objects

**Raises:**
- `WebsiteProcessingException`: Loading or extraction failed

**Example:**
```python
from services import WebsiteService

docs = WebsiteService.load_and_extract("https://example.com")
for doc in docs:
    print(doc.page_content)
```

#### SummarizationService

```python
class SummarizationService:
    def __init__(self, api_key: str):
        """Initialize with Groq API key."""
    
    def summarize(
        self,
        docs: List[Document],
        style: str = "balanced",
        length: int = 300,
    ) -> str:
        """Summarize documents using LLM."""
```

**Parameters:**
- `docs` (List[Document]): LangChain documents
- `style` (str): Summary style (balanced, bullet_points, executive, technical, simplified)
- `length` (int): Target length in words

**Returns:**
- Summary text (str)

**Raises:**
- `SummarizationException`: Summarization failed

**Example:**
```python
from services import SummarizationService
from langchain_core.documents import Document

service = SummarizationService("your_groq_api_key")
docs = [Document(page_content="Your content here...")]
summary = service.summarize(docs, style="executive", length=300)
print(summary)
```

### `utils.py`

Utility functions and helpers.

#### URLValidator

```python
class URLValidator:
    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Check if URL format is valid."""
    
    @staticmethod
    def is_youtube_url(url: str) -> bool:
        """Check if URL is YouTube link."""
    
    @staticmethod
    def is_website_url(url: str) -> bool:
        """Check if URL is website link."""
    
    @staticmethod
    def get_url_type(url: str) -> Optional[str]:
        """Determine URL type (youtube, website, None)."""
```

#### APIKeyValidator

```python
class APIKeyValidator:
    @staticmethod
    def validate_groq_key(api_key: str) -> bool:
        """Validate Groq API key format."""
```

#### SimpleCache

```python
class SimpleCache:
    def __init__(self, ttl_seconds: int = 3600):
        """Initialize cache with TTL."""
    
    def set(self, key: str, value: Any) -> None:
        """Store value in cache."""
    
    def get(self, key: str) -> Optional[Any]:
        """Retrieve value from cache."""
    
    def clear(self) -> None:
        """Clear all cache."""
    
    def get_size(self) -> int:
        """Get number of cached items."""
```

**Example:**
```python
from utils import SimpleCache

cache = SimpleCache(ttl_seconds=3600)
cache.set("key1", "value1")
result = cache.get("key1")  # Returns "value1"
```

#### RateLimiter

```python
class RateLimiter:
    def __init__(self, max_calls: int, period_seconds: int):
        """Initialize rate limiter."""
    
    def is_allowed(self, identifier: str = "default") -> bool:
        """Check if action is allowed."""
    
    def get_retry_after(self, identifier: str = "default") -> int:
        """Get seconds until next call allowed."""
```

**Example:**
```python
from utils import RateLimiter

limiter = RateLimiter(max_calls=10, period_seconds=60)
if limiter.is_allowed():
    # Process request
else:
    retry_after = limiter.get_retry_after()
    print(f"Wait {retry_after} seconds")
```

#### Text Utilities

```python
def sanitize_text(text: str, max_length: Optional[int] = None) -> str:
    """Remove extra whitespace and optionally truncate."""

def estimate_reading_time(text: str, words_per_minute: int = 200) -> int:
    """Estimate reading time in minutes."""

def format_timestamp(dt: Optional[datetime] = None) -> str:
    """Format datetime to string."""
```

### `config.py`

Configuration management.

```python
class Config:
    """Base configuration class with environment variables."""
    
    # API settings
    GROQ_API_KEY: str
    GROQ_MODEL: str = "llama3-8b-8192"
    GROQ_MAX_RETRIES: int = 3
    
    # Summarization
    DEFAULT_SUMMARY_LENGTH: int = 300
    SUMMARY_STYLES: List[str] = [...]
    
    # Caching
    ENABLE_CACHE: bool = True
    CACHE_TTL_SECONDS: int = 3600
    
    # Rate limiting
    ENABLE_RATE_LIMITING: bool = True
    RATE_LIMIT_CALLS: int = 10
    RATE_LIMIT_PERIOD_SECONDS: int = 60
    
    # Features
    ENABLE_HISTORY: bool = True
    ENABLE_EXPORT: bool = True
    ENABLE_ADVANCED_OPTIONS: bool = True
```

### `exceptions.py`

Custom exception hierarchy.

```python
class AppException(Exception):
    """Base application exception."""
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""

class ValidationException(AppException):
    """Input validation error."""

class SummarizationException(AppException):
    """Summarization error."""

class YouTubeProcessingException(AppException):
    """YouTube processing error."""

class WebsiteProcessingException(AppException):
    """Website processing error."""

class RateLimitException(AppException):
    """Rate limiting error."""
```

**Example:**
```python
from exceptions import ValidationException

try:
    # Your code
except ValidationException as e:
    print(f"Error: {e.message}")
    print(f"Details: {e.to_dict()}")
```

### `logger.py`

Logging utilities.

```python
def setup_logging(name: str, level: Optional[str] = None) -> logging.Logger:
    """Set up logging for a module."""
```

**Example:**
```python
from logger import setup_logging

logger = setup_logging(__name__)
logger.info("Application started")
logger.error("An error occurred")
```

## Configuration

### Environment Variables

```env
# API
GROQ_API_KEY=your_key
GROQ_MODEL=llama3-8b-8192

# Features
ENABLE_CACHE=true
ENABLE_RATE_LIMITING=true
ENABLE_HISTORY=true

# Logging
LOG_LEVEL=INFO
```

### Programmatic Configuration

```python
from config import current_config as config

print(config.DEFAULT_SUMMARY_LENGTH)  # 300
print(config.SUMMARY_STYLES)  # ['balanced', ...]
```

## Error Handling

All services raise custom exceptions that can be caught and handled:

```python
from exceptions import (
    YouTubeProcessingException,
    SummarizationException,
    AppException,
)

try:
    transcript = YouTubeService.download_and_transcribe(url)
    docs = [Document(page_content=transcript)]
    summary = service.summarize(docs)
except YouTubeProcessingException as e:
    print(f"YouTube error: {e.message}")
except SummarizationException as e:
    print(f"Summarization error: {e.message}")
except AppException as e:
    print(f"Application error: {e.error_code}")
```

## Performance Tips

1. **Enable Caching**: Reduces API calls by 70%
   ```env
   ENABLE_CACHE=true
   CACHE_TTL_SECONDS=3600
   ```

2. **Use GPU**: 5-10x faster transcription
   ```env
   WHISPER_DEVICE=cuda
   ```

3. **Rate Limiting**: Prevent API overuse
   ```env
   RATE_LIMIT_CALLS=10
   RATE_LIMIT_PERIOD_SECONDS=60
   ```

4. **Smaller Whisper Models**: For faster processing
   ```python
   YouTubeService.download_and_transcribe(url, "base")
   ```

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment guides.

---

For more information, see [PRODUCTION_GUIDE.md](PRODUCTION_GUIDE.md)
