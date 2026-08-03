"""User Account Role Enum Definitions."""

from enum import Enum


class UserRole(str, Enum):
    """User account classification roles."""

    CANDIDATE = "candidate"
    RECRUITER = "recruiter"
    ADMIN = "admin"
