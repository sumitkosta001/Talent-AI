"""Unified Text Processing Orchestrator for Day 23.

Orchestrates the Day 23 NLP text processing pipeline:
ExtractedDocument (Day 21/22)
  └─> Text Cleaning
       └─> Extraction Noise Removal
            └─> Section Detection
                 └─> Tokenization
                      └─> ProcessedResumeText

Idempotent, deterministic, and preserves the original ExtractedDocument intact.
"""

import time
import logging
from typing import Dict, Any

from app.exceptions.resume import ResumeParsingError
from .models import ExtractedDocument, ProcessedResumeText
from .text_cleaner import clean_text, remove_extraction_noise
from .section_detector import detect_sections
from .tokenizer import tokenize_resume_text

logger = logging.getLogger("talentai.resume_processing.text_processor")


def process_extracted_document(doc: ExtractedDocument | None) -> ProcessedResumeText:
    """Process an ExtractedDocument into a clean, normalized, structured ProcessedResumeText.

    This function does NOT mutate the input ExtractedDocument instance.

    Args:
        doc: ExtractedDocument instance from Day 21/22 extraction.

    Returns:
        ProcessedResumeText containing clean text, normalized representations,
        sections, tokens, and metadata.

    Raises:
        ResumeParsingError: If doc is None or input document contains no text.
    """
    if doc is None:
        logger.error("Text processing rejected: ExtractedDocument is None.")
        raise ResumeParsingError("Cannot process text of a None document.")

    if not doc.text or len(doc.text.strip()) == 0:
        logger.warning("Text processing rejected: ExtractedDocument contains no text.")
        raise ResumeParsingError("The extracted document contains no readable text.")

    start_time = time.time()

    # Step 1: Text cleaning & Unicode NFKC normalization
    cleaned_raw = clean_text(doc.text)

    # Step 2: Removal of extraction noise (page numbers, repeated headers/footers, dividers)
    denoised_text, noise_lines_removed = remove_extraction_noise(cleaned_raw, pages=doc.pages)

    if not denoised_text:
        denoised_text = cleaned_raw  # Fallback to cleaned text if denoising stripped everything

    # Step 3: Normalization representations
    normalized_text = denoised_text
    lowercase_text = normalized_text.lower()

    # Step 4: Section detection
    try:
        sections = detect_sections(text=normalized_text, doc=doc)
    except Exception as sec_exc:
        logger.warning("Section detection encountered error, falling back to UNKNOWN section: %s", str(sec_exc))
        from .models import ProcessedSection
        sections = [
            ProcessedSection(
                name="UNKNOWN",
                title="Unassigned Content",
                content=normalized_text,
                confidence=1.0,
                start_line=1,
                end_line=len(normalized_text.split("\n")),
                page_number=1,
            )
        ]

    # Step 5: Tokenization (case-preserved & lowercase normalized)
    try:
        tokens, normalized_tokens = tokenize_resume_text(normalized_text)
    except Exception as tok_exc:
        logger.warning("Tokenization encountered error, using simple whitespace fallback: %s", str(tok_exc))
        tokens = normalized_text.split()
        normalized_tokens = [t.lower() for t in tokens]

    duration = round(time.time() - start_time, 4)

    # Step 6: Assemble processing metadata
    metadata: Dict[str, Any] = {
        "character_count": len(normalized_text),
        "word_count": len(tokens),
        "line_count": len(normalized_text.split("\n")),
        "section_count": len(sections),
        "detected_sections": [s.name for s in sections],
        "noise_lines_removed": noise_lines_removed,
        "processing_duration_seconds": duration,
        "document_type": doc.document_type,
        "extraction_method": doc.extraction_method,
    }

    logger.info(
        "Text processing complete: doc_type=%s, method=%s, chars=%d, words=%d, "
        "sections=%d (%s), noise_removed=%d, duration=%.4fs",
        doc.document_type, doc.extraction_method, len(normalized_text),
        len(tokens), len(sections), ", ".join(s.name for s in sections),
        noise_lines_removed, duration,
    )

    return ProcessedResumeText(
        cleaned_text=denoised_text,
        normalized_text=normalized_text,
        lowercase_text=lowercase_text,
        sections=sections,
        tokens=tokens,
        normalized_tokens=normalized_tokens,
        metadata=metadata,
        original_document=doc,
    )
