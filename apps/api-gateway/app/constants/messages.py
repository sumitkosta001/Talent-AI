"""Standardized Response and Error Message Strings."""


class ResponseMessages:
    """Standardized operational response messages."""

    LOGIN_SUCCESS = "User authenticated successfully."
    REGISTER_SUCCESS = "Account created. Please check email for verification."
    LOGOUT_SUCCESS = "Session ended successfully."
    PASSWORD_RESET_SENT = "Password reset instructions sent to email."
    RESUME_PARSED = "Resume parsed and ATS evaluation completed."
    UNAUTHORIZED = "Invalid or expired authorization token."
    FORBIDDEN = "Insufficient permissions to perform action."
