# Repositories Module (`app/repositories/`)

## Purpose
The `app/repositories/` module implements the Repository pattern to encapsulate data access and persistence logic, decoupling business domain services from underlying SQLAlchemy ORM details.

## Responsibilities
- Executes async CRUD operations (`get_by_id`, `filter`, `create`, `update`, `delete`).
- Handles complex JOINs, full-text search queries, and database pagination.
- Abstracts raw database queries away from business domain services.

## What Belongs Here
- Asynchronous repository classes accepting an `AsyncSession` dependency.

## What Should NOT Belong Here
- HTTP exception handling (belongs in `app/services/` or `app/routers/`).
- FastAPI `Request` or `Response` objects.
- Business validation rules (belong in `app/services/`).

## Future Repositories To Implement
- `base.py`: Generic `BaseRepository[T]` providing standard CRUD query methods.
- `user.py`: `UserRepository` handling user lookup by email, OAuth provider IDs, and role filtering.
- `job.py`: `JobRepository` handling full-text PostgreSQL search, filter by salary/tags, and recruiter job listings.
- `application.py`: `ApplicationRepository` handling candidate application status updates and stage tracking.
- `resume.py`: `ResumeRepository` handling parsed resume persistence and ATS evaluation history.
