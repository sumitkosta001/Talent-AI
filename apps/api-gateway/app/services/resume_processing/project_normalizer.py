"""Project Normalizer and Classification Engine for Day 27.

Provides deterministic functions for normalizing project names, technology stacks,
classifying project domains and types, and deduplicating project records.
Reuses Day 24 SKILL_DICTIONARY and ALIAS_MAP for technology normalization.
"""

from typing import List, Tuple, Optional, Dict, Any, Set
import re
import logging

from .models import ProjectRecord
from .skill_dictionary import SKILL_DICTIONARY, ALIAS_MAP

logger = logging.getLogger("talentai.resume_processing.project_normalizer")


def normalize_project_name(raw_name: str) -> Tuple[Optional[str], Optional[str]]:
    """Clean raw project name string and generate normalized ID.

    Returns:
        (canonical_name, normalized_name)
    """
    if not raw_name or not raw_name.strip():
        return None, None

    cleaned = raw_name.strip(" ,.-|:\t\n")
    cleaned = re.sub(r'\s+', ' ', cleaned)

    if not cleaned:
        return None, None

    lowered = cleaned.lower()
    return cleaned, lowered


def normalize_technologies(raw_techs: List[str]) -> Tuple[List[str], List[str]]:
    """Normalize technology strings using Day 24 SKILL_DICTIONARY and ALIAS_MAP.

    Returns:
        (canonical_technologies_list, normalized_technologies_list)
    """
    if not raw_techs:
        return [], []

    canonical_set: Set[str] = set()
    normalized_set: Set[str] = set()

    for tech in raw_techs:
        if isinstance(tech, (tuple, list)):
            tech_str = str(tech[0])
        else:
            tech_str = str(tech)

        if not tech_str or not tech_str.strip():
            continue
        cleaned = tech_str.strip(" ,.-|:\t\n")
        lowered = cleaned.lower()

        # Check ALIAS_MAP (maps lowercase alias -> (canonical_name, category))
        if lowered in ALIAS_MAP:
            entry = ALIAS_MAP[lowered]
            canonical_name = entry[0] if isinstance(entry, (tuple, list)) else str(entry)
            canonical_set.add(canonical_name)
            normalized_set.add(canonical_name.lower())
        else:
            # Preserve raw capitalization for unknown technology
            canonical_set.add(cleaned)
            normalized_set.add(lowered)

    # Return deterministically sorted lists
    can_list = sorted(list(canonical_set))
    norm_list = sorted(list(normalized_set))
    return can_list, norm_list


def classify_project(name: str, description: str, techs: List[str]) -> Tuple[str, str]:
    """Deterministically classify project domain and project type based on evidence.

    Returns:
        (classification, project_type)
    """
    combined_text = f"{name or ''} {description or ''} {' '.join(techs or [])}".lower()

    # 1. Classify Project Type
    project_type = "UNKNOWN"
    if re.search(r'\b(?:academic|university|coursework|capstone|thesis)\b', combined_text):
        project_type = "ACADEMIC"
    elif re.search(r'\b(?:personal|hobby|side\s+project|portfolio)\b', combined_text):
        project_type = "PERSONAL"
    elif re.search(r'\b(?:open\s*source|github|contributor)\b', combined_text):
        project_type = "OPEN_SOURCE"
    elif re.search(r'\b(?:client|commercial|freelance|enterprise|company)\b', combined_text):
        project_type = "COMMERCIAL"

    # 2. Classify Project Domain (Classification Precedence)
    # Priority 1: Mobile Application
    if re.search(r'\b(?:react\s+native|flutter|ios|android|swift|kotlin|mobile\s+app)\b', combined_text):
        return "MOBILE_APPLICATION", project_type

    # Priority 2: Machine Learning
    ml_evidence = re.search(r'\b(?:tensorflow|pytorch|scikit-learn|sklearn|keras|machine\s+learning|deep\s+learning|prediction|classification|regression|random\s+forest|xgboost)\b', combined_text)
    if ml_evidence:
        return "MACHINE_LEARNING", project_type

    # Priority 3: Artificial Intelligence / Computer Vision / NLP
    ai_evidence = re.search(r'\b(?:opencv|computer\s+vision|nlp|spacy|llm|transformers|neural\s+network|face\s+recognition|artificial\s+intelligence)\b', combined_text)
    if ai_evidence:
        return "ARTIFICIAL_INTELLIGENCE", project_type

    # Priority 4: Data Engineering / Data Science
    data_evidence = re.search(r'\b(?:spark|hadoop|pandas|numpy|etl|data\s+pipeline|data\s+science|analytics)\b', combined_text)
    if data_evidence:
        return "DATA_SCIENCE", project_type

    # Priority 5: DevOps / Cloud / Infrastructure
    devops_evidence = re.search(r'\b(?:docker|kubernetes|aws|azure|gcp|terraform|ci/cd|jenkins|ansible|devops|cloud)\b', combined_text)
    if devops_evidence and not re.search(r'\b(?:react|angular|vue|fastapi|django)\b', combined_text):
        return "DEVOPS", project_type

    # Priority 6: Embedded / IoT / Hardware
    embedded_evidence = re.search(r'\b(?:arduino|raspberry\s+pi|sensors|embedded|microcontroller|iot)\b', combined_text)
    if embedded_evidence:
        return "EMBEDDED", project_type

    # Priority 7: Full Stack (Frontend + Backend evidence present)
    has_frontend = bool(re.search(r'\b(?:react|next\.js|angular|vue|html|css|typescript|javascript)\b', combined_text))
    has_backend = bool(re.search(r'\b(?:fastapi|django|flask|express|node\.js|spring|postgresql|mongodb|mysql)\b', combined_text))
    if has_frontend and has_backend:
        return "FULL_STACK", project_type

    # Priority 8: Web Application
    if has_frontend or re.search(r'\b(?:web\s+app|website|web\s+platform|dashboard|portal)\b', combined_text):
        return "WEB_APPLICATION", project_type

    if has_backend:
        return "WEB_APPLICATION", project_type

    # Priority 9: Research
    if re.search(r'\b(?:research|paper|publication)\b', combined_text):
        return "RESEARCH", project_type

    return "OTHER", project_type


def deduplicate_project_records(records: List[ProjectRecord]) -> List[ProjectRecord]:
    """Deduplicate project records based on normalized project name and technologies.

    Returns deduplicated records preserving document order.
    """
    if not records:
        return []

    seen: Set[Tuple[str, str]] = set()
    deduped: List[ProjectRecord] = []

    for rec in records:
        key = (
            (rec.normalized_name or "").lower(),
            ",".join(sorted(rec.normalized_technologies)),
        )
        if key in seen:
            continue
        seen.add(key)
        deduped.append(rec)

    return deduped
