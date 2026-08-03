"""Fine-Grained Authorization Permission Scopes."""

from enum import Enum


class PermissionScope(str, Enum):
    """Fine-grained permission scopes for RBAC/ABAC enforcement."""

    JOBS_READ = "jobs:read"
    JOBS_WRITE = "jobs:write"
    APPLICATIONS_READ = "applications:read"
    APPLICATIONS_WRITE = "applications:write"
    RESUME_AUDIT = "resume:audit"
    USERS_MANAGE = "users:manage"
    SYSTEM_DIAGNOSTICS = "system:diagnostics"
