"""HTTP Request and Response Access Logging Middleware.

Logs execution duration, status codes, client IPs, and path metrics for audit trails.
"""

import time
import logging
from typing import Callable, Awaitable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("talentai.access")


class LoggingMiddleware(BaseHTTPMiddleware):
    """ASGI middleware for logging request lifecycle metrics."""

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        """Intercept and log request execution duration, status, client IP, and request ID.
        
        Args:
            request: Incoming HTTP Request instance.
            call_next: Next request processing delegate.
            
        Returns:
            Processed HTTP Response instance.
        """
        start_time = time.perf_counter()
        request_id = getattr(request.state, "request_id", "N/A")
        client_ip = request.client.host if request.client else "unknown"

        response = await call_next(request)

        process_time_ms = (time.perf_counter() - start_time) * 1000
        response.headers["X-Process-Time-MS"] = f"{process_time_ms:.2f}"

        logger.info(
            f"[{request_id}] {client_ip} - \"{request.method} {request.url.path}\" {response.status_code} - {process_time_ms:.2f}ms"
        )
        return response
