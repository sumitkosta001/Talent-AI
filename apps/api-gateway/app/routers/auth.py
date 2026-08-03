"""Authentication API Router.

Exposes endpoints for registration, login, token refresh, password resets, 2FA, and OAuth.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Endpoint placeholders (login, register, verify-email, send-otp, verify-otp, 2fa)
