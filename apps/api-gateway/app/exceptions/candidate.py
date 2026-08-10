"""Candidate Profile Domain Exception Classes."""

from app.exceptions.base import TalentAIException


class CandidateProfileError(TalentAIException):
    """Base exception class for candidate profile operations."""

    def __init__(self, message: str = "Candidate profile error occurred.", status_code: int = 400) -> None:
        super().__init__(message=message, status_code=status_code)


class CandidateProfileNotFoundError(CandidateProfileError):
    """Raised when a requested candidate profile does not exist."""

    def __init__(self, identifier: str = "me") -> None:
        super().__init__(
            message=f"Candidate profile '{identifier}' was not found.",
            status_code=404,
        )


class EducationNotFoundError(CandidateProfileError):
    """Raised when an education record does not exist or does not belong to the candidate."""

    def __init__(self, education_id: str) -> None:
        super().__init__(
            message=f"Education record '{education_id}' was not found.",
            status_code=404,
        )


class ExperienceNotFoundError(CandidateProfileError):
    """Raised when an experience record does not exist or does not belong to the candidate."""

    def __init__(self, experience_id: str) -> None:
        super().__init__(
            message=f"Experience record '{experience_id}' was not found.",
            status_code=404,
        )


class SkillNotFoundError(CandidateProfileError):
    """Raised when a skill record does not exist or does not belong to the candidate."""

    def __init__(self, skill_id: str) -> None:
        super().__init__(
            message=f"Skill record '{skill_id}' was not found.",
            status_code=404,
        )


class DuplicateSkillError(CandidateProfileError):
    """Raised when attempting to add a skill that already exists on the candidate profile."""

    def __init__(self, skill_name: str) -> None:
        super().__init__(
            message=f"Skill '{skill_name}' has already been added to your profile.",
            status_code=409,
        )


class InvalidDateRangeError(CandidateProfileError):
    """Raised when start_date is after end_date."""

    def __init__(self, message: str = "Start date cannot be after end date.") -> None:
        super().__init__(message=message, status_code=422)
