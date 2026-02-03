"""
Utility functions for YT Web Summarizer.
Includes validation, caching, and helper functions.
"""

import re
import hashlib
import json
import time
from datetime import datetime
from typing import Optional, Dict, Any, Callable
from functools import wraps
import validators
from logger import setup_logging
from exceptions import (
    ValidationException,
    RateLimitException,
)

logger = setup_logging(__name__)


class URLValidator:
    """URL validation utilities."""

    YOUTUBE_REGEX = r"(https?://)?(www\.)?(youtube\.com|youtu\.be)/"
    SUPPORTED_DOMAINS = ["youtube.com", "youtu.be", "wikipedia.org", "github.com"]

    @staticmethod
    def is_valid_url(url: str) -> bool:
        """
        Validate if URL format is correct.

        Args:
            url: URL string to validate

        Returns:
            True if valid, False otherwise
        """
        if not url or not isinstance(url, str):
            return False
        return validators.url(url) is True

    @staticmethod
    def is_youtube_url(url: str) -> bool:
        """
        Check if URL is a YouTube URL.

        Args:
            url: URL string to check

        Returns:
            True if YouTube URL, False otherwise
        """
        if not URLValidator.is_valid_url(url):
            return False
        return bool(re.match(URLValidator.YOUTUBE_REGEX, url.strip()))

    @staticmethod
    def is_website_url(url: str) -> bool:
        """
        Check if URL is a valid website URL.

        Args:
            url: URL string to check

        Returns:
            True if valid website URL, False otherwise
        """
        if not URLValidator.is_valid_url(url):
            return False
        return not URLValidator.is_youtube_url(url)

    @staticmethod
    def get_url_type(url: str) -> Optional[str]:
        """
        Determine the type of URL.

        Args:
            url: URL string to analyze

        Returns:
            'youtube', 'website', or None
        """
        if URLValidator.is_youtube_url(url):
            return "youtube"
        elif URLValidator.is_website_url(url):
            return "website"
        return None


class APIKeyValidator:
    """API key validation utilities."""

    @staticmethod
    def validate_groq_key(api_key: str) -> bool:
        """
        Validate Groq API key format.

        Args:
            api_key: API key to validate

        Returns:
            True if valid format, False otherwise
        """
        if not api_key:
            return False
        # Groq keys are typically alphanumeric strings
        return len(api_key) >= 10 and api_key.replace("-", "").replace("_", "").isalnum()


class SimpleCache:
    """Simple in-memory cache with TTL support."""

    def __init__(self, ttl_seconds: int = 3600):
        """
        Initialize cache.

        Args:
            ttl_seconds: Time to live for cached items in seconds
        """
        self.ttl_seconds = ttl_seconds
        self._cache: Dict[str, Dict[str, Any]] = {}

    def _get_hash(self, key: str) -> str:
        """Generate hash for cache key."""
        return hashlib.md5(key.encode()).hexdigest()

    def set(self, key: str, value: Any) -> None:
        """
        Store value in cache.

        Args:
            key: Cache key
            value: Value to cache
        """
        hash_key = self._get_hash(key)
        self._cache[hash_key] = {
            "value": value,
            "timestamp": time.time(),
        }
        logger.debug(f"Cache set: {key}")

    def get(self, key: str) -> Optional[Any]:
        """
        Retrieve value from cache.

        Args:
            key: Cache key

        Returns:
            Cached value if exists and not expired, None otherwise
        """
        hash_key = self._get_hash(key)
        if hash_key not in self._cache:
            return None

        cached = self._cache[hash_key]
        if time.time() - cached["timestamp"] > self.ttl_seconds:
            del self._cache[hash_key]
            logger.debug(f"Cache expired: {key}")
            return None

        logger.debug(f"Cache hit: {key}")
        return cached["value"]

    def clear(self) -> None:
        """Clear all cache."""
        self._cache.clear()
        logger.info("Cache cleared")

    def get_size(self) -> int:
        """Get cache size in items."""
        return len(self._cache)


class RateLimiter:
    """Rate limiting utility."""

    def __init__(self, max_calls: int, period_seconds: int):
        """
        Initialize rate limiter.

        Args:
            max_calls: Maximum number of calls allowed
            period_seconds: Time period in seconds
        """
        self.max_calls = max_calls
        self.period_seconds = period_seconds
        self._calls: Dict[str, list] = {}

    def is_allowed(self, identifier: str = "default") -> bool:
        """
        Check if action is allowed under rate limit.

        Args:
            identifier: Unique identifier for rate limiting (e.g., user IP)

        Returns:
            True if allowed, False if rate limited
        """
        now = time.time()
        if identifier not in self._calls:
            self._calls[identifier] = []

        # Remove old calls outside the period
        self._calls[identifier] = [
            call_time
            for call_time in self._calls[identifier]
            if now - call_time < self.period_seconds
        ]

        if len(self._calls[identifier]) < self.max_calls:
            self._calls[identifier].append(now)
            return True

        return False

    def get_retry_after(self, identifier: str = "default") -> int:
        """Get seconds to wait before next call is allowed."""
        if identifier not in self._calls or not self._calls[identifier]:
            return 0
        oldest_call = min(self._calls[identifier])
        retry_after = int(self.period_seconds - (time.time() - oldest_call)) + 1
        return max(0, retry_after)


def rate_limit(max_calls: int, period_seconds: int):
    """
    Decorator for rate limiting function calls.

    Args:
        max_calls: Maximum number of calls allowed
        period_seconds: Time period in seconds
    """
    limiter = RateLimiter(max_calls, period_seconds)

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not limiter.is_allowed():
                retry_after = limiter.get_retry_after()
                raise RateLimitException(
                    f"Rate limit exceeded. Try again in {retry_after} seconds.",
                    retry_after=retry_after,
                )
            return func(*args, **kwargs)

        return wrapper

    return decorator


def sanitize_text(text: str, max_length: Optional[int] = None) -> str:
    """
    Sanitize and clean text.

    Args:
        text: Text to sanitize
        max_length: Maximum length to truncate to

    Returns:
        Sanitized text
    """
    # Remove extra whitespace
    text = " ".join(text.split())

    # Truncate if needed
    if max_length and len(text) > max_length:
        text = text[: max_length - 3] + "..."

    return text


def format_timestamp(dt: Optional[datetime] = None) -> str:
    """
    Format datetime to string.

    Args:
        dt: Datetime object (defaults to now)

    Returns:
        Formatted datetime string
    """
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def estimate_reading_time(text: str, words_per_minute: int = 200) -> int:
    """
    Estimate reading time in minutes.

    Args:
        text: Text to estimate
        words_per_minute: Reading speed assumption

    Returns:
        Estimated minutes to read
    """
    word_count = len(text.split())
    return max(1, word_count // words_per_minute)
