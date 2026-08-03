# Custom Exceptions Module (`app/exceptions/`)

## Purpose
The `app/exceptions/` module establishes a domain-specific custom exception hierarchy derived from `TalentAIException`. This allows services to raise expressive domain errors that automatically translate into formatted HTTP responses.

## Responsibilities
- Provides standard base exception `TalentAIException(message, status_code, details)`.
- Defines domain-focused subclasses:
  - `auth.py`: Authentication and permission exceptions (`401`, `403`).
  - `database.py`: Record search and unique conflict exceptions (`404`, `409`).
  - `jobs.py`: Job availability and lifecycle exceptions.
  - `users.py`: Account status and lookup exceptions.
  - `resume.py`: Document parsing and file format exceptions (`400`, `422`).

## What Belongs Here
- Custom Python exception classes and error taxonomy.

## What Should NOT Belong Here
- FastAPI `FastAPI.add_exception_handler` middleware handling (belongs in `app/main.py` or middleware handlers).
- Direct HTTP JSON responses.
