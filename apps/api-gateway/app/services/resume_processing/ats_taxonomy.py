"""Phase 4 Day 30 — ATS Scoring Taxonomy and Weights.

Centralized weights, component parameters, role compatibility matrices,
and degree level rank mappings.
"""

from typing import Dict

# Global Component Weights (Sum = 1.0)
ATS_KEYWORD_WEIGHT: float = 0.20
ATS_SKILL_WEIGHT: float = 0.40
ATS_EDUCATION_WEIGHT: float = 0.15
ATS_EXPERIENCE_WEIGHT: float = 0.25

# Sub-component Weights
REQUIRED_SKILL_WEIGHT: float = 0.75
PREFERRED_SKILL_WEIGHT: float = 0.25

REQUIRED_KEYWORD_WEIGHT: float = 0.75
PREFERRED_KEYWORD_WEIGHT: float = 0.25

REQUIRED_EDUCATION_WEIGHT: float = 0.80
PREFERRED_EDUCATION_WEIGHT: float = 0.20

# Experience Component Weights
EXP_DURATION_WEIGHT: float = 0.50
EXP_ROLE_WEIGHT: float = 0.25
EXP_DOMAIN_WEIGHT: float = 0.15
EXP_SENIORITY_WEIGHT: float = 0.10

SCORER_VERSION: str = "day30-v1"
SCORING_METHOD: str = "weighted_hybrid_rule_based"

# Degree Level Hierarchy Rank Mapping (Higher = More Advanced)
DEGREE_LEVEL_RANKS: Dict[str, int] = {
    "DOCTORATE": 4,
    "POSTGRADUATE": 3,
    "MASTER": 3,
    "UNDERGRADUATE": 2,
    "BACHELOR": 2,
    "ASSOCIATE": 1,
    "DIPLOMA": 1,
    "SECONDARY": 1,
    "UNKNOWN": 0,
    "OTHER": 0,
}

# Role Compatibility Score Matrix (Range 0.0 - 1.0)
ROLE_COMPATIBILITY_MAP: Dict[str, Dict[str, float]] = {
    "FULL_STACK_DEVELOPER": {
        "FULL_STACK_DEVELOPER": 1.0,
        "BACKEND_DEVELOPER": 0.85,
        "FRONTEND_DEVELOPER": 0.85,
        "SOFTWARE_ENGINEER": 0.90,
        "WEB_DEVELOPER": 0.80,
    },
    "BACKEND_DEVELOPER": {
        "BACKEND_DEVELOPER": 1.0,
        "FULL_STACK_DEVELOPER": 0.80,
        "SOFTWARE_ENGINEER": 0.85,
    },
    "FRONTEND_DEVELOPER": {
        "FRONTEND_DEVELOPER": 1.0,
        "FULL_STACK_DEVELOPER": 0.80,
        "SOFTWARE_ENGINEER": 0.80,
    },
    "SOFTWARE_ENGINEER": {
        "SOFTWARE_ENGINEER": 1.0,
        "FULL_STACK_DEVELOPER": 0.85,
        "BACKEND_DEVELOPER": 0.85,
        "FRONTEND_DEVELOPER": 0.80,
    },
    "MACHINE_LEARNING_ENGINEER": {
        "MACHINE_LEARNING_ENGINEER": 1.0,
        "AI_ENGINEER": 0.90,
        "DATA_SCIENTIST": 0.80,
    },
    "AI_ENGINEER": {
        "AI_ENGINEER": 1.0,
        "MACHINE_LEARNING_ENGINEER": 0.90,
        "DATA_SCIENTIST": 0.75,
    },
    "DATA_SCIENTIST": {
        "DATA_SCIENTIST": 1.0,
        "MACHINE_LEARNING_ENGINEER": 0.80,
        "DATA_ANALYST": 0.70,
    },
    "DEVOPS_ENGINEER": {
        "DEVOPS_ENGINEER": 1.0,
        "CLOUD_ENGINEER": 0.85,
        "SYSTEMS_ENGINEER": 0.75,
    },
    "EMBEDDED_ENGINEER": {
        "EMBEDDED_ENGINEER": 1.0,
        "FIRMWARE_ENGINEER": 0.90,
        "ELECTRONICS_ENGINEER": 0.80,
    },
}
