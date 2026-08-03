"""API v1 Master Router Aggregator.

Assembles all domain sub-routers (auth, users, jobs, companies, applications,
resume, notifications, dashboard) under `/api/v1` prefix.
"""

from fastapi import APIRouter
from app.routers import (
    auth,
    users,
    jobs,
    companies,
    applications,
    resume,
    notifications,
    dashboard,
)

api_v1_router = APIRouter(prefix="/v1")

# Include domain routers
api_v1_router.include_router(auth.router)
api_v1_router.include_router(users.router)
api_v1_router.include_router(jobs.router)
api_v1_router.include_router(companies.router)
api_v1_router.include_router(applications.router)
api_v1_router.include_router(resume.router)
api_v1_router.include_router(notifications.router)
api_v1_router.include_router(dashboard.router)
