"""User Domain Custom Exceptions."""

from .base import TalentAIException


class UserNotFoundError(TalentAIException):
    """Raised when specified user account is not found."""

    def __init__(self, user_id_or_email: str | int = "") -> None:
        """Initialize user not found error with 404 status."""
        msg = f"User '{user_id_or_email}' not found." if user_id_or_email else "User account not found."
        super().__init__(message=msg, status_code=404)


class UserInactiveError(TalentAIException):
    """Raised when attempting action on disabled/deactivated user account."""

    def __init__(self, message: str = "User account has been suspended or deactivated.") -> None:
        """Initialize user inactive error with 403 status."""
        super().__init__(message=message, status_code=403)
