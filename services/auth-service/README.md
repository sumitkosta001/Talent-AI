# Auth Service

This service is a FastAPI-based microservice designed for **Auth Service** management in the TalentAI recruitment system.

## Folder Directory Responsibilities

- **`app/api/`**: Subrouters containing endpoint definitions for the local API.
- **`app/core/`**: Security credentials, core configs, logging settings.
- **`app/config/`**: Service environment variables and external service endpoint config.
- **`app/database/`**: Engine initializations, session makers, migrations metadata.
- **`app/models/`**: SQLAlchemy models representing internal service schema.
- **`app/repositories/`**: Repository pattern files isolating data access queries.
- **`app/schemas/`**: Pydantic input/output schemas.
- **`app/services/`**: Business logic rules, external API connectors, utility drivers.
- **`app/workers/`**: RabbitMQ consumers, background cron, celery task definitions.
- **`app/utils/`**: Helpers, string formatters, parsing tools.
- **`tests/`**: Pytest testing suites.
