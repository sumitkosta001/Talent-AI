# Business Domain Services Module (`app/services/`)

## Purpose
The `app/services/` module implements pure business domain logic, orchestrating repositories, background Celery tasks, and external third-party SDK integrations.

## Responsibilities
- Coordinates multi-step business transactions (e.g. user registration -> hash password -> save record -> send verification email via Resend).
- Interacts with `app/repositories/` for data persistence.
- Triggers AI integration wrappers (`app/integrations/openai.py`, `app/integrations/gemini.py`).

## What Belongs Here
- Pure Python business service classes operating on domain inputs and repository abstractions.

## What Should NOT Belong Here
- FastAPI `Request`, `Response`, or `APIRouter` objects.
- Raw SQL query strings (belong in `app/repositories/`).

## Future Services To Implement
- `auth_service.py`: Authentication, registration, OTP validation, and password resets.
- `user_service.py`: Profile updates, settings management, and account deactivation.
- `job_service.py`: Job posting creation, editing, closing, and candidate search filters.
- `application_service.py`: Application pipeline management and status transitions.
- `resume_service.py`: Document parsing, skill extraction, and ATS match score evaluation.
- `notification_service.py`: Real-time alert dispatch and notification preferences.
