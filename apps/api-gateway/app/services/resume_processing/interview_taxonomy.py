"""Phase 4 — Day 34: Interview Question Taxonomies.

Centralized taxonomy for question categories and difficulty levels.
Prevents scattered string constants and enforces consistent API representations.
"""

from enum import Enum
from typing import List, Dict, Set


class QuestionCategory(str, Enum):
    """Centralized taxonomy for interview question categories (Day 34)."""

    TECHNICAL = "TECHNICAL"
    BEHAVIORAL = "BEHAVIORAL"
    SYSTEM_DESIGN = "SYSTEM_DESIGN"
    CODING = "CODING"
    CONCEPTUAL = "CONCEPTUAL"
    PROJECT = "PROJECT"
    EXPERIENCE = "EXPERIENCE"
    ROLE_SPECIFIC = "ROLE_SPECIFIC"
    SKILL_SPECIFIC = "SKILL_SPECIFIC"
    SITUATIONAL = "SITUATIONAL"


class QuestionDifficulty(str, Enum):
    """Centralized taxonomy for interview question difficulty levels (Day 34)."""

    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"
    EXPERT = "EXPERT"


# Default distribution helper ratios when target count is requested
DEFAULT_CATEGORY_DISTRIBUTION: Dict[QuestionCategory, float] = {
    QuestionCategory.TECHNICAL: 0.30,
    QuestionCategory.SKILL_SPECIFIC: 0.20,
    QuestionCategory.ROLE_SPECIFIC: 0.20,
    QuestionCategory.PROJECT: 0.15,
    QuestionCategory.BEHAVIORAL: 0.15,
}


def normalize_category(category_str: str) -> QuestionCategory:
    """Normalize input category string to QuestionCategory Enum.

    Handles plain strings ('technical'), enum value strings ('TECHNICAL'),
    and Python str() enum representations ('QuestionCategory.TECHNICAL').
    """
    if not category_str or not category_str.strip():
        return QuestionCategory.TECHNICAL

    # Strip class prefix if str() was called on a str Enum (e.g. "QuestionCategory.TECHNICAL")
    raw = category_str.strip()
    if "." in raw:
        raw = raw.split(".", 1)[-1]

    cleaned = raw.upper().replace(" ", "_").replace("-", "_")
    for cat in QuestionCategory:
        if cat.value == cleaned or cat.name == cleaned:
            return cat
    return QuestionCategory.TECHNICAL


def normalize_difficulty(difficulty_str: str) -> QuestionDifficulty:
    """Normalize input difficulty string to QuestionDifficulty Enum.

    Handles plain strings ('easy'), enum value strings ('EASY'),
    and Python str() enum representations ('QuestionDifficulty.EASY').
    """
    if not difficulty_str or not difficulty_str.strip():
        return QuestionDifficulty.MEDIUM

    # Strip class prefix if str() was called on a str Enum (e.g. "QuestionDifficulty.EASY")
    raw = difficulty_str.strip()
    if "." in raw:
        raw = raw.split(".", 1)[-1]

    cleaned = raw.upper()
    for diff in QuestionDifficulty:
        if diff.value == cleaned or diff.name == cleaned:
            return diff
    return QuestionDifficulty.MEDIUM
