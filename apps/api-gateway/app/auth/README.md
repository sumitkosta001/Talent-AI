# Authentication Module (`app/auth/`)

## Purpose
The `app/auth/` module encapsulates low-level authentication protocols, cryptographically secure token processing, password hashing primitives, and permission evaluation rules.

## Responsibilities
- **JWT Management**: Encodes and decodes signed JWT access tokens using HS256/RS256.
- **OAuth2 Protocols**: Manages social authentication redirect URLs and callback token exchanges for Google/GitHub identity providers.
- **Password Hashing**: Provides Argon2id hashing and constant-time signature verification.
- **Role-Based Access Control (RBAC)**: Evaluates user roles (`candidate`, `recruiter`, `admin`) against required resource scopes.
- **Refresh Token Rotation**: Coordinates Redis-backed refresh token storage, rotation, and revocation blacklists.

## What Belongs Here
- Low-level authentication algorithms, cryptographic helpers, OAuth provider state helpers, token generators, and permission checkers.

## What Should NOT Belong Here
- FastAPI `APIRouter` endpoint declarations (belong in `app/routers/auth.py`).
- Higher-level business domain logic (belongs in `app/services/`).
- Database models or direct SQL queries (belong in `app/models/` and `app/repositories/`).

## Future Implementation Files
- `jwt.py`: Production PyJWT / python-jose integration with RSA keypair support.
- `oauth.py`: Full httpx OAuth2 client for Google, GitHub, and LinkedIn SSO.
- `password.py`: Passlib Argon2id configuration.
- `tokens.py`: Redis connection integration for revoked JWT blacklisting.
