"""
Custom exceptions and error handling for YT Web Summarizer.
"""

from typing import Optional


class AppException(Exception):
    """Base exception for the application."""

    def __init__(
        self, message: str, error_code: str = "UNKNOWN_ERROR", details: Optional[dict] = None
    ):
        """
        Initialize AppException.

        Args:
            message: User-friendly error message
            error_code: Machine-readable error code
            details: Additional error details for debugging
        """
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)

    def to_dict(self) -> dict:
        """Convert exception to dictionary format."""
        return {
            "error_code": self.error_code,
            "message": self.message,
            "details": self.details,
        }


class APIException(AppException):
    """Exception for API-related errors."""

    def __init__(self, message: str, status_code: Optional[int] = None, **kwargs):
        """Initialize APIException."""
        super().__init__(message, "API_ERROR", **kwargs)
        self.status_code = status_code


class GroqAPIException(APIException):
    """Exception for Groq API errors."""

    def __init__(self, message: str, **kwargs):
        """Initialize GroqAPIException."""
        super().__init__(message, error_code="GROQ_API_ERROR", **kwargs)


class YouTubeProcessingException(AppException):
    """Exception for YouTube processing errors."""

    def __init__(self, message: str, **kwargs):
        """Initialize YouTubeProcessingException."""
        super().__init__(message, "YOUTUBE_ERROR", **kwargs)


class WebsiteProcessingException(AppException):
    """Exception for website processing errors."""

    def __init__(self, message: str, **kwargs):
        """Initialize WebsiteProcessingException."""
        super().__init__(message, "WEBSITE_ERROR", **kwargs)


class TranscriptionException(AppException):
    """Exception for audio transcription errors."""

    def __init__(self, message: str, **kwargs):
        """Initialize TranscriptionException."""
        super().__init__(message, "TRANSCRIPTION_ERROR", **kwargs)


class SummarizationException(AppException):
    """Exception for summarization errors."""

    def __init__(self, message: str, **kwargs):
        """Initialize SummarizationException."""
        super().__init__(message, "SUMMARIZATION_ERROR", **kwargs)


class ValidationException(AppException):
    """Exception for input validation errors."""

    def __init__(self, message: str, field: Optional[str] = None, **kwargs):
        """Initialize ValidationException."""
        details = kwargs.pop("details", {})
        if field:
            details["field"] = field
        super().__init__(message, "VALIDATION_ERROR", details=details, **kwargs)


class ConfigurationException(AppException):
    """Exception for configuration errors."""

    def __init__(self, message: str, **kwargs):
        """Initialize ConfigurationException."""
        super().__init__(message, "CONFIG_ERROR", **kwargs)


class RateLimitException(AppException):
    """Exception for rate limiting."""

    def __init__(self, message: str, retry_after: Optional[int] = None, **kwargs):
        """Initialize RateLimitException."""
        details = kwargs.pop("details", {})
        if retry_after:
            details["retry_after"] = retry_after
        super().__init__(message, "RATE_LIMIT_ERROR", details=details, **kwargs)
        self.retry_after = retry_after
