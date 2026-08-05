"""Password Hashing and Verification Service.

Provides secure password hashing and verification routines using `pwdlib`
with Argon2id and Bcrypt support. This module is the sole authority for password
cryptographic operations across the TalentAI platform.
"""

from typing import Final
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from pwdlib.hashers.bcrypt import BcryptHasher

# Singleton PasswordHash instance with Argon2id as default and Bcrypt as fallback/deprecated hasher.
_hasher: Final[PasswordHash] = PasswordHash(
    (
        Argon2Hasher(),
        BcryptHasher(),
    )
)


def hash_password(password: str) -> str:
    """Securely hash a plain text password using pwdlib.

    Validates password input, strips leading and trailing whitespace, and returns
    the generated password hash string using the default password hashing algorithm (Argon2id).

    Args:
        password: Plain text password string to be hashed.

    Returns:
        Securely formatted password hash string.

    Raises:
        ValueError: If password is None, empty, or consists only of whitespace.
        RuntimeError: If password hashing encounters an unexpected internal error.
    """
    if password is None:
        raise ValueError("Password cannot be None.")

    cleaned_password = password.strip()
    if not cleaned_password:
        raise ValueError("Password cannot be empty or consist only of whitespace.")

    try:
        return _hasher.hash(cleaned_password)
    except Exception as exc:
        raise RuntimeError("An unexpected error occurred while hashing the password.") from exc


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain text password against a stored password hash.

    Compares the provided plain text password with the stored password hash in a
    constant-time or cryptographically secure manner. Strips leading/trailing whitespace
    from the plain text password prior to verification.

    Args:
        plain_password: Plain text password to verify.
        hashed_password: Stored password hash string to verify against.

    Returns:
        True if the password matches the hash, False otherwise.
        Returns False safely if inputs are invalid or verification fails.
    """
    if plain_password is None or hashed_password is None:
        return False

    cleaned_password = plain_password.strip()
    if not cleaned_password or not hashed_password.strip():
        return False

    try:
        return _hasher.verify(cleaned_password, hashed_password)
    except Exception:
        return False
