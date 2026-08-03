"""Domain Entity Lifecycle Status Definitions."""

from enum import Enum


class JobStatus(str, Enum):
    """Job posting lifecycle status."""

    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    CLOSED = "closed"


class ApplicationStatus(str, Enum):
    """Candidate job application evaluation status."""

    APPLIED = "applied"
    UNDER_REVIEW = "under_review"
    SHORTLISTED = "shortlisted"
    INTERVIEWING = "interviewing"
    OFFERED = "offered"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"
