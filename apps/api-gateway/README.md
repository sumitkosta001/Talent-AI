# API Gateway

The API Gateway is the single entry point for all client requests. It routes calls to specific backend microservices, performs rate limiting, authenticates token signatures, and handles CORS configurations.

## Responsibilities
- **`app/api/`**: Main endpoint routers mapping client-facing actions.
- **`app/core/`**: Security settings, JWT validation, and application core logic.
- **`app/config/`**: Configuration parsing for routing maps and host addresses.
- **`app/middleware/`**: Cross-cutting concerns like logging, timing, and security headers.
- **`app/dependencies/`**: Dependency injection for authorization guards and HTTP clients.
- **`app/routers/`**: Subrouters mapped to individual microservice proxies.
- **`app/schemas/`**: Pydantic validation schemas.
- **`app/services/`**: Proxy handlers communicating with downstream microservices.
- **`app/database/`**: Config if Gateway needs persistent key-value store access (e.g. Redis).
- **`app/utils/`**: Utilities for network requests, mapping, and headers.
