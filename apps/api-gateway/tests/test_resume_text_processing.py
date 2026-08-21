"""Comprehensive Test Suite for Phase 4 Day 23: Text Processing, Normalization, Section Detection, Noise Removal, and Tokenization.

Tests:
1. Text cleaning (CRLF, control chars, Unicode NFKC, bullets, dashes, line whitespace, blank lines)
2. Extraction noise removal (standalone page numbers, "Page X of Y", repeated headers/footers, decorative lines)
3. Information preservation (emails, phone numbers, URLs, C++, C#, .NET, Node.js, React.js, Next.js, CI/CD, dates, CGPA)
4. Normalization (case-preserving normalized_text, lowercase_text, idempotency, non-mutation of ExtractedDocument)
5. Section detection (canonical taxonomy, aliases, heading scoring, section boundaries, line/page references, UNKNOWN fallback, false-positive protection)
6. Tokenization (technical terms intact, emails, URLs, dates, normalized lowercase tokens, no stopword removal, no stemming/lemmatization)
7. Integration (native PDF, OCR, mixed documents)
8. Pytest compatibility
"""

import asyncio
import io
import sys
from pathlib import Path
from typing import List

_root_dir = str(Path(__file__).resolve().parent.parent)
if _root_dir not in sys.path:
    sys.path.insert(0, _root_dir)

import pytest

from app.services.resume_processing.models import (
    ExtractedDocument,
    DocumentPage,
    DocumentBlock,
    DocumentMetadata,
    OCRMetadata,
    ProcessedSection,
    ProcessedResumeText,
)
from app.services.resume_processing.text_cleaner import clean_text, remove_extraction_noise
from app.services.resume_processing.section_detector import detect_sections, SECTION_ALIASES
from app.services.resume_processing.tokenizer import tokenize_resume_text
from app.services.resume_processing.text_processor import process_extracted_document
from app.exceptions.resume import ResumeParsingError

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def create_synthetic_extracted_document(
    text: str = None,
    document_type: str = "pdf",
    extraction_method: str = "pymupdf",
    page_count: int = 1,
) -> ExtractedDocument:
    """Create a synthetic ExtractedDocument for Day 23 testing."""
    if text is None:
        text = (
            "JOHN DOE\n"
            "Software Engineer\n"
            "john.doe@example.com | +91 9876543210 | https://github.com/johndoe\n\n"
            "PROFESSIONAL SUMMARY\n"
            "Full-stack software engineer with 3+ years of experience in Python, FastAPI, C++, .NET, Node.js, and React.js.\n\n"
            "TECHNICAL SKILLS\n"
            "• Languages: Python, C++, C#, JavaScript, TypeScript\n"
            "• Frameworks: FastAPI, Node.js, React.js, Next.js, .NET\n"
            "• Tools: Docker, Kubernetes, CI/CD, PostgreSQL, MongoDB\n\n"
            "WORK EXPERIENCE\n"
            "Senior Backend Lead | Tech Corp | 2022 - Present\n"
            "- Built high-throughput microservices using FastAPI and PostgreSQL\n"
            "- Implemented CI/CD pipelines and Docker deployments\n\n"
            "EDUCATION\n"
            "B.Tech in Computer Science | NIT Rourkela | 2018 - 2022\n"
            "CGPA: 8.7 / 10.0\n\n"
            "PROJECTS\n"
            "TalentAI Recruitment Platform\n"
            "Built AI backend processing resumes using Python, FastAPI, and C++.\n\n"
            "CERTIFICATIONS\n"
            "AWS Certified Solutions Architect (2023)\n"
        )

    pages = [
        DocumentPage(
            page_number=1,
            text=text,
            blocks=[DocumentBlock(text=text, block_index=0)],
            character_count=len(text),
            word_count=len(text.split()),
            has_extractable_text=True,
            extraction_method=extraction_method,
        )
    ]

    return ExtractedDocument(
        text=text,
        document_type=document_type,
        extraction_method=extraction_method,
        page_count=page_count,
        pages=pages,
        metadata=DocumentMetadata(title="Synthetic Candidate Resume", author="John Doe"),
        character_count=len(text),
        word_count=len(text.split()),
        has_extractable_text=True,
    )


