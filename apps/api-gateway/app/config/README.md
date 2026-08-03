# Application Configuration Module (`app/config/`)

## Purpose
The `app/config/` module handles environment variable parsing, runtime configuration validation, and structured logging initialization.

## Responsibilities
- **`settings.py`**: Pydantic Settings v2 configuration container reading from `.env` files.
- **`logging.py`**: Structured JSON logging formatters and logger setup.
- **`environment.py`**: Runtime environment stage identification (`development`, `staging`, `production`).

## What Belongs Here
- Global application settings, third-party API endpoint URLs, and logging formatters.

## What Should NOT Belong Here
- Static domain enum constants (belong in `app/constants/`).
- Hardcoded secrets or committed credentials.
