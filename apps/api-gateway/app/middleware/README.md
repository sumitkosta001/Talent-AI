# Middleware Module (`app/middleware/`)

## Purpose
The `app/middleware/` module provides cross-cutting ASGI middleware components for request/response interception, correlation tracking, security header enforcement, and rate limiting.

## Responsibilities
- **`cors.py`**: Configures cross-origin request policies (`CORSMiddleware`).
- **`logging.py`**: Intercepts HTTP request execution duration and logs status metrics.
- **`authentication.py`**: Attaches parsed user identity state to `request.state`.
- **`rate_limit.py`**: Enforces sliding window request throttling via Redis.
- **`request_id.py`**: Generates and propagates correlation `X-Request-ID` headers for distributed tracing.

## What Belongs Here
- Pure Starlette/FastAPI `BaseHTTPMiddleware` classes intercepting all incoming HTTP traffic.

## What Should NOT Belong Here
- Endpoint specific authorization logic (belongs in `app/dependencies/auth.py`).
- Route handlers or business domain logic.
