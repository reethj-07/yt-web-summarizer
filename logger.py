"""
Logging configuration and utilities for YT Web Summarizer.
"""

import logging
import os
from typing import Optional
from config import current_config as config


class LogFormatter(logging.Formatter):
    """Custom log formatter with colors and enhanced formatting."""

    COLORS = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[41m",  # Red background
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        """Format log record with color and additional info."""
        level_name = record.levelname
        color = self.COLORS.get(level_name, self.RESET)

        # Enhanced formatting
        log_message = (
            f"{color}[{record.levelname}]{self.RESET} "
            f"{record.name}:{record.lineno} - {record.getMessage()}"
        )

        if record.exc_info:
            log_message += f"\n{self.formatException(record.exc_info)}"

        return log_message


def setup_logging(name: str, level: Optional[str] = None) -> logging.Logger:
    """
    Set up logging for a module.

    Args:
        name: Logger name (usually __name__)
        level: Log level (defaults to config.LOG_LEVEL)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    level_str = level or config.LOG_LEVEL
    logger.setLevel(getattr(logging, level_str))

    # Console handler
    if not logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(LogFormatter())
        logger.addHandler(console_handler)

        # File handler if enabled
        if config.ENABLE_FILE_LOGGING:
            os.makedirs(os.path.dirname(config.LOG_FILE) or ".", exist_ok=True)
            file_handler = logging.FileHandler(config.LOG_FILE)
            file_handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                )
            )
            logger.addHandler(file_handler)

    return logger


# Create module-level logger
logger = setup_logging(__name__)
