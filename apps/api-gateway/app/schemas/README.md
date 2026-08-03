# Schemas Module (`app/schemas/`)

## Purpose
The `app/schemas/` module defines request, response, and internal Data Transfer Objects (DTOs) using Pydantic v2 `BaseModel`.

## Responsibilities
- Input validation, string sanitization, and type coercion.
- OpenAPI schema generation and example payload declarations.
- Outbound API response serialization (`ConfigDict(from_attributes=True)`).

## What Belongs Here
- Pydantic v2 `BaseModel` classes, `Field()` constraints, and custom `@field_validator` methods.

## What Should NOT Belong Here
- SQLAlchemy 2.0 database model definitions (belong in `app/models/`).
- Direct SQL execution or ORM database session references.

## Future Schema Definitions To Implement
- `auth.py`: `LoginRequest`, `RegisterRequest`, `TokenResponse`, `OTPVerifyRequest`.
- `user.py`: `UserProfileResponse`, `UserUpdateRequest`, `UserRoleChangeRequest`.
- `job.py`: `JobCreateRequest`, `JobUpdateRequest`, `JobResponse`, `JobListResponse`.
- `application.py`: `ApplicationCreateRequest`, `ApplicationStatusUpdate`, `ApplicationResponse`.
- `resume.py`: `ResumeUploadResponse`, `ATSScoreResponse`, `SkillBreakdownResponse`.