async def run_resume_text_processing_tests():
    print("\n============================================================", flush=True)
    print("RUNNING RESUME TEXT PROCESSING TESTS (DAY 23)", flush=True)
    print("============================================================", flush=True)

    passed = 0
    failed = 0
    total = 0

    def check(condition: bool, test_name: str, detail: str = ""):
        nonlocal passed, failed, total
        total += 1
        if condition:
            passed += 1
            print(f"  PASS [{total:02d}] {test_name}", flush=True)
        else:
            failed += 1
            print(f"  FAIL [{total:02d}] {test_name} - {detail}", flush=True)

    # -------------------------------------------------------------------
    # SECTION 1: Text Cleaning & Unicode Normalization
    # -------------------------------------------------------------------
    print("\n--- Section 1: Text Cleaning & Unicode Normalization ---", flush=True)

    # 1. CRLF normalization
    crlf_input = "Line 1\r\nLine 2\rLine 3\nLine 4"
    cleaned_crlf = clean_text(crlf_input)
    check("\r" not in cleaned_crlf and cleaned_crlf == "Line 1\nLine 2\nLine 3\nLine 4", "CRLF and CR normalized to LF")

    # 2. Control character removal (preserving \n and \t)
    ctrl_input = "Hello\x00 World\x07!\nTabbed\tText\x1b"
    cleaned_ctrl = clean_text(ctrl_input)
    check("\x00" not in cleaned_ctrl and "\x07" not in cleaned_ctrl and "\x1b" not in cleaned_ctrl, "Null bytes and non-printable control chars stripped")
    check("\n" in cleaned_ctrl and "\t" in cleaned_ctrl, "Newlines and tabs preserved during control char cleaning")

    # 3. Unicode NFKC normalization
    unicode_input = "Python\uFB01 (ligature) \uFF13.\uFF11\uFF12 (full-width numbers)"
    cleaned_unicode = clean_text(unicode_input)
    check("Pythonfi" in cleaned_unicode and "3.12" in cleaned_unicode, "Unicode NFKC normalization resolves ligatures & full-width characters")

    # 4. Bullet normalization
    bullet_input = "▪ Bullet 1\n◦ Bullet 2\n‣ Bullet 3\n* Bullet 4\n- Bullet 5"
    cleaned_bullets = clean_text(bullet_input)
    bullet_lines = cleaned_bullets.split("\n")
    check(all(line.startswith("• ") for line in bullet_lines), "Bullet characters (▪, ◦, ‣, *, -) normalized to standard '•'")

    # 5. Dash normalization
    dash_input = "2021–2025 (en-dash) | 2022—2024 (em-dash) | 5−3 (minus)"
    cleaned_dashes = clean_text(dash_input)
    check("2021-2025" in cleaned_dashes and "2022-2024" in cleaned_dashes and "5-3" in cleaned_dashes, "Dash variants (en-dash, em-dash, minus) normalized to ASCII hyphen '-'")

    # 6. Whitespace collapse and line trimming
    ws_input = "  Line 1 with   multiple   spaces   \n\n\n\nLine 2 after  quadruple newlines  "
    cleaned_ws = clean_text(ws_input)
    check("Line 1 with multiple spaces" in cleaned_ws, "Trailing/leading line whitespace trimmed and internal multiple spaces collapsed")
    check("\n\n\n" not in cleaned_ws, "Excessive blank lines (>2) collapsed to 2 newlines")

    # -------------------------------------------------------------------
    # SECTION 2: Extraction Noise Removal
    # -------------------------------------------------------------------
    print("\n--- Section 2: Extraction Noise Removal ---", flush=True)

    # 7. Page number removal ("Page 1", "Page 2 of 3", "1 / 2")
    page_num_text = "JOHN DOE\nPage 1\nSKILLS\nPython\nPage 2 of 3\nEXPERIENCE\n1 / 2\nTech Corp"
    denoised_page_num, removed_count = remove_extraction_noise(page_num_text)
    check("Page 1" not in denoised_page_num and "Page 2 of 3" not in denoised_page_num and "1 / 2" not in denoised_page_num, "Explicit page numbers ('Page 1', 'Page 2 of 3', '1 / 2') removed")
    check(removed_count == 3, "Correct count of page number noise lines reported")

    # 8. Standalone single/double digit page numbers
    standalone_text = "Header\n1\nSection Content\n2\nFooter"
    denoised_digits, _ = remove_extraction_noise(standalone_text)
    check("\n1\n" not in f"\n{denoised_digits}\n" and "\n2\n" not in f"\n{denoised_digits}\n", "Standalone single/double digit page number lines removed")

    # 9. Preservation of resume metrics (years, experience count)
    metrics_text = "EXPERIENCE\n2024\n3 years of experience\n10+ years"
    denoised_metrics, _ = remove_extraction_noise(metrics_text)
    check("2024" in denoised_metrics and "3 years of experience" in denoised_metrics and "10+ years" in denoised_metrics, "Resume metrics (years '2024', '3 years', '10+ years') preserved")

    # 10. Decorative line removal
    decor_text = "SUMMARY\n--------------------\nBackend Engineer\n====================\nSKILLS"
    denoised_decor, decor_removed = remove_extraction_noise(decor_text)
    check("--------------------" not in denoised_decor and "====================" not in denoised_decor, "Decorative line dividers (----, ====) removed")
    check(decor_removed == 2, "Decorative line removal count tracked correctly")

    # 11. Repeated header/footer removal across pages
    page1 = DocumentPage(page_number=1, text="JOHN DOE RESUME\nPage Header\nSUMMARY\nPython Developer\nPage Footer", blocks=[])
    page2 = DocumentPage(page_number=2, text="Page Header\nEXPERIENCE\nTech Lead\nPage Footer", blocks=[])
    combined_pages_text = f"{page1.text}\n\n{page2.text}"
    denoised_repeated, rep_count = remove_extraction_noise(combined_pages_text, pages=[page1, page2])
    check("Page Header" not in denoised_repeated and "Page Footer" not in denoised_repeated, "Repeated headers/footers across pages identified and removed")

    # -------------------------------------------------------------------
    # SECTION 3: Information & Technical Terms Preservation
    # -------------------------------------------------------------------
    print("\n--- Section 3: Information & Technical Terms Preservation ---", flush=True)

    # 12. Contact details & URLs preserved
    contact_sample = "Contact: john.doe@example.com | +91-9876543210 | https://github.com/johndoe | https://linkedin.com/in/johndoe"
    cleaned_contact = clean_text(contact_sample)
    check("john.doe@example.com" in cleaned_contact, "Email address preserved")
    check("+91-9876543210" in cleaned_contact, "Phone number preserved")
    check("https://github.com/johndoe" in cleaned_contact, "GitHub URL preserved")
    check("https://linkedin.com/in/johndoe" in cleaned_contact, "LinkedIn URL preserved")

    # 13. Technical terms preserved intact
    tech_sample = "Proficient in C++, C#, .NET, Node.js, React.js, Next.js, Vue.js, CI/CD, FastAPI, PostgreSQL."
    cleaned_tech = clean_text(tech_sample)
    check("C++" in cleaned_tech, "C++ technical term preserved")
    check("C#" in cleaned_tech, "C# technical term preserved")
    check(".NET" in cleaned_tech, ".NET technical term preserved")
    check("Node.js" in cleaned_tech, "Node.js technical term preserved")
    check("React.js" in cleaned_tech, "React.js technical term preserved")
    check("Next.js" in cleaned_tech, "Next.js technical term preserved")
    check("CI/CD" in cleaned_tech, "CI/CD technical term preserved")

    # 14. CGPA and degree dates preserved
    academic_sample = "B.Tech in Computer Science (2018 - 2022) | CGPA: 8.7 / 10.0"
    cleaned_academic = clean_text(academic_sample)
    check("2018 - 2022" in cleaned_academic, "Degree date range preserved")
    check("CGPA: 8.7 / 10.0" in cleaned_academic, "CGPA score preserved")

    # -------------------------------------------------------------------
    # SECTION 4: Section Detection & Taxonomy
    # -------------------------------------------------------------------
    print("\n--- Section 4: Section Detection & Taxonomy ---", flush=True)

    # 15. Section detection on full synthetic document
    doc_fixture = create_synthetic_extracted_document()
    sections = detect_sections(doc_fixture.text, doc=doc_fixture)
    section_names = [s.name for s in sections]

    check("SUMMARY" in section_names, "SUMMARY section detected")
    check("SKILLS" in section_names, "SKILLS section detected")
    check("EXPERIENCE" in section_names, "EXPERIENCE section detected")
    check("EDUCATION" in section_names, "EDUCATION section detected")
    check("PROJECTS" in section_names, "PROJECTS section detected")
    check("CERTIFICATIONS" in section_names, "CERTIFICATIONS section detected")

    # 16. Section ordering preserved
    expected_order = ["UNKNOWN", "SUMMARY", "SKILLS", "EXPERIENCE", "EDUCATION", "PROJECTS", "CERTIFICATIONS"]
    check(section_names == expected_order, f"Section sequence matches document order ({section_names})")

    # 17. Section alias mapping checks
    alias_text = "CAREER HISTORY\nTech Corp - Software Engineer\n\nACADEMIC BACKGROUND\nNIT Rourkela - B.Tech\n\nCORE COMPETENCIES\nPython, FastAPI"
    alias_sections = detect_sections(alias_text)
    alias_names = [s.name for s in alias_sections]
    check("EXPERIENCE" in alias_names, "Alias 'CAREER HISTORY' mapped to EXPERIENCE")
    check("EDUCATION" in alias_names, "Alias 'ACADEMIC BACKGROUND' mapped to EDUCATION")
    check("SKILLS" in alias_names, "Alias 'CORE COMPETENCIES' mapped to SKILLS")

    # 18. False-positive protection for single tech keyword line
    false_pos_text = "SKILLS\nPYTHON\nFASTAPI\nPOSTGRESQL\n\nEXPERIENCE\nSoftware Engineer"
    fp_sections = detect_sections(false_pos_text)
    fp_names = [s.name for s in fp_sections]
    check("SKILLS" in fp_names and "EXPERIENCE" in fp_names, "SKILLS and EXPERIENCE sections detected")
    check("PYTHON" not in fp_names and "FASTAPI" not in fp_names, "Single tech keyword lines ('PYTHON', 'FASTAPI') NOT misclassified as sections")

    # 19. Section confidence scores
    skills_sec = [s for s in sections if s.name == "SKILLS"][0]
    check(skills_sec.confidence >= 0.70, f"Detected section has high confidence score (got {skills_sec.confidence})")
    check(skills_sec.start_line > 0 and skills_sec.end_line >= skills_sec.start_line, "Section start_line and end_line bounds are valid")

    # 20. UNKNOWN fallback section for unassigned content
    unknown_text = "Jane Doe\nFreelance Software Consultant\n\nSKILLS\nPython"
    un_sections = detect_sections(unknown_text)
    check(un_sections[0].name == "UNKNOWN", "Initial content before first section header assigned to UNKNOWN section")

    # -------------------------------------------------------------------
    # SECTION 5: Tokenization
    # -------------------------------------------------------------------
    print("\n--- Section 5: Tokenization ---", flush=True)

    # 21. Tokenization preserving technical terms
    sample_text = "Senior Software Engineer proficient in C++, C#, .NET, Node.js, React.js, Next.js, and CI/CD."
    tokens, norm_tokens = tokenize_resume_text(sample_text)

    check("C++" in tokens, "C++ preserved as single case-preserved token")
    check("c++" in norm_tokens, "c++ present in normalized lowercase tokens")
    check("C#" in tokens and "c#" in norm_tokens, "C# / c# tokenized properly")
    check(".NET" in tokens and ".net" in norm_tokens, ".NET / .net tokenized properly")
    check("Node.js" in tokens and "node.js" in norm_tokens, "Node.js / node.js tokenized properly")
    check("React.js" in tokens and "react.js" in norm_tokens, "React.js / react.js tokenized properly")
    check("CI/CD" in tokens and "ci/cd" in norm_tokens, "CI/CD / ci/cd tokenized properly")

    # 22. Email and URL tokenization
    email_url_sample = "Contact john.doe@example.com or visit https://github.com/johndoe."
    eu_tokens, _ = tokenize_resume_text(email_url_sample)
    check("john.doe@example.com" in eu_tokens, "Email tokenized as single intact token")
    check("https://github.com/johndoe" in eu_tokens, "URL tokenized as single intact token")

    # 23. Version & Date tokenization
    version_sample = "Python 3.12 and v2.4.1 released in 2024-05."
    ver_tokens, _ = tokenize_resume_text(version_sample)
    check("3.12" in ver_tokens or "Python 3.12" in ver_tokens, "Version number tokenized intact")
    check("2024-05" in ver_tokens or "2024" in ver_tokens, "Date string tokenized intact")

    # 24. No stopword removal or stemming
    stopword_sample = "The engineer is working at Google with Python."
    sw_tokens, _ = tokenize_resume_text(stopword_sample)
    check("The" in sw_tokens and "is" in sw_tokens and "with" in sw_tokens, "Stopwords ('The', 'is', 'with') NOT removed at Day 23")

    # -------------------------------------------------------------------
    # SECTION 6: Full Pipeline Orchestration (`process_extracted_document`)
    # -------------------------------------------------------------------
    print("\n--- Section 6: Full Pipeline Orchestration ---", flush=True)

    # 25. Process extracted document returns ProcessedResumeText
    doc_input = create_synthetic_extracted_document()
    proc_result = process_extracted_document(doc_input)

    check(isinstance(proc_result, ProcessedResumeText), "process_extracted_document returns ProcessedResumeText instance")
    check(len(proc_result.cleaned_text) > 0, "cleaned_text is populated")
    check(len(proc_result.normalized_text) > 0, "normalized_text is populated")
    check(proc_result.lowercase_text == proc_result.normalized_text.lower(), "lowercase_text matches lowercased normalized_text")
    check(len(proc_result.sections) > 0, "sections list is populated")
    check(len(proc_result.tokens) > 0, "tokens list is populated")
    check(len(proc_result.normalized_tokens) == len(proc_result.tokens), "normalized_tokens count matches tokens count")

    # 26. Non-mutation of original ExtractedDocument
    original_text_before = doc_input.text
    original_char_count_before = doc_input.character_count
    _ = process_extracted_document(doc_input)
    check(doc_input.text == original_text_before, "Original ExtractedDocument text is NOT mutated")
    check(doc_input.character_count == original_char_count_before, "Original ExtractedDocument character_count is NOT mutated")
    check(proc_result.original_document is doc_input, "ProcessedResumeText retains reference to original ExtractedDocument")

    # 27. Idempotency & determinism
    proc_result_1 = process_extracted_document(doc_input)
    proc_result_2 = process_extracted_document(doc_input)
    check(proc_result_1.cleaned_text == proc_result_2.cleaned_text, "Pipeline is idempotent (cleaned_text matches)")
    check(len(proc_result_1.sections) == len(proc_result_2.sections), "Pipeline is idempotent (sections count matches)")
    check(proc_result_1.tokens == proc_result_2.tokens, "Pipeline is idempotent (tokens list matches)")

    # 28. OCR ExtractedDocument integration
    ocr_doc = create_synthetic_extracted_document(extraction_method="ocr")
    proc_ocr = process_extracted_document(ocr_doc)
    check(proc_ocr.metadata["extraction_method"] == "ocr", "OCR ExtractedDocument pipeline integration successful")

    # 29. Hybrid ExtractedDocument integration
    hybrid_doc = create_synthetic_extracted_document(extraction_method="hybrid")
    proc_hybrid = process_extracted_document(hybrid_doc)
    check(proc_hybrid.metadata["extraction_method"] == "hybrid", "Hybrid ExtractedDocument pipeline integration successful")

    # 30. Error handling for None document
    try:
        process_extracted_document(None)
        check(False, "None ExtractedDocument raises ResumeParsingError")
    except ResumeParsingError as e:
        check("ExtractedDocument is None" in str(e) or "Cannot process" in str(e), "None ExtractedDocument raises controlled ResumeParsingError")

    # 31. Error handling for empty document text
    empty_doc = create_synthetic_extracted_document(text="")
    try:
        process_extracted_document(empty_doc)
        check(False, "Empty ExtractedDocument text raises ResumeParsingError")
    except ResumeParsingError as e:
        check("contains no readable text" in str(e), "Empty ExtractedDocument raises controlled ResumeParsingError")

    # -------------------------------------------------------------------
    # Summary
    # -------------------------------------------------------------------
    print(f"\n============================================================", flush=True)
    print(f"RESUME TEXT PROCESSING TESTS: {passed} passed, {failed} failed, {total} total", flush=True)
    print(f"============================================================", flush=True)

    if failed > 0:
        sys.exit(1)


@pytest.mark.asyncio
async def test_resume_text_processing():
    await run_resume_text_processing_tests()


if __name__ == "__main__":
    asyncio.run(run_resume_text_processing_tests())
