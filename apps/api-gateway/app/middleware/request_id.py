"""Unique Correlation Request ID Middleware.

Attaches UUID X-Request-ID headers to incoming requests and outgoing responses
for distributed tracing.
"""

import uuid
from typing import Callable, Awaitable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class RequestIDMiddleware(BaseHTTPMiddleware):
    """ASGI middleware generating and injecting correlation X-Request-ID headers."""

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        """Inject or propagate X-Request-ID header value.
        
        Args:
            request: Incoming HTTP request.
            call_next: Response generator delegate.
            
        Returns:
            Processed HTTP response with X-Request-ID header attached.
        """
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response
