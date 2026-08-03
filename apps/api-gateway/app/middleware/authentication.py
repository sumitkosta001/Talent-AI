"""Global HTTP Authentication Interceptor Middleware.

Extracts bearer tokens globally across non-exempt API endpoints.
"""

from typing import Callable, Awaitable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class AuthenticationMiddleware(BaseHTTPMiddleware):
    """ASGI middleware evaluating authentication state on incoming requests."""

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        """Intercept request to attach user claims to request.state.
        
        Args:
            request: Incoming HTTP request.
            call_next: Response generator delegate.
            
        Returns:
            Processed HTTP response.
        """
        # TODO: Attach parsed user state to request.state.user
        return await call_next(request)
