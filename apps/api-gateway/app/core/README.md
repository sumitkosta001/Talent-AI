# Core System Module (`app/core/`)

## Purpose
The `app/core/` module manages fundamental system lifecycle behaviors, global security defaults, and lifespan context handlers for the FastAPI application instance.

## Responsibilities
- **`lifespan.py`**: FastAPI `@asynccontextmanager` managing startup resource allocation (DB engine, Redis client) and shutdown cleanup.
- **`events.py`**: Event callbacks triggered on application start or termination.
- **`security.py`**: Core security policies and token expiration defaults.

## What Belongs Here
- System-wide lifecycle managers, event hooks, and global security policies.

## What Should NOT Belong Here
- Request-level auth dependency injection (belongs in `app/dependencies/auth.py`).
- HTTP router endpoint definitions (belong in `app/routers/`).
