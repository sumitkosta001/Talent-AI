# Constants Module (`app/constants/`)

## Purpose
The `app/constants/` module provides centralized, immutable enumerations, default boundary limits, and standardized response strings used across transport, service, and database layers.

## Responsibilities
- **Role Enums**: Defines `UserRole` (`candidate`, `recruiter`, `admin`).
- **Permission Scopes**: Standardizes OAuth2/RBAC scope identifiers.
- **Entity Lifecycles**: Enumerates state transitions for `JobStatus` and `ApplicationStatus`.
- **System Boundaries**: Specifies pagination maximums, file upload limits, and allowed file formats.

## What Belongs Here
- Pure Python `Enum` classes, immutable string constants, and static application boundaries.

## What Should NOT Belong Here
- Dynamic environment settings loaded from `.env` files (belong in `app/config/settings.py`).
- Pydantic DTO validation logic (belongs in `app/schemas/`).
