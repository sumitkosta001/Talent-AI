"""Dashboard Overview Analytics API Router.

Exposes endpoints for aggregated candidate, recruiter, and admin dashboard metrics.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

# Endpoint placeholders (get_candidate_dashboard, get_recruiter_dashboard, get_admin_dashboard)
