"""
Unit tests for YT Web Summarizer utilities and services.
"""

import pytest
from utils import (
    URLValidator,
    APIKeyValidator,
    SimpleCache,
    RateLimiter,
    sanitize_text,
    estimate_reading_time,
)
from exceptions import ValidationException, RateLimitException
import time


class TestURLValidator:
    """Test URL validation utilities."""

    def test_valid_url(self):
        """Test valid URL detection."""
        assert URLValidator.is_valid_url("https://www.youtube.com/watch?v=123")
        assert URLValidator.is_valid_url("https://example.com")
        assert URLValidator.is_valid_url("https://en.wikipedia.org")

    def test_invalid_url(self):
        """Test invalid URL detection."""
        assert not URLValidator.is_valid_url("")
        assert not URLValidator.is_valid_url("not a url")
        assert not URLValidator.is_valid_url(None)

    def test_youtube_url(self):
        """Test YouTube URL detection."""
        assert URLValidator.is_youtube_url("https://www.youtube.com/watch?v=123")
        assert URLValidator.is_youtube_url("https://youtu.be/123")
        assert not URLValidator.is_youtube_url("https://example.com")

    def test_website_url(self):
        """Test website URL detection."""
        assert URLValidator.is_website_url("https://example.com")
        assert URLValidator.is_website_url("https://en.wikipedia.org")
        assert not URLValidator.is_website_url("https://www.youtube.com/watch?v=123")

    def test_url_type_detection(self):
        """Test URL type detection."""
        assert URLValidator.get_url_type("https://www.youtube.com/watch?v=123") == "youtube"
        assert URLValidator.get_url_type("https://example.com") == "website"
        assert URLValidator.get_url_type("invalid") is None


class TestAPIKeyValidator:
    """Test API key validation utilities."""

    def test_valid_groq_key(self):
        """Test valid Groq API key detection."""
        assert APIKeyValidator.validate_groq_key("valid_groq_key_12345")
        assert APIKeyValidator.validate_groq_key("abcd1234-efgh-5678-ijkl")

    def test_invalid_groq_key(self):
        """Test invalid Groq API key detection."""
        assert not APIKeyValidator.validate_groq_key("")
        assert not APIKeyValidator.validate_groq_key("short")
        assert not APIKeyValidator.validate_groq_key(None)


class TestSimpleCache:
    """Test simple caching utilities."""

    def test_cache_set_and_get(self):
        """Test basic cache operations."""
        cache = SimpleCache(ttl_seconds=3600)
        cache.set("test_key", "test_value")
        assert cache.get("test_key") == "test_value"

    def test_cache_expiration(self):
        """Test cache TTL expiration."""
        cache = SimpleCache(ttl_seconds=1)
        cache.set("test_key", "test_value")
        time.sleep(1.5)
        assert cache.get("test_key") is None

    def test_cache_miss(self):
        """Test cache miss."""
        cache = SimpleCache()
        assert cache.get("nonexistent") is None

    def test_cache_clear(self):
        """Test cache clearing."""
        cache = SimpleCache()
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        assert cache.get_size() == 2
        cache.clear()
        assert cache.get_size() == 0


class TestRateLimiter:
    """Test rate limiting utilities."""

    def test_rate_limit_allowed(self):
        """Test rate limiting allows calls within limit."""
        limiter = RateLimiter(max_calls=3, period_seconds=60)
        assert limiter.is_allowed()
        assert limiter.is_allowed()
        assert limiter.is_allowed()

    def test_rate_limit_exceeded(self):
        """Test rate limiting blocks calls exceeding limit."""
        limiter = RateLimiter(max_calls=2, period_seconds=60)
        assert limiter.is_allowed()
        assert limiter.is_allowed()
        assert not limiter.is_allowed()

    def test_rate_limit_reset(self):
        """Test rate limit resets after period."""
        limiter = RateLimiter(max_calls=1, period_seconds=1)
        assert limiter.is_allowed()
        assert not limiter.is_allowed()
        time.sleep(1.1)
        assert limiter.is_allowed()

    def test_rate_limit_retry_after(self):
        """Test retry_after calculation."""
        limiter = RateLimiter(max_calls=1, period_seconds=5)
        limiter.is_allowed()
        assert not limiter.is_allowed()
        retry_after = limiter.get_retry_after()
        assert retry_after > 0
        assert retry_after <= 5


class TestTextUtilities:
    """Test text utility functions."""

    def test_sanitize_text(self):
        """Test text sanitization."""
        text = "  This   has   extra   spaces  "
        sanitized = sanitize_text(text)
        assert sanitized == "This has extra spaces"

    def test_sanitize_text_truncation(self):
        """Test text truncation."""
        text = "This is a long text that should be truncated"
        sanitized = sanitize_text(text, max_length=10)
        assert len(sanitized) == 10
        assert sanitized.endswith("...")

    def test_estimate_reading_time(self):
        """Test reading time estimation."""
        # Assuming 200 words per minute
        text = " ".join(["word"] * 200)  # 200 words
        reading_time = estimate_reading_time(text)
        assert reading_time == 1

        text = " ".join(["word"] * 400)  # 400 words
        reading_time = estimate_reading_time(text)
        assert reading_time == 2


class TestExceptions:
    """Test custom exception classes."""

    def test_exception_to_dict(self):
        """Test exception conversion to dict."""
        exc = ValidationException("Test error", field="test_field")
        exc_dict = exc.to_dict()
        assert exc_dict["error_code"] == "VALIDATION_ERROR"
        assert exc_dict["message"] == "Test error"
        assert exc_dict["details"]["field"] == "test_field"

    def test_rate_limit_exception(self):
        """Test rate limit exception."""
        exc = RateLimitException("Rate limited", retry_after=30)
        assert exc.retry_after == 30


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=.", "--cov-report=html"])
