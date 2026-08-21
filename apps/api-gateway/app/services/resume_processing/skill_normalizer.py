"""Skill Normalizer and Deduplicator for Day 24.

Maps raw skill matches and aliases to canonical skill names, deduplicates mentions across
the document, aggregates section context and mention counts, and constructs ExtractedSkills.
"""

from typing import List, Dict, Any, Set, Tuple, Optional
from collections import defaultdict
import logging

from .models import ExtractedSkill, ExtractedSkills
from .skill_dictionary import ALIAS_MAP, SKILL_DICTIONARY

logger = logging.getLogger("talentai.resume_processing.skill_normalizer")


def normalize_and_deduplicate_skills(
    raw_matches: List[Dict[str, Any]],
) -> ExtractedSkills:
    """Normalize, deduplicate, and group raw skill match dictionaries into ExtractedSkills.

    Args:
        raw_matches: List of match dicts containing:
          - matched_text: str (raw match string)
          - canonical_name: Optional[str]
          - category: Optional[str]
          - section_name: str (e.g. 'SKILLS', 'EXPERIENCE')
          - source: str ('dictionary', 'phrase_match', 'regex', etc.)
          - confidence: float

    Returns:
        ExtractedSkills container with deduplicated skills and category breakdowns.
    """
    if not raw_matches:
        return ExtractedSkills(skills=[], total_count=0, categories={}, metadata={"match_count": 0})

    # Group matches by canonical skill name
    grouped: Dict[str, Dict[str, Any]] = {}

    for match in raw_matches:
        matched_text = match.get("matched_text", "").strip()
        if not matched_text:
            continue

        candidate_canonical = match.get("canonical_name")

        # Resolve canonical name and category strictly via dictionary/aliases
        resolved = _resolve_canonical_skill(matched_text, candidate_canonical)
        if not resolved:
            logger.debug(
                "Skipping unresolved raw match: matched_text='%s', candidate_canonical='%s'",
                matched_text,
                candidate_canonical,
            )
            continue

        canonical_name, category = resolved
        norm_name = canonical_name.lower()
        section_name = match.get("section_name", "UNKNOWN")
        source = match.get("source", "dictionary")
        confidence = match.get("confidence", 0.90)

        if norm_name not in grouped:
            grouped[norm_name] = {
                "name": canonical_name,
                "normalized_name": norm_name,
                "category": category,
                "sources": set([source]),
                "confidence": confidence,
                "matched_text": matched_text,
                "sections": set([section_name]),
                "mentions_count": 1,
            }
        else:
            entry = grouped[norm_name]
            entry["mentions_count"] += 1
            entry["sections"].add(section_name)
            entry["sources"].add(source)

            # Determine whether new matched_text is preferred over existing matched_text
            if _is_better_matched_text(
                matched_text, confidence, entry["matched_text"], entry["confidence"], canonical_name
            ):
                entry["matched_text"] = matched_text

            # Maximize confidence score if seen in a higher-priority section
            if confidence > entry["confidence"]:
                entry["confidence"] = confidence

    # Build ExtractedSkill objects
    skills_list: List[ExtractedSkill] = []
    category_map: Dict[str, Set[str]] = defaultdict(set)

    for norm_name, entry in grouped.items():
        # Preserve sections order deterministically
        section_list = sorted(list(entry["sections"]))
        sources_set = entry["sources"]
        final_source = _resolve_source(sources_set)

        skill_obj = ExtractedSkill(
            name=entry["name"],
            normalized_name=entry["normalized_name"],
            category=entry["category"],
            source=final_source,
            confidence=round(entry["confidence"], 2),
            matched_text=entry["matched_text"],
            sections=section_list,
            mentions_count=entry["mentions_count"],
        )
        skills_list.append(skill_obj)
        category_map[entry["category"]].add(entry["name"])

    # Deterministic sorting: highest confidence first, then by mentions_count desc, then canonical name asc
    skills_list.sort(key=lambda s: (-s.confidence, -s.mentions_count, s.name.lower()))

    # Build category dict with sorted list of canonical skill names
    categories_dict: Dict[str, List[str]] = {
        cat: sorted(list(skills))
        for cat, skills in sorted(category_map.items())
    }

    return ExtractedSkills(
        skills=skills_list,
        total_count=len(skills_list),
        categories=categories_dict,
        metadata={
            "raw_matches_count": len(raw_matches),
            "deduplicated_skills_count": len(skills_list),
        },
    )


def _resolve_canonical_skill(
    matched_text: str, candidate_canonical: Optional[str]
) -> Optional[Tuple[str, str]]:
    """Resolve matched_text and optional candidate_canonical to (canonical_name, category).

    Strictly validates against SKILL_DICTIONARY and ALIAS_MAP.
    Returns None if the match cannot be resolved.
    """
    raw_lower = matched_text.lower()

    # Case 1: candidate_canonical is provided and present in SKILL_DICTIONARY
    if candidate_canonical and candidate_canonical in SKILL_DICTIONARY:
        category = SKILL_DICTIONARY[candidate_canonical]["category"]
        return candidate_canonical, category

    # Case 2: raw_lower in ALIAS_MAP -> gives canonical name from dictionary
    if raw_lower in ALIAS_MAP:
        canonical_name, _ = ALIAS_MAP[raw_lower]
        if canonical_name in SKILL_DICTIONARY:
            category = SKILL_DICTIONARY[canonical_name]["category"]
            return canonical_name, category

    # Case 3: raw_lower matches a canonical key in SKILL_DICTIONARY (case-insensitive)
    for dict_key, info in SKILL_DICTIONARY.items():
        if dict_key.lower() == raw_lower:
            return dict_key, info["category"]

    # Case 4: candidate_canonical matches a canonical key in SKILL_DICTIONARY (case-insensitive)
    if candidate_canonical:
        cand_lower = candidate_canonical.lower()
        for dict_key, info in SKILL_DICTIONARY.items():
            if dict_key.lower() == cand_lower:
                return dict_key, info["category"]

    return None


def _resolve_source(sources: Set[str]) -> str:
    """Deterministically merge set of match sources into final source string.

    Rules:
    - If "hybrid" exists: return "hybrid"
    - If both "phrase_match" and "regex" exist: return "hybrid"
    - If "phrase_match" exists: return "phrase_match"
    - If "regex" exists: return "regex"
    - If "dictionary" exists: return "dictionary"
    - Otherwise: return deterministic first source (alphabetical order)
    """
    if "hybrid" in sources or ("phrase_match" in sources and "regex" in sources):
        return "hybrid"
    if "phrase_match" in sources:
        return "phrase_match"
    if "regex" in sources:
        return "regex"
    if "dictionary" in sources:
        return "dictionary"

    sorted_sources = sorted(list(sources))
    return sorted_sources[0] if sorted_sources else "dictionary"


def _is_better_matched_text(
    new_text: str, new_conf: float, curr_text: str, curr_conf: float, canonical_name: str
) -> bool:
    """Determine if new_text should replace curr_text for matched_text representation.

    Priority order:
    1. Higher confidence score.
    2. If confidence is equal, prefer canonical-looking casing.
    3. If still equal, retain current (first occurrence) deterministically.
    """
    if new_conf > curr_conf:
        return True
    if new_conf < curr_conf:
        return False

    def _casing_score(text: str) -> int:
        if text == canonical_name:
            return 3
        if text.lower() == canonical_name.lower() and text != text.lower():
            return 2
        if any(c.isupper() for c in text):
            return 1
        return 0

    return _casing_score(new_text) > _casing_score(curr_text)
