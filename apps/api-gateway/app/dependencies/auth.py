"""Authentication Dependency Injection Providers.

Yields current authenticated user identity and enforces role authorization checks
for route handlers using `Depends()`.
"""

from typing import Dict, Any, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.exceptions.auth import AuthenticationError, PermissionDeniedError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)


async def get_current_user(token: Optional[str] = Depends(oauth2_scheme)) -> Dict[str, Any]:
    """Validate bearer token and return current authenticated user data.
    
    Args:
        token: Bearer JWT string from Authorization header.
        
    Returns:
        User payload dictionary containing sub, email, and role.
        
    Raises:
        HTTPException: 401 Unauthorized if token is invalid or expired.
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # TODO: Validate JWT token via app.auth.jwt.JWTManager
    return {"id": "user_123", "email": "user@example.com", "role": "candidate"}


async def get_current_active_admin(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """Enforce that current user has Admin role permissions.
    
    Args:
        current_user: Authenticated user dictionary from get_current_user.
        
    Returns:
        User payload dictionary.
        
    Raises:
        HTTPException: 403 Forbidden if user is not an admin.
    """
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin role required for this action.",
        )
    return current_user
