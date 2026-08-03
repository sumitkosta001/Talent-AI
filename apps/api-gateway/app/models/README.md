# Models Module (`app/models/`)

## Purpose
The `app/models/` module houses all database entity declarations using SQLAlchemy 2.0 ORM (`Mapped` and `mapped_column` type annotations).

## Responsibilities
- Defines table schemas, primary keys, foreign key constraints, indexes, and relationships.
- Serves as the single source of truth for Alembic database migrations.

## What Belongs Here
- SQLAlchemy 2.0 classes deriving from `app.database.base.Base`.

## What Should NOT Belong Here
- Pydantic DTO schemas (belong in `app/schemas/`).
- Direct SQL execution queries or session commits (belong in `app/repositories/`).
- API request or response modeling.

## Future Entities To Implement
- `user.py`: `User`, `UserProfile`, `UserSecurity` entities.
- `job.py`: `JobPosting`, `Company`, `JobSkill` entities.
- `application.py`: `Application`, `ApplicationHistory`, `Interview` entities.
- `resume.py`: `Resume`, `ATSAnalysis`, `SkillExtraction` entities.
