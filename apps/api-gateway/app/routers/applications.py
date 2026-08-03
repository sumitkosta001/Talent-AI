"""Candidate Job Applications API Router.

Exposes endpoints for job application submission, tracking, pipeline stage changes, and feedback.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/applications", tags=["Applications"])

# Endpoint placeholders (apply_for_job, list_candidate_applications, update_application_status)
