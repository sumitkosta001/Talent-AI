"""Production-Ready Structured Logging System Configuration.

Configures console, rotating file, and structured JSON log handlers for application,
error, and HTTP access logs.
"""

import os
import sys
import logging
import logging.config
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Dict, Any
from app.config.settings import settings


# Ensure logs directory exists
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(parents=True, exist_ok=True)

APP_LOG_PATH = LOGS_DIR / "app.log"
ERROR_LOG_PATH = LOGS_DIR / "error.log"
ACCESS_LOG_PATH = LOGS_DIR / "access.log"


class ColoredConsoleFormatter(logging.Formatter):
    """Console formatter adding ANSI color codes for development readability."""

    COLOR_CODES = {
        logging.DEBUG: "\033[36m",     # Cyan
        logging.INFO: "\033[32m",      # Green
        logging.WARNING: "\033[33m",   # Yellow
        logging.ERROR: "\033[31m",     # Red
        logging.CRITICAL: "\033[35m",  # Magenta
    }
    RESET_CODE = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        """Format log record with ANSI color encoding."""
        log_color = self.COLOR_CODES.get(record.levelno, self.RESET_CODE)
        record.levelname = f"{log_color}{record.levelname:<8}{self.RESET_CODE}"
        return super().format(record)


def get_logging_config() -> Dict[str, Any]:
    """Construct dictConfig logger dictionary.
    
    Returns:
        Structured dictionary matching logging.config.dictConfig specification.
    """
    log_level = settings.app.log_level.upper()

    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s [%(levelname)s] %(name)s (%(filename)s:%(lineno)d): %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "colored": {
                "()": ColoredConsoleFormatter,
                "format": "%(asctime)s [%(levelname)s] %(name)s (%(filename)s:%(lineno)d): %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "json": {
                "format": '{"timestamp":"%(asctime)s","level":"%(levelname)s","logger":"%(name)s","file":"%(filename)s","line":%(lineno)d,"message":"%(message)s"}',
                "datefmt": "%Y-%m-%dT%H:%M:%SZ",
            },
            "access": {
                "format": "%(asctime)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": log_level,
                "formatter": "colored" if settings.app.debug else "standard",
                "stream": "ext://sys.stdout",
            },
            "app_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": log_level,
                "formatter": "standard",
                "filename": str(APP_LOG_PATH),
                "maxBytes": 10 * 1024 * 1024,  # 10 MB
                "backupCount": 5,
                "encoding": "utf8",
            },
            "error_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "ERROR",
                "formatter": "standard",
                "filename": str(ERROR_LOG_PATH),
                "maxBytes": 10 * 1024 * 1024,  # 10 MB
                "backupCount": 5,
                "encoding": "utf8",
            },
            "access_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "INFO",
                "formatter": "access",
                "filename": str(ACCESS_LOG_PATH),
                "maxBytes": 10 * 1024 * 1024,  # 10 MB
                "backupCount": 5,
                "encoding": "utf8",
            },
        },
        "loggers": {
            "": {  # Root logger
                "level": log_level,
                "handlers": ["console", "app_file", "error_file"],
            },
            "talentai.access": {
                "level": "INFO",
                "handlers": ["console", "access_file"],
                "propagate": False,
            },
            "uvicorn": {
                "level": "INFO",
                "handlers": ["console", "app_file"],
                "propagate": False,
            },
            "uvicorn.access": {
                "level": "INFO",
                "handlers": ["access_file"],
                "propagate": False,
            },
        },
    }


def setup_logging() -> None:
    """Initialize structured logging config."""
    config = get_logging_config()
    logging.config.dictConfig(config)
    logger = logging.getLogger("talentai.bootstrap")
    logger.info(f"Logging initialized at level {settings.app.log_level} (env: {settings.app.env})")
