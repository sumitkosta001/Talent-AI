"""API v1 Master Router Aggregator.

Assembles all domain sub-routers under `/api/v1` prefix.
"""

from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.candidates.router import router as candidates_router

api_v1_router = APIRouter(prefix="/v1")

# Include Authentication Router
api_v1_router.include_router(auth_router)

# Include Candidate Profile Router
api_v1_router.include_router(candidates_router)

