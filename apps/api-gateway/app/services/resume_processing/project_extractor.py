"""Phase 4 Day 27 — Project Extraction Engine.

Rule-based, section-aware, deterministic project extractor for resume processing.
Consumes ProcessedResumeText without mutating input objects.
Reuses Day 24 skill dictionaries and technology normalization.
"""

from typing import List, Dict, Any, Optional, Set, Tuple
import re
import time
import logging

from app.exceptions.resume import ResumeParsingError
from .models import ProcessedResumeText, ProjectRecord, ExtractedProjects
from .skill_dictionary import SKILL_DICTIONARY, ALIAS_MAP
from .project_normalizer import (
    normalize_project_name,
    normalize_technologies,
    classify_project,
    deduplicate_project_records,
)

logger = logging.getLogger("talentai.resume_processing.project_extractor")

# False positive guards for non-project sections
NON_PROJECT_SECTION_NAMES = {"SKILLS", "EXPERIENCE", "EDUCATION", "CERTIFICATIONS"}

# Generic non-technology words to ignore
GENERIC_IGNORE_WORDS = {"team", "system", "project", "development", "application", "platform", "tool", "user", "data", "technologies", "tech", "stack"}

# Date pattern for project dates
YEAR_RANGE_PATTERN = re.compile(r'\b(20[0-3]\d|19[7-9]\d)(?:\s*(?:-|–|—|to)\s*(20[0-3]\d|19[7-9]\d|Present|Current))?\b', re.IGNORECASE)


def _extract_techs_from_text(text: str) -> List[str]:
    """Match technologies in text against Day 24 SKILL_DICTIONARY and ALIAS_MAP."""
    if not text:
        return []

    found_techs: List[str] = []

    # Split by comma or slash or pipe for tech lists e.g. "FastAPI, React, PostgreSQL"
    parts = [p.strip(" ,.-()[]:\t\n") for p in re.split(r'[,/|]|(?:\band\b)', text) if p.strip()]
    for part in parts:
        low_part = part.lower()
        if low_part in GENERIC_IGNORE_WORDS:
            continue
        if low_part in ALIAS_MAP:
            alias_val = ALIAS_MAP[low_part]
            cand = alias_val[0] if isinstance(alias_val, (tuple, list)) else str(alias_val)
            if cand not in found_techs:
                found_techs.append(cand)
        elif low_part in SKILL_DICTIONARY:
            entry = SKILL_DICTIONARY[low_part]
            canonical_name = entry[0] if isinstance(entry, (tuple, list)) else str(entry)
            if canonical_name not in found_techs:
                found_techs.append(canonical_name)
        else:
            if len(part.split()) <= 4 and not re.search(r'\b(?:extracts|matches|builds|developed|created|implemented)\b', part, re.IGNORECASE):
                if part not in found_techs:
                    found_techs.append(part)

    # Token scan fallback
    for token in re.findall(r'\b[A-Za-z0-9+#.-]+\b', text):
        low_tok = token.lower()
        if low_tok in GENERIC_IGNORE_WORDS:
            continue
        if low_tok in ALIAS_MAP:
            alias_val = ALIAS_MAP[low_tok]
            cand = alias_val[0] if isinstance(alias_val, (tuple, list)) else str(alias_val)
            if cand not in found_techs:
                found_techs.append(cand)
        elif low_tok in SKILL_DICTIONARY:
            entry = SKILL_DICTIONARY[low_tok]
            canonical_name = entry[0] if isinstance(entry, (tuple, list)) else str(entry)
            if canonical_name not in found_techs:
                found_techs.append(canonical_name)

    return found_techs


ACTION_VERBS: Set[str] = {
    "architected", "developed", "built", "integrated", "designed", "implemented",
    "created", "engineered", "maintained", "utilized", "led", "managed", "configured",
    "deployed", "automated", "optimized", "enhanced", "spearheaded", "authored",
    "trained", "achieved", "executed", "collaborated", "constructed", "generated",
    "solved", "delivered", "programmed", "orchestrated", "established", "supervised",
}


TECH_KEYWORDS: Set[str] = {
    "python", "typescript", "javascript", "react", "react.js", "next.js", "nextjs", "node.js",
    "express.js", "fastapi", "django", "flask", "postgresql", "mongodb", "mysql", "redis",
    "docker", "kubernetes", "aws", "azure", "gcp", "tailwind", "prisma", "gemini api", "openai api",
    "pytorch", "tensorflow", "scikit-learn", "opencv", "spacy", "java", "c++", "c#", "html", "css"
}


def _is_pure_date_line(line: str) -> bool:
    """Check if line is purely a date or year range."""
    clean = line.strip()
    if YEAR_RANGE_PATTERN.search(clean):
        letters_only = re.sub(r'[\d\s\-–—/.,()toPresentCurrentOngoingNow]', '', clean, flags=re.IGNORECASE)
        if len(letters_only) == 0:
            return True
    return False


