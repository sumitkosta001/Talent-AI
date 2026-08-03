"""Enterprise Application Configuration System.

Provides modular Pydantic v2 BaseSettings domain classes reading directly from .env.development
with type validation, default fallback values, and a unified container instance.
"""


from pathlib import Path
from typing import Optional, Dict, Any
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import make_url

# Locate .env files using absolute path relative to apps/api-gateway
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = BASE_DIR / ".env"
ENV_DEV_FILE = BASE_DIR / ".env.development"


class BaseAppSettings(BaseSettings):
    """Base settings configuration enabling absolute path .env loading."""

    model_config = SettingsConfigDict(
        env_file=(str(ENV_FILE), str(ENV_DEV_FILE)),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


class ApplicationSettings(BaseAppSettings):
    """Application metadata and core operational settings."""

    app_name: str = Field("TalentAI API Gateway", validation_alias="APP_NAME")
    app_env: str = Field("development", validation_alias="APP_ENV")
    app_version: str = Field("0.1.0", validation_alias="APP_VERSION")
    debug: bool = Field(True, validation_alias="DEBUG")
    secret_key: str = Field(
        "dev_secret_key_super_secret_1234567890_talentai",
        validation_alias="SECRET_KEY",
    )
    timezone: str = Field("UTC", validation_alias="TIMEZONE")
    log_level: str = Field("INFO", validation_alias="LOG_LEVEL")
    docs_url: Optional[str] = Field("/docs", validation_alias="DOCS_URL")
    redoc_url: Optional[str] = Field("/redoc", validation_alias="REDOC_URL")
    openapi_url: Optional[str] = Field("/openapi.json", validation_alias="OPENAPI_URL")
    contact_name: str = Field("TalentAI Team", validation_alias="CONTACT_NAME")
    contact_email: str = Field("support@talentai.com", validation_alias="CONTACT_EMAIL")
    license_name: str = Field("MIT", validation_alias="LICENSE_NAME")

    @property
    def name(self) -> str:
        """Property alias for app_name compatibility."""
        return self.app_name

    @property
    def env(self) -> str:
        """Property alias for app_env compatibility."""
        return self.app_env

    @property
    def version(self) -> str:
        """Property alias for app_version compatibility."""
        return self.app_version


class ServerSettings(BaseAppSettings):
    """HTTP web server and networking configuration settings."""

    host: str = Field("0.0.0.0", validation_alias="HOST")
    port: int = Field(8000, validation_alias="PORT")
    api_prefix: str = Field("/api/v1", validation_alias="API_PREFIX")
    allowed_hosts_str: str = Field(
        "http://localhost:3000,http://127.0.0.1:3000",
        validation_alias="ALLOWED_HOSTS",
    )
    workers: int = Field(1, validation_alias="WORKERS")
    reload: bool = Field(True, validation_alias="RELOAD")
    trusted_hosts_str: str = Field("*", validation_alias="TRUSTED_HOSTS")
    proxy_headers: bool = Field(True, validation_alias="PROXY_HEADERS")

    @property
    def allowed_hosts(self) -> list[str]:
        """Convert comma-separated allowed hosts string into a Python list."""
        if not self.allowed_hosts_str:
            return ["*"]
        return [h.strip() for h in self.allowed_hosts_str.split(",") if h.strip()]

    @property
    def trusted_hosts(self) -> list[str]:
        """Convert comma-separated trusted hosts string into a Python list."""
        if not self.trusted_hosts_str:
            return ["*"]
        return [h.strip() for h in self.trusted_hosts_str.split(",") if h.strip()]


class DatabaseSettings(BaseAppSettings):
    """PostgreSQL async database connection settings."""

    url: str = Field(..., validation_alias="DATABASE_URL")
    echo: bool = Field(False, validation_alias="DATABASE_ECHO")
    pool_size: int = Field(5, validation_alias="DATABASE_POOL_SIZE")
    max_overflow: int = Field(10, validation_alias="DATABASE_MAX_OVERFLOW")
    pool_timeout: int = Field(30, validation_alias="DATABASE_POOL_TIMEOUT")
    pool_recycle: int = Field(1800, validation_alias="DATABASE_POOL_RECYCLE")
    pool_pre_ping: bool = Field(True, validation_alias="DATABASE_POOL_PRE_PING")
    connect_timeout: int = Field(10, validation_alias="DATABASE_CONNECT_TIMEOUT")

    @field_validator("url")
    @classmethod
    def validate_postgresql_url(cls, v: str) -> str:
        """Validate PostgreSQL connection URL."""
        if not v.startswith("postgresql+asyncpg://") and not v.startswith("postgresql://"):
            raise ValueError(
                "DATABASE_URL must start with 'postgresql+asyncpg://' or 'postgresql://'"
            )

        if "sqlite" in v.lower():
            raise ValueError(
                "SQLite is not supported. Use PostgreSQL."
            )

        return v

    @property
    def connection_info(self) -> Dict[str, Any]:
        """Parse non-sensitive connection details for safe logging."""
        parsed = make_url(self.url)
        return {
            "driver": parsed.drivername or "unknown",
            "host": parsed.host or "unknown",
            "port": parsed.port or 5432,
            "database_name": parsed.database or "unknown",
            "username": parsed.username or "unknown",
        }


class RedisSettings(BaseAppSettings):
    """Redis in-memory caching and session broker settings."""

    url: str = Field("redis://localhost:6379/0", validation_alias="REDIS_URL")
    db: int = Field(0, validation_alias="REDIS_DB")
    decode_responses: bool = Field(True, validation_alias="REDIS_DECODE_RESPONSES")


class JWTSettings(BaseAppSettings):
    """JWT token generation, signature, and expiration settings."""

    secret: str = Field("dev_jwt_secret_key_12345", validation_alias="JWT_SECRET")
    algorithm: str = Field("HS256", validation_alias="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(60, validation_alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_days: int = Field(7, validation_alias="REFRESH_TOKEN_EXPIRE_DAYS")
    issuer: str = Field("talentai-api", validation_alias="JWT_ISSUER")
    audience: str = Field("talentai-app", validation_alias="JWT_AUDIENCE")
    clock_skew_seconds: int = Field(0, validation_alias="CLOCK_SKEW_SECONDS")


class OAuthSettings(BaseAppSettings):
    """Social OAuth identity provider client credential settings."""

    google_client_id: Optional[str] = Field(None, validation_alias="GOOGLE_CLIENT_ID")
    google_client_secret: Optional[str] = Field(None, validation_alias="GOOGLE_CLIENT_SECRET")
    github_client_id: Optional[str] = Field(None, validation_alias="GITHUB_CLIENT_ID")
    github_client_secret: Optional[str] = Field(None, validation_alias="GITHUB_CLIENT_SECRET")
    linkedin_client_id: Optional[str] = Field(None, validation_alias="LINKEDIN_CLIENT_ID")
    linkedin_client_secret: Optional[str] = Field(None, validation_alias="LINKEDIN_CLIENT_SECRET")


class EmailSettings(BaseAppSettings):
    """Resend and SMTP transactional email delivery settings."""

    resend_api_key: Optional[str] = Field(None, validation_alias="RESEND_API_KEY")
    smtp_host: str = Field("smtp.resend.com", validation_alias="SMTP_HOST")
    smtp_port: int = Field(587, validation_alias="SMTP_PORT")
    smtp_user: Optional[str] = Field(None, validation_alias="SMTP_USER")
    smtp_password: Optional[str] = Field(None, validation_alias="SMTP_PASSWORD")
    email_from: str = Field("TalentAI <no-reply@talentai.com>", validation_alias="EMAIL_FROM")


class CloudinarySettings(BaseAppSettings):
    """Cloudinary media storage SDK configuration settings."""

    cloud_name: Optional[str] = Field(None, validation_alias="CLOUDINARY_CLOUD_NAME")
    api_key: Optional[str] = Field(None, validation_alias="CLOUDINARY_API_KEY")
    api_secret: Optional[str] = Field(None, validation_alias="CLOUDINARY_API_SECRET")


class AISettings(BaseAppSettings):
    """External AI model API integration settings."""

    openai_api_key: Optional[str] = Field(None, validation_alias="OPENAI_API_KEY")
    gemini_api_key: Optional[str] = Field(None, validation_alias="GEMINI_API_KEY")
    huggingface_api_key: Optional[str] = Field(None, validation_alias="HUGGINGFACE_API_KEY")
    default_ai_provider: str = Field("openai", validation_alias="DEFAULT_AI_PROVIDER")
    default_temperature: float = Field(0.7, validation_alias="DEFAULT_TEMPERATURE")
    default_max_tokens: int = Field(2048, validation_alias="DEFAULT_MAX_TOKENS")


class MonitoringSettings(BaseAppSettings):
    """Sentry application performance and error monitoring settings."""

    sentry_dsn: Optional[str] = Field(None, validation_alias="SENTRY_DSN")


class CelerySettings(BaseAppSettings):
    """Celery background worker queue configuration settings."""

    broker_url: str = Field("redis://localhost:6379/1", validation_alias="CELERY_BROKER_URL")
    result_backend: str = Field("redis://localhost:6379/2", validation_alias="CELERY_RESULT_BACKEND")


class Settings:
    """Master Application Configuration Container."""

    app = ApplicationSettings()
    server = ServerSettings()
    database = DatabaseSettings()
    redis = RedisSettings()
    jwt = JWTSettings()
    oauth = OAuthSettings()
    email = EmailSettings()
    cloudinary = CloudinarySettings()
    ai = AISettings()
    monitoring = MonitoringSettings()
    celery = CelerySettings()


settings = Settings()
