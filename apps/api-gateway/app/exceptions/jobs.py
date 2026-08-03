"""Job Posting and Recruitment Domain Custom Exceptions."""

from .base import TalentAIException


class JobNotFoundError(TalentAIException):
    """Raised when target job posting does not exist."""

    def __init__(self, job_id: str | int = "") -> None:
        """Initialize job not found error with 404 status."""
        msg = f"Job posting '{job_id}' not found." if job_id else "Job posting not found."
        super().__init__(message=msg, status_code=404)


class JobClosedError(TalentAIException):
    """Raised when user attempts to apply to a closed or draft job posting."""

    def __init__(self, message: str = "This job posting is closed for applications.") -> None:
        """Initialize job closed error with 400 status."""
        super().__init__(message=message, status_code=400)