def _is_tech_stack_line(line: str) -> bool:
    """Check if line is a comma-separated tech stack listing rather than a project title."""
    clean = line.strip()
    if clean.lower().startswith(("technologies:", "tech stack:", "tools:", "stack:", "tech:")):
        return True
    if ("," in clean or "/" in clean) and ("|" not in clean and "–" not in clean and "—" not in clean and "(" not in clean):
        parts = [p.strip().lower() for p in re.split(r'[,/]', clean) if p.strip()]
        if len(parts) >= 2:
            matched = sum(1 for p in parts if any(k in p for k in TECH_KEYWORDS))
            if matched >= 1:
                return True
    return False


def _is_project_header_line(line: str) -> bool:
    """Determine if a line is a genuine project title header vs bullet/tech/description."""
    clean = line.strip()
    if not clean:
        return False
    # Check bullet prefixes
    if clean.startswith(("-", "*", "•", "▪", "◦", "‣")):
        return False
    # Check numbered bullet like 1. or (1)
    if re.match(r'^(?:\d+[\.\)]|\(\d+\))\s+', clean):
        return False
    # Check section title
    if clean.lower().rstrip(":") in {
        "projects", "academic projects", "personal projects",
        "key projects", "selected projects", "technical projects",
        "technologies", "tech stack", "tools", "stack"
    }:
        return False
    if _is_pure_date_line(clean):
        return False
    if _is_tech_stack_line(clean):
        return False
    # Check action verbs
    first_word = clean.split()[0].lower().rstrip(":,.-")
    if first_word in ACTION_VERBS:
        return False
    # Check ending in period (sentences are descriptions)
    if clean.endswith("."):
        return False
    # Project title shouldn't be excessively long sentence
    if len(clean) > 80:
        return False
    return True



def _extract_name_and_techs_from_line(line: str) -> Tuple[Optional[str], List[str]]:
    """Extract project name and embedded technologies from heading line."""
    if not line:
        return None, []

    line_clean = line.strip()

    # Parenthesis format e.g. "Resume Analyzer (Python, spaCy, FastAPI)"
    paren_match = re.search(r'^([A-Za-z0-9\s&._-]{2,50})\s*\(([^)]+)\)', line_clean)
    if paren_match:
        name_cand = paren_match.group(1).strip()
        tech_str = paren_match.group(2).strip()
        techs = _extract_techs_from_text(tech_str)
        return name_cand, techs

    # Separator format e.g. "Learnify – AI-Powered Learning Platform" or "Talent AI | FastAPI | React"
    if "|" in line_clean or "—" in line_clean or " – " in line_clean or " - " in line_clean:
        parts = [p.strip() for p in re.split(r'[|—–]|\s+-\s+', line_clean) if p.strip()]
        if len(parts) >= 2:
            name_cand = parts[0]
            techs: List[str] = []
            for p in parts[1:]:
                p_techs = _extract_techs_from_text(p)
                if p_techs:
                    techs.extend(p_techs)
            return name_cand, techs

    # Colon format e.g. "Talent Platform: Candidate-job matching platform" (ensure it is not a URL)
    if ":" in line_clean and not re.search(r'https?:', line_clean, re.IGNORECASE):
        parts = [p.strip() for p in line_clean.split(":", 1) if p.strip()]
        if len(parts) == 2:
            name_cand = parts[0]
            if len(name_cand) <= 50 and len(name_cand.split()) <= 5:
                techs = _extract_techs_from_text(parts[1])
                return name_cand, techs

    return line_clean, []


