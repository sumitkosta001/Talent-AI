"""Environment Identifier Enumeration and Helper Functions.

Provides helper predicates to inspect active runtime environment stages.
"""

from enum import Enum
from app.config.settings import settings


class EnvironmentOption(str, Enum):
    """Runtime environment options."""

    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"


def get_environment() -> str:
    """Return active environment string identifier.
    
    Returns:
        Lower-case environment stage string (e.g. 'development', 'production').
    """
    return settings.app.env.lower()


def is_dev() -> bool:
    """Check if current environment is development.
    
    Returns:
        True if APP_ENV is 'development', False otherwise.
    """
    return get_environment() in (EnvironmentOption.DEVELOPMENT.value, "dev")


def is_prod() -> bool:
    """Check if current environment is production.
    
    Returns:
        True if APP_ENV is 'production', False otherwise.
    """
    return get_environment() in (EnvironmentOption.PRODUCTION.value, "prod")


def is_test() -> bool:
    """Check if current environment is testing.
    
    Returns:
        True if APP_ENV is 'testing', False otherwise.
    """
    return get_environment() in (EnvironmentOption.TESTING.value, "test")
