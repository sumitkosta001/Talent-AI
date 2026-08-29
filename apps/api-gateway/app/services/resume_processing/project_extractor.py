"""Phase 4 Day 27 — Project Extraction Engine.

Rule-based, section-aware, deterministic project extractor for resume processing.
Consumes ProcessedResumeText without mutating input objects.
Reuses Day 24 skill dictionaries and technology normalization.

Implements multi-signal scoring for project header detection to prevent
false positives from subtitles, description lines, tech stacks, dates, labels,
and non-project section headings (Achievements, Certifications, Awards, etc.).
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
NON_PROJECT_SECTION_NAMES = {
    "SKILLS", "EXPERIENCE", "EDUCATION", "CERTIFICATIONS", "ACHIEVEMENTS",
    "AWARDS", "PUBLICATIONS", "LANGUAGES", "INTERESTS", "REFERENCES", "CONTACT",
    "PROFILE", "OBJECTIVE", "VOLUNTEERING", "LEADERSHIP", "EXTRACURRICULAR",
}

# Comprehensive set of normalized non-project section keywords and titles
_NON_PROJECT_SECTION_KEYWORDS: Set[str] = {
    # Section titles & labels
    "achievements", "certifications", "certificates", "certificate", "certification",
    "awards", "honors", "accomplishments", "extracurricular", "activities",
    "extracurricular activities", "publications", "volunteering", "leadership",
    "interests", "hobbies", "languages", "references", "education", "experience",
    "work experience", "professional experience", "employment history", "skills",
    "technical skills", "summary", "objective", "contact", "profile", "personal info",
    "licenses & certifications", "licenses and certifications", "courses & certifications",
    "achievements/certifications", "achievements & certifications", "achievements and certifications",
    "certifications & achievements", "certifications and achievements", "certifications/achievements",
    "honors & awards", "honors and awards", "awards & honors", "awards and honors",
    "patents", "patents & publications", "research papers", "national semi-finalist",
}

# Generic non-technology words to ignore
GENERIC_IGNORE_WORDS = {"team", "system", "project", "development", "application", "platform", "tool", "user", "data", "technologies", "tech", "stack"}

# Common English words that must never be treated as technologies
_COMMON_NON_TECH_WORDS: Set[str] = {
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with",
    "by", "from", "is", "are", "was", "were", "be", "been", "being", "have", "has",
    "had", "do", "does", "did", "will", "would", "could", "should", "may", "might",
    "shall", "can", "need", "must", "that", "this", "these", "those", "it", "its",
    "my", "your", "his", "her", "our", "their", "which", "who", "whom", "what",
    "where", "when", "how", "why", "all", "each", "every", "both", "few", "more",
    "most", "other", "some", "such", "no", "not", "only", "same", "so", "than",
    "too", "very", "just", "about", "above", "after", "again", "also", "any",
    "based", "using", "used", "via", "across", "along", "among", "around",
    "ai", "powered", "real", "time", "dynamic", "custom", "brand", "voice",
    "personalized", "automated", "social", "media", "multi", "channel",
    "content", "generator", "learning", "generating", "reducing", "manual",
    "effort", "marketing", "hospitality", "businesses", "concept", "explanation",
    "feedback", "responsive", "online", "shopping", "portal", "scheduler",
    "copy", "generation", "roadmaps", "quizzes", "recruitment", "matching",
    "candidates", "information", "analysis", "internal", "built", "hotel",
    "post", "posts", "quick", "app", "router",
}

MONTHS_PATTERN = r'(?:january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|jun|jul|aug|sep|sept|oct|nov|dec)'
# Date pattern for project dates
YEAR_RANGE_PATTERN = re.compile(r'\b(20[0-3]\d|19[7-9]\d)(?:\s*(?:-|–|—|to)\s*(20[0-3]\d|19[7-9]\d|Present|Current))?', re.IGNORECASE)


def _is_non_project_section_header(line: str) -> bool:
    """Check if line matches a known non-project section header or label.

    Normalizes whitespace, trailing colons, slashes, ampersands, and case.
    """
    clean = line.strip().rstrip(":")
    if not clean:
        return False
    # Strip bullet prefix if present
    clean_no_bullet = clean.lstrip("- •*▪◦‣\t").strip()
    norm = clean_no_bullet.lower()

    if norm in _NON_PROJECT_SECTION_KEYWORDS:
        return True

    # Normalize slashes / ampersands / 'and'
    norm_slash = re.sub(r'\s*[/&]\s*', ' & ', norm)
    if norm_slash in _NON_PROJECT_SECTION_KEYWORDS:
        return True

    norm_and = re.sub(r'\s+and\s+', ' & ', norm)
    if norm_and in _NON_PROJECT_SECTION_KEYWORDS:
        return True

    return False


def _extract_techs_from_text(text: str) -> List[str]:
    """Match technologies in text against Day 24 SKILL_DICTIONARY and ALIAS_MAP.

    ONLY returns technologies that are confirmed by the skill dictionary or alias map.
    Does NOT accept arbitrary text fragments as technologies.
    """
    if not text:
        return []

    found_techs: List[str] = []

    # Split by comma or slash or pipe for tech lists e.g. "FastAPI, React, PostgreSQL"
    parts = [p.strip(" ,.-()[]\t\n") for p in re.split(r'[,/|]|(?:\band\b)', text) if p.strip()]
    for part in parts:
        low_part = part.lower()
        if low_part in GENERIC_IGNORE_WORDS or low_part in _COMMON_NON_TECH_WORDS:
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

    # Token scan fallback — only accept dictionary-confirmed tokens
    for token in re.findall(r'\b[A-Za-z0-9+#.-]+\b', text):
        low_tok = token.lower()
        if low_tok in GENERIC_IGNORE_WORDS or low_tok in _COMMON_NON_TECH_WORDS:
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
    "created", "engineered", "maintained", "utilized", "used", "led", "managed", "configured",
    "deployed", "automated", "optimized", "enhanced", "spearheaded", "authored",
    "trained", "achieved", "executed", "collaborated", "constructed", "generated",
    "solved", "delivered", "programmed", "orchestrated", "established", "supervised",
    "reduced", "improved", "accelerated", "scaled", "refactored", "streamlined", "crafted",
    "pioneered", "boosted", "expanded", "wrote", "added", "provided", "handled", "facilitated",
    "architect", "develop", "build", "integrate", "design", "implement", "create",
    "engineer", "maintain", "utilize", "lead", "manage", "configure", "deploy",
    "automate", "optimize", "enhance", "spearhead", "author", "train", "achieve",
    "execute", "collaborate", "construct", "generate", "solve", "deliver", "program",
    "orchestrate", "establish", "supervise", "reduce", "improve", "accelerate",
    "scale", "refactor", "streamline", "craft", "pioneer", "boost", "expand",
    "write", "add", "provide", "handle", "facilitate",
}


TECH_KEYWORDS: Set[str] = {
    "python", "typescript", "javascript", "react", "react.js", "next.js", "nextjs", "node.js",
    "express.js", "fastapi", "django", "flask", "postgresql", "mongodb", "mysql", "redis",
    "docker", "kubernetes", "aws", "azure", "gcp", "tailwind", "prisma", "gemini api", "openai api",
    "pytorch", "tensorflow", "scikit-learn", "opencv", "spacy", "java", "c++", "c#", "html", "css",
    "hugging face", "clerk"
}


_REJECTED_HEADER_LABELS: Set[str] = {
    "projects", "academic projects", "personal projects", "key projects",
    "selected projects", "technical projects", "technologies", "tech stack",
    "tools", "stack", "tech", "description", "details", "overview", "summary",
    "date", "dates", "github", "demo", "live demo", "link", "url", "urls",
    "repo", "source code", "code", "work", "role", "duration", "timeline",
    "links", "reference", "responsibilities", "achievements", "certifications",
    "certificates", "certificate", "certification", "awards", "honors", "accomplishments",
    "extracurricular", "activities", "extracurricular activities",
}

# Section labels that appear as content lines (e.g. "Technologies:", "Description:", "Date:")
_SECTION_CONTENT_LABELS: Set[str] = {
    "technologies", "tech stack", "tools", "stack", "tech",
    "description", "details", "overview", "summary",
    "date", "dates", "duration", "timeline",
    "github", "demo", "live demo", "link", "url", "urls",
    "repo", "source code", "code", "role", "responsibilities",
}

# Generic single words that are very unlikely to be standalone project names
_GENERIC_TITLE_WORDS: Set[str] = {
    "system", "application", "platform", "website", "portal", "dashboard",
    "tool", "project", "module", "service", "solution", "interface",
    "learning", "marketing", "hotel", "management", "certificate", "certification",
    "achievements", "awards", "honors",
}

# Words that commonly appear in description subtitles but not in project titles
_DESCRIPTION_STARTER_WORDS: Set[str] = {
    "a", "an", "the", "for", "with", "using", "based", "powered",
    "via", "through", "within", "across", "about",
}


def _is_pure_date_line(line: str) -> bool:
    """Check if line is purely a date, month-year, or year range."""
    clean = line.strip()
    if not clean:
        return False
    rem = re.sub(r'\b' + MONTHS_PATTERN + r'\b', '', clean, flags=re.IGNORECASE)
    rem = re.sub(r'\b(20[0-3]\d|19[7-9]\d|Present|Current|Ongoing|Now)\b', '', rem, flags=re.IGNORECASE)
    rem = re.sub(r'[\d\s\-–—/.,():to]', '', rem, flags=re.IGNORECASE)
    return len(rem) == 0


def _is_tech_stack_line(line: str) -> bool:
    """Check if line is a comma-separated tech stack listing rather than a project title."""
    clean = line.strip()
    if clean.lower().startswith(("technologies:", "tech stack:", "tools:", "stack:", "tech:")):
        return True
    if ("," in clean or "/" in clean) and ("|" not in clean and "–" not in clean and "—" not in clean and "(" not in clean):
        parts = [p.strip().lower() for p in re.split(r'[,/]', clean) if p.strip()]
        if len(parts) >= 2:
            matched = sum(1 for p in parts if any(k in p for k in TECH_KEYWORDS))
            if matched >= 2:
                return True
            dict_matched = sum(
                1 for p in parts
                if p in ALIAS_MAP or p in SKILL_DICTIONARY
            )
            if dict_matched >= 2 and dict_matched >= len(parts) // 2:
                return True
    return False


def _is_section_content_label(line: str) -> bool:
    """Check if line is a section content label like 'Technologies:', 'Description:', 'Date:'."""
    clean = line.strip()
    if not clean:
        return False
    # Must end with colon or be a known label
    if clean.endswith(":"):
        label = clean[:-1].strip().lower()
        if label in _SECTION_CONTENT_LABELS:
            return True
    return False


def _is_pure_tech_name(text: str) -> bool:
    """Check if text (after stripping bullets) is purely a single technology name."""
    clean = text.strip()
    if not clean:
        return False
    low = clean.lower()
    # Check exact match in dictionaries
    if low in ALIAS_MAP or low in SKILL_DICTIONARY:
        return True
    # Check multi-word tech names (e.g., "Tailwind CSS", "Gemini API", "Hugging Face")
    if low in TECH_KEYWORDS:
        return True
    return False


def _score_project_header(line: str, next_lines: List[str]) -> Tuple[int, str]:
    """Score a candidate line to determine if it is a genuine project title header.

    Returns (score, reason_string) where score >= 3 indicates acceptance.
    Uses both positive and negative signals with context awareness.
    """
    clean = line.strip()
    if not clean:
        return -10, "empty line"

    reasons: List[str] = []
    score = 0

    # ===== HARD REJECTIONS (immediate disqualification) =====

    # Non-project section header guard (Achievements, Certifications, Awards, etc.)
    if _is_non_project_section_header(clean):
        return -10, f"non-project section header guard: {clean}"

    # Bullet prefixes
    if clean.startswith(("-", "*", "•", "▪", "◦", "‣")):
        return -10, "bullet prefix"

    # Numbered bullet like 1. or (1)
    if re.match(r'^(?:\d+[\.)]|\(\d+\))\s+', clean):
        return -10, "numbered bullet"

    # Section title or label
    label_check = clean.lower().rstrip(":")
    if label_check in _REJECTED_HEADER_LABELS:
        return -10, f"rejected label: {label_check}"

    # Section content label (e.g., "Technologies:", "Description:", "Date:")
    if _is_section_content_label(clean):
        return -10, f"section content label: {clean}"

    # Pure date lines
    if _is_pure_date_line(clean):
        return -10, "pure date line"

    # Tech stack line
    if _is_tech_stack_line(clean):
        return -10, "tech stack line"

    # URLs, GitHub links, Demo labels
    if re.search(r'https?://|github\.com|www\.', clean, re.IGNORECASE):
        return -10, "URL/link"
    if clean.lower().startswith(("github:", "demo:", "live demo:", "repo:", "link:", "url:", "source code:")):
        return -10, "link label"

    # Action verbs — description bullets/sentences often start with action verbs
    first_word = clean.split()[0].lower().rstrip(":,.-")
    if first_word in ACTION_VERBS:
        return -10, f"action verb: {first_word}"

    # Ending in period (sentences are descriptions, not titles)
    if clean.endswith("."):
        return -10, "sentence ending with period"

    # Absolute length limits
    if len(clean) > 100:
        return -10, "too long (>100 chars)"

    # ===== NEGATIVE SIGNALS =====

    words = clean.split()
    word_count = len(words)

    # Starts with description-starter word
    if first_word in _DESCRIPTION_STARTER_WORDS:
        score -= 4
        reasons.append(f"starts with description word: {first_word}")

    # Check if too many common English words (sentence-like structure)
    lower_words = [w.lower().rstrip(",.;:") for w in words]
    common_word_count = sum(1 for w in lower_words if w in _COMMON_NON_TECH_WORDS)
    if word_count >= 3 and common_word_count > word_count * 0.6:
        score -= 3
        reasons.append(f"too many common words ({common_word_count}/{word_count})")

    # Generic single-word title
    if word_count == 1 and clean.lower() in _GENERIC_TITLE_WORDS:
        score -= 3
        reasons.append(f"generic single word: {clean}")

    # Long line without separator
    has_separator = bool(re.search(r'[|–—]|\s+-\s+|\([^)]+\)', clean))
    has_colon = ":" in clean and not re.search(r'https?:', clean, re.IGNORECASE)

    if not has_separator and not has_colon:
        if word_count > 6:
            score -= 5
            reasons.append(f"too many words without separator ({word_count})")
        elif word_count > 4:
            score -= 1
            reasons.append(f"moderately long without separator ({word_count})")
    elif has_separator or has_colon:
        if word_count > 12:
            score -= 5
            reasons.append(f"too many words even with separator ({word_count})")

    if len(clean) > 80:
        score -= 2
        reasons.append("long line (>80 chars)")

    # ===== POSITIVE SIGNALS =====

    # Separator structure indicates structured project header
    if has_separator:
        score += 3
        reasons.append("has separator (|/–/—/parens)")

    if has_colon and not _is_section_content_label(clean):
        # Colon separator like "Project Name: Description"
        parts = clean.split(":", 1)
        if len(parts) == 2 and len(parts[0].split()) <= 5:
            score += 2
            reasons.append("colon-separated title")

    # Short distinctive title (1-3 words, no separator needed)
    if 1 <= word_count <= 3 and not has_separator:
        score += 2
        reasons.append(f"short title ({word_count} words)")

    # Title case or all caps (formatting signal)
    if clean[0].isupper() and not clean[0].isdigit():
        score += 1
        reasons.append("starts with uppercase")

    # Context: followed by bullet points
    bullet_followers = sum(1 for nl in next_lines[:5] if nl.strip().startswith(("-", "•", "*", "▪")))
    if bullet_followers >= 2:
        score += 2
        reasons.append(f"followed by {bullet_followers} bullets")

    # Context: followed by a technology line
    for nl in next_lines[:3]:
        nl_clean = nl.strip()
        if _is_tech_stack_line(nl_clean) or _is_section_content_label(nl_clean):
            score += 2
            reasons.append("followed by tech/label line")
            break
        # Bulleted tech name
        stripped = nl_clean.lstrip("- •*▪◦‣\t").strip()
        if stripped and _is_pure_tech_name(stripped):
            score += 1
            reasons.append("followed by tech bullet")
            break

    # Context: followed by a date line
    for nl in next_lines[:4]:
        nl_clean = nl.strip()
        if _is_pure_date_line(nl_clean) or (nl_clean.lstrip("- •*").strip() and _is_pure_date_line(nl_clean.lstrip("- •*").strip())):
            score += 1
            reasons.append("followed by date line")
            break

    reason_str = "; ".join(reasons) if reasons else "no specific signals"
    return score, reason_str


def _is_project_header_line(line: str, next_lines: Optional[List[str]] = None) -> bool:
    """Determine if a line is a genuine project title header.

    Uses the multi-signal scoring system. Threshold = 3.
    """
    if next_lines is None:
        next_lines = []
    score, reason = _score_project_header(line, next_lines)
    is_header = score >= 3

    logger.debug(
        "PROJECT HEADER CANDIDATE: line=%r score=%d accepted=%s reason=%s",
        line.strip()[:80], score, is_header, reason,
    )

    return is_header


def _extract_name_and_techs_from_line(line: str) -> Tuple[Optional[str], List[str], Optional[str]]:
    """Extract project name, embedded technologies, and subtitle from heading line.

    Returns:
        (project_name, technologies_list, subtitle_or_None)
    """
    if not line:
        return None, [], None

    line_clean = line.strip()

    # Parenthesis format e.g. "Resume Analyzer (Python, spaCy, FastAPI)"
    paren_match = re.search(r'^([A-Za-z0-9\s&._-]{2,50})\s*\(([^)]+)\)', line_clean)
    if paren_match:
        name_cand = paren_match.group(1).strip()
        tech_str = paren_match.group(2).strip()
        techs = _extract_techs_from_text(tech_str)
        # If parenthesized content has no tech matches, treat as subtitle
        if not techs:
            return name_cand, [], tech_str
        return name_cand, techs, None

    # Separator format e.g. "Learnify – AI-Powered Learning Platform" or "Talent AI | FastAPI | React"
    if "|" in line_clean or "—" in line_clean or " – " in line_clean or " - " in line_clean:
        parts = [p.strip() for p in re.split(r'[|—–]|\s+-\s+', line_clean) if p.strip()]
        if len(parts) >= 2:
            name_cand = parts[0]
            techs: List[str] = []
            subtitle_parts: List[str] = []

            for p in parts[1:]:
                p_techs = _extract_techs_from_text(p)
                if p_techs:
                    techs.extend(p_techs)
                else:
                    # Non-tech part after separator is subtitle context
                    subtitle_parts.append(p)

            subtitle = " ".join(subtitle_parts) if subtitle_parts else None
            return name_cand, techs, subtitle

    # Colon format e.g. "Talent Platform: Candidate-job matching platform" (ensure it is not a URL)
    if ":" in line_clean and not re.search(r'https?:', line_clean, re.IGNORECASE):
        parts = [p.strip() for p in line_clean.split(":", 1) if p.strip()]
        if len(parts) == 2:
            name_cand = parts[0]
            if len(name_cand) <= 50 and len(name_cand.split()) <= 5:
                techs = _extract_techs_from_text(parts[1])
                subtitle = parts[1] if not techs else None
                return name_cand, techs, subtitle

    return line_clean, [], None


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
            all_lines = [l.strip() for l in sec.content.splitlines() if l.strip()]
            # Filter out section title lines
            lines: List[str] = []
            for l in all_lines:
                if l.lower().rstrip(":") in {"projects", "academic projects", "personal projects", "key projects", "technical projects"}:
                    continue
                lines.append(l)

            # Build blocks using context-aware header scoring with safety boundary check
            curr_block: List[Tuple[str, str, float]] = []
            for idx, l in enumerate(lines):
                # Safety boundary check: terminate project extraction on non-project section header
                if _is_non_project_section_header(l):
                    if curr_block:
                        blocks.append(curr_block)
                        curr_block = []
                    break

                remaining_lines = lines[idx + 1:]
                if _is_project_header_line(l, next_lines=remaining_lines):
                    if curr_block:
                        blocks.append(curr_block)
                        curr_block = []
                curr_block.append((l, sec.name, 0.90))
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

        # Double check: skip if header line is a non-project section header or label
        if _is_non_project_section_header(header_line):
            continue

        if header_line.lower().rstrip(":") in {"projects", "academic projects", "personal projects", "technologies", "tech stack"}:
            if len(block_lines) > 1:
                header_line = block_lines[1]
                block_lines = block_lines[1:]
            else:
                continue

        # Extract name, same-line technologies, and subtitle
        raw_name, same_line_techs, subtitle = _extract_name_and_techs_from_line(header_line)
        if not raw_name or len(raw_name) > 60 or raw_name.endswith("."):
            continue

        # Clean project name
        can_name, norm_name = normalize_project_name(raw_name)
        if not can_name or _is_non_project_section_header(can_name):
            continue

        # Extract technologies from explicit tech lines & block body
        raw_techs: List[str] = list(same_line_techs)
        description_lines: List[str] = []
        start_yr: Optional[int] = None
        end_yr: Optional[int] = None

        # Add subtitle as first description line if present
        if subtitle and subtitle.strip():
            description_lines.append(subtitle.strip())

        for l in block_lines[1:]:
            l_clean = l.strip()
            if not l_clean:
                continue

            # Safety boundary inside block: stop processing if a non-project section header is reached
            if _is_non_project_section_header(l_clean):
                break

            # Skip section content labels (Technologies:, Description:, Date:, etc.)
            if _is_section_content_label(l_clean):
                continue

            # Check explicit technology line e.g. "FastAPI, React, PostgreSQL" or "Technologies: FastAPI, React"
            if l_clean.lower().startswith(("technologies:", "tech stack:", "tools:", "stack:")):
                tech_val = re.sub(r'^(?:technologies|tech stack|tools|stack):\s*', '', l_clean, flags=re.IGNORECASE)
                raw_techs.extend(_extract_techs_from_text(tech_val))
                continue

            # Check date line e.g. "2024 - 2025" or bulleted date "- August 2025"
            date_candidate = l_clean.lstrip("- •*▪◦‣\t").strip()
            if date_candidate:
                date_match = YEAR_RANGE_PATTERN.search(date_candidate)
                if date_match and len(date_candidate) < 30 and not any(kw in date_candidate.lower() for kw in ["system", "platform", "app"]):
                    if _is_pure_date_line(date_candidate):
                        start_yr = int(date_match.group(1))
                        if date_match.group(2) and date_match.group(2).isdigit():
                            end_yr = int(date_match.group(2))
                        continue

            # Strip bullet marker for further analysis
            stripped_content = l_clean.lstrip("- •*▪◦‣\t").strip()
            if not stripped_content:
                continue

            # Check if this is a bulleted pure technology name (e.g., "- Next.js", "- PostgreSQL")
            if l_clean.startswith(("-", "•", "*", "▪", "◦", "‣")) and _is_pure_tech_name(stripped_content):
                raw_techs.extend(_extract_techs_from_text(stripped_content))
                continue

            # Check if standalone line is a list of technologies e.g. "FastAPI, React, PostgreSQL"
            if not l_clean.startswith(("-", "•", "*")):
                extracted_line_techs = _extract_techs_from_text(l_clean)
                if extracted_line_techs and len(l_clean.split(",")) >= 2:
                    raw_techs.extend(extracted_line_techs)
                    continue

            # Description bullet or paragraph line
            if stripped_content and len(stripped_content) > 5:
                description_lines.append(stripped_content)
                # Also extract technologies mentioned inside description line
                raw_techs.extend(_extract_techs_from_text(stripped_content))

        # Normalize technologies
        can_techs, norm_techs = normalize_technologies(raw_techs)

        # Build original verbatim description text
        description_text = " ".join(description_lines)

        # Classify project domain & project type
        classification, project_type = classify_project(can_name, description_text, can_techs)

        # Compute evidence-based confidence
        evidence_count = 0
        if can_name:
            evidence_count += 1
        if can_techs:
            evidence_count += 1
        if description_text and len(description_text) > 20:
            evidence_count += 1
        if start_yr:
            evidence_count += 1
        if subtitle:
            evidence_count += 1

        if evidence_count >= 4:
            confidence = 0.98
        elif evidence_count >= 3:
            confidence = 0.95
        elif evidence_count >= 2:
            confidence = 0.88
        elif evidence_count >= 1:
            confidence = 0.78
        else:
            confidence = 0.65

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