def extract_projects(processed_text: Optional[ProcessedResumeText]) -> ExtractedProjects:
    """Extract, normalize, classify, and deduplicate projects from ProcessedResumeText.

    Args:
        processed_text: ProcessedResumeText object from Day 23.

    Returns:
        ExtractedProjects container with extracted ProjectRecord items and metadata.

    Raises:
        ResumeParsingError: If processed_text is None or has no text.
    """
    if processed_text is None:
        raise ResumeParsingError("Cannot extract projects from a None ProcessedResumeText.")

    if not processed_text.normalized_text or not processed_text.normalized_text.strip():
        raise ResumeParsingError("The processed resume document contains no text.")

    start_time = time.perf_counter()
    records: List[ProjectRecord] = []

    # 1. Identify PROJECTS Sections vs Fallback
    proj_sections = [s for s in processed_text.sections if s.name == "PROJECTS"]

    blocks: List[List[Tuple[str, str, float]]] = []

    if proj_sections:
        for sec in proj_sections:
            lines = [l.strip() for l in sec.content.splitlines() if l.strip()]
            curr_block: List[Tuple[str, str, float]] = []
            for l in lines:
                if l.lower().rstrip(":") in {"projects", "academic projects", "personal projects", "key projects", "technical projects"}:
                    continue
                if _is_project_header_line(l):
                    if curr_block:
                        blocks.append(curr_block)
                        curr_block = []
                curr_block.append((l, sec.name, 0.95))
            if curr_block:
                blocks.append(curr_block)

    # 2. Process Candidate Blocks
    for block in blocks:
        block_lines = [item[0] for item in block]
        block_text = " ".join(block_lines)
        sec_name = block[0][1]
        base_confidence = block[0][2]

        if not block_lines:
            continue

        header_line = block_lines[0]

        # Ignore if header line is just "PROJECTS" or "ACADEMIC PROJECTS"
        if header_line.lower().rstrip(":") in {"projects", "academic projects", "personal projects", "technologies", "tech stack"}:
            if len(block_lines) > 1:
                header_line = block_lines[1]
                block_lines = block_lines[1:]
            else:
                continue

        # Extract name and same-line technologies
        raw_name, same_line_techs = _extract_name_and_techs_from_line(header_line)
        if not raw_name or len(raw_name) > 60 or raw_name.endswith("."):
            continue

        # Clean project name
        can_name, norm_name = normalize_project_name(raw_name)
        if not can_name:
            continue


        # Extract technologies from explicit tech lines & block body
        raw_techs: List[str] = list(same_line_techs)
        description_lines: List[str] = []
        start_yr: Optional[int] = None
        end_yr: Optional[int] = None

        for l in block_lines[1:]:
            l_clean = l.strip()
            if not l_clean:
                continue

            # Check explicit technology line e.g. "FastAPI, React, PostgreSQL" or "Technologies: FastAPI, React"
            if l_clean.lower().startswith(("technologies:", "tech stack:", "tools:", "stack:")):
                tech_val = re.sub(r'^(?:technologies|tech stack|tools|stack):\s*', '', l_clean, flags=re.IGNORECASE)
                raw_techs.extend(_extract_techs_from_text(tech_val))
                continue

            # Check date line e.g. "2024 - 2025"
            date_match = YEAR_RANGE_PATTERN.search(l_clean)
            if date_match and len(l_clean) < 30 and not any(kw in l_clean.lower() for kw in ["system", "platform", "app"]):
                start_yr = int(date_match.group(1))
                if date_match.group(2) and date_match.group(2).isdigit():
                    end_yr = int(date_match.group(2))
                continue

            # Check if standalone line is a list of technologies e.g. "FastAPI, React, PostgreSQL"
            extracted_line_techs = _extract_techs_from_text(l_clean)
            if extracted_line_techs and len(l_clean.split(",")) >= 2 and not l_clean.startswith(("-", "•", "*")):
                raw_techs.extend(extracted_line_techs)
                continue

            # Description bullet or paragraph line
            clean_l = l_clean.lstrip("- •*▪◦‣\t").strip()
            if clean_l and len(clean_l) > 5:
                description_lines.append(clean_l)
                # Also extract technologies mentioned inside description line
                raw_techs.extend(_extract_techs_from_text(clean_l))

        # Normalize technologies
        can_techs, norm_techs = normalize_technologies(raw_techs)

        # Build original verbatim description text
        description_text = " ".join(description_lines)

        # Classify project domain & project type
        classification, project_type = classify_project(can_name, description_text, can_techs)

        # Compute heuristic confidence
        confidence = base_confidence
        if can_name and can_techs and description_text:
            confidence = min(0.98, base_confidence + 0.03)
        elif can_name and (can_techs or description_text):
            confidence = base_confidence
        else:
            confidence = max(0.75, base_confidence - 0.15)

        record = ProjectRecord(
            name=can_name,
            normalized_name=norm_name,
            technologies=can_techs,
            normalized_technologies=norm_techs,
            description=description_text,
            project_type=project_type,
            classification=classification,
            start_year=start_yr,
            end_year=end_yr,
            source_text=block_text[:300],
            section=sec_name,
            source="pattern",
            confidence=round(confidence, 2),
        )
        records.append(record)

    # 3. Deduplicate records
    deduped_records = deduplicate_project_records(records)
    elapsed_sec = round(time.perf_counter() - start_time, 4)

    # Build classification summary dict
    class_map: Dict[str, List[str]] = {}
    for r in deduped_records:
        cls = r.classification or "OTHER"
        if cls not in class_map:
            class_map[cls] = []
        if r.name and r.name not in class_map[cls]:
            class_map[cls].append(r.name)

    logger.info(
        "Extracted %d project records (%d deduplicated) in %.4fs",
        len(records),
        len(deduped_records),
        elapsed_sec,
    )

    return ExtractedProjects(
        projects=deduped_records,
        total_count=len(deduped_records),
        classifications=class_map,
        metadata={
            "duration_seconds": elapsed_sec,
            "raw_candidate_blocks": len(blocks),
            "accepted_projects_count": len(deduped_records),
        },
    )
