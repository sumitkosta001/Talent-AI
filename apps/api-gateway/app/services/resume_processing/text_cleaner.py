"""Text cleaning and extraction noise removal module for Day 23.

Provides functions to clean raw extracted text, normalize Unicode, line endings,
bullets, and dashes, and conservatively filter out document extraction noise
(page numbers, repeated headers/footers, decorative line dividers).

Crucially preserves technical terms (C++, C#, .NET, Node.js, React.js, CI/CD),
emails, phone numbers, URLs, dates, and all meaningful resume details.
"""

import re
import unicodedata
from typing import List, Tuple, Optional, Set
import logging

from .models import DocumentPage

logger = logging.getLogger("talentai.resume_processing.text_cleaner")

# Bullet characters to normalize
BULLET_CHARS_PATTERN = re.compile(r'^[ \t]*[•▪◦‣⁃\*\-][ \t]+')

# Common dash variants (en-dash, em-dash, minus sign)
DASH_VARIANTS_PATTERN = re.compile(r'[\u2010\u2011\u2012\u2013\u2014\u2015\u2212]')

# Decorative separator line pattern (4+ repeated symbols)
DECORATIVE_LINE_PATTERN = re.compile(r'^[ \t]*[-=*_~.#/]{4,}[ \t]*$')

# Page number patterns (conservative matching to avoid deleting resume metrics)
PAGE_NUMBER_PATTERNS = [
    re.compile(r'^[ \t]*page[ \t]+\d+([ \t]+of[ \t]+\d+)?[ \t]*$', re.IGNORECASE),
    re.compile(r'^[ \t]*\d+[ \t]*/[ \t]*\d+[ \t]*$'),
    re.compile(r'^[ \t]*\d+[ \t]+of[ \t]+\d+[ \t]*$', re.IGNORECASE),
    re.compile(r'^[ \t]*-\[?[ \t]*\d+[ \t]*\]?-[ \t]*$'),
    re.compile(r'^[ \t]*--[ \t]*\d+[ \t]*--[ \t]*$'),
    re.compile(r'^[ \t]*\[[ \t]*\d+[ \t]*\][ \t]*$'),
]

# Standalone single/double digit page numbers on isolated lines (e.g. line is just "1" or "2")
STANDALONE_DIGIT_PAGE_PATTERN = re.compile(r'^[ \t]*\d{1,2}[ \t]*$')


def clean_text(text: str) -> str:
    """Perform primary text cleaning and Unicode normalization.

    Args:
        text: Raw text string from extraction or OCR.

    Returns:
        Cleaned, normalized text string.
    """
    if not text:
        return ""

    # 1. Normalize line endings (CRLF -> LF, CR -> LF)
    cleaned = text.replace("\r\n", "\n").replace("\r", "\n")

    # 2. Strip null bytes and non-printable control characters (keep \n and \t)
    cleaned = "".join(
        ch for ch in cleaned
        if ch in ("\n", "\t") or not unicodedata.category(ch).startswith("C")
    )

    # 3. Unicode NFKC normalization (normalizes combined characters & full-width forms safely)
    cleaned = unicodedata.normalize("NFKC", cleaned)

    # 4. Normalize dash variants to standard ASCII hyphen '-'
    cleaned = DASH_VARIANTS_PATTERN.sub("-", cleaned)

    # 5. Process line by line
    lines = cleaned.split("\n")
    cleaned_lines = []

    for line in lines:
        # Strip trailing/leading horizontal whitespace
        line_str = line.strip()

        # Normalize bullet prefix if present
        if BULLET_CHARS_PATTERN.match(line_str):
            line_str = BULLET_CHARS_PATTERN.sub("• ", line_str)

        # Collapse multiple horizontal spaces/tabs within line
        line_str = re.sub(r'[ \t]{2,}', ' ', line_str)

        cleaned_lines.append(line_str)

    # Rejoin lines
    result = "\n".join(cleaned_lines)

    # 6. Collapse excessive blank lines (more than 2 consecutive newlines -> 2 newlines)
    result = re.sub(r'\n{3,}', '\n\n', result)

    return result.strip()


def remove_extraction_noise(text: str, pages: Optional[List[DocumentPage]] = None) -> Tuple[str, int]:
    """Remove PDF/OCR extraction noise such as page numbers, repeated headers/footers, and divider lines.

    Args:
        text: Cleaned text string.
        pages: Optional list of DocumentPage objects for positional/per-page repeated header checks.

    Returns:
        Tuple of (denoised_text, removed_lines_count).
    """
    if not text:
        return "", 0

    lines = text.split("\n")
    removed_count = 0
    denoised_lines: List[str] = []

    # Detect repeated header/footer lines across pages if page breakdown exists
    repeated_page_lines: Set[str] = set()
    if pages and len(pages) > 1:
        repeated_page_lines = _detect_repeated_headers_footers(pages)

    for line in lines:
        line_strip = line.strip()
        if not line_strip:
            denoised_lines.append("")
            continue

        # 1. Check decorative divider lines (e.g. "--------------------")
        if DECORATIVE_LINE_PATTERN.match(line_strip):
            removed_count += 1
            logger.debug("Removed decorative line noise: '%s'", line_strip)
            continue

        # 2. Check explicitly matched page number formats
        is_page_num = any(pat.match(line_strip) for pat in PAGE_NUMBER_PATTERNS)
        if is_page_num:
            removed_count += 1
            logger.debug("Removed page number line: '%s'", line_strip)
            continue

        # 3. Check standalone 1-2 digit page numbers (e.g. line is just "1" or "2")
        # Ensure it is not a year (4 digits) or experience count (e.g. "10+ years")
        if STANDALONE_DIGIT_PAGE_PATTERN.match(line_strip):
            val = int(line_strip)
            if 1 <= val <= 99:  # Standalone single/double digit page number on its own line
                removed_count += 1
                logger.debug("Removed standalone page digit line: '%s'", line_strip)
                continue

        # 4. Check repeated header/footer lines detected across pages
        if line_strip.lower() in repeated_page_lines:
            removed_count += 1
            logger.debug("Removed repeated header/footer line: '%s'", line_strip)
            continue

        denoised_lines.append(line_strip)

    # Rejoin and collapse consecutive blank lines
    result_text = "\n".join(denoised_lines)
    result_text = re.sub(r'\n{3,}', '\n\n', result_text).strip()

    return result_text, removed_count


def _detect_repeated_headers_footers(pages: List[DocumentPage]) -> Set[str]:
    """Detect lines that repeat at page boundaries across multiple pages (e.g. candidate name header).

    Args:
        pages: List of DocumentPage objects.

    Returns:
        Set of lowercased line strings to remove.
    """
    first_last_lines_per_page: List[List[str]] = []

    for page in pages:
        if not page.text:
            continue
        p_lines = [l.strip() for l in page.text.split("\n") if l.strip()]
        if not p_lines:
            continue

        candidates = []
        # First 2 lines of page (header area)
        candidates.extend(p_lines[:2])
        # Last 2 lines of page (footer area)
        candidates.extend(p_lines[-2:])

        first_last_lines_per_page.append([c.lower() for c in candidates])

    if len(first_last_lines_per_page) < 2:
        return set()

    # Find lines present in header/footer area of AT LEAST 2 pages
    line_counts: dict = {}
    for page_cands in first_last_lines_per_page:
        for cand in set(page_cands):
            # Exclude very short generic words or numbers from header removal
            if len(cand) > 3 and not cand.isdigit():
                line_counts[cand] = line_counts.get(cand, 0) + 1

    repeated_lines = {line for line, count in line_counts.items() if count >= 2}
    return repeated_lines
