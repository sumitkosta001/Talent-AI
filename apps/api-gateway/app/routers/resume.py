"""Resume Upload and AI ATS Score API Router.

Exposes endpoints for PDF/DOCX resume file upload, text extraction, and AI ATS analysis.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/resume", tags=["Resume & ATS"])

# Endpoint placeholders (upload_resume, get_resume_audit, get_ats_score)
