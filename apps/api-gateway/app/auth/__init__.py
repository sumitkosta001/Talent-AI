"""Authentication Module for TalentAI API Gateway.

Handles JWT encoding/decoding, OAuth2 integration (Google/GitHub), Argon2 password
hashing, role/permission checkers, and security token rotation protocols.
"""

__all__ = [
    "jwt",
    "oauth",
    "password",
    "permissions",
    "security",
    "tokens",
]
