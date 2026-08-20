"""Comprehensive Test Suite for Phase 4 Day 22: OCR for Scanned PDF Processing.

Tests:
1. Scanned PDF detection (normal, empty, whitespace, sparse, mixed pages)
2. OCR pipeline (render, preprocess, OCR, result integration)
3. Image preprocessing (grayscale, upscale, contrast, threshold, immutability)
4. Error handling (Tesseract unavailable, invalid config, missing language, render failure,
   OCR exception, empty result, all pages fail, partial success)
5. Processing lifecycle (scanned→PROCESSED, OCR unavailable→FAILED, no text→FAILED,
   normal PDF without Tesseract still works)
6. Integration test with real Tesseract (skipped if unavailable)
"""

import asyncio
import io
import sys
import uuid
import pytest
import pymupdf
from datetime import datetime, timezone
from unittest.mock import patch, MagicMock, AsyncMock
from PIL import Image, ImageDraw, ImageFont

from app.services.resume_processing.models import (
    ExtractedDocument,
    DocumentPage,
    DocumentBlock,
    DocumentMetadata,
    OCRMetadata,
)
from app.services.resume_processing.pdf_extractor import extract_pdf_text
from app.services.resume_processing.ocr import (
    check_tesseract_available,
    reset_tesseract_cache,
    detect_ocr_pages,
    render_pdf_page_to_image,
    ocr_single_page,
    process_pdf_with_ocr,
)
from app.services.resume_processing.image_preprocessing import preprocess_image_for_ocr
from app.services.resume_processing.extractor import extract_document
from app.exceptions.resume import ResumeParsingError

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


# ---------------------------------------------------------------------------
# Synthetic Test Document Generators
# ---------------------------------------------------------------------------

def create_normal_text_pdf(pages_text: list[str] = None) -> bytes:
    """Create a valid PDF with real text content on each page."""
    if pages_text is None:
        pages_text = [
            "JOHN DOE\nSenior Software Engineer\n\nEXPERIENCE\nTech Corp - Backend Lead (2021-Present)\n- Architected high-throughput microservices in Python\n\nEDUCATION\nNIT Rourkela - B.Tech (2017-2021)"
        ]
    doc = pymupdf.open()
    for page_idx, text in enumerate(pages_text):
        page = doc.new_page(width=595, height=842)
        y_pos = 70
        for block in text.split("\n\n"):
            page.insert_text((50, y_pos), block, fontsize=12)
            y_pos += 40 + len(block.split("\n")) * 15
    pdf_bytes = doc.write()
    doc.close()
    return pdf_bytes


def create_scanned_pdf(texts: list[str] = None) -> bytes:
    """Create a PDF where each page is a rasterized image (no extractable text layer).

    This simulates a scanned document by drawing text onto images and
    inserting them as full-page images into the PDF.
    """
    if texts is None:
        texts = ["JOHN DOE\nSoftware Engineer\nPython\nFastAPI\nPostgreSQL"]

    doc = pymupdf.open()
    for text in texts:
        # Create image with text
        img = Image.new("RGB", (595, 842), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        y_pos = 80
        for line in text.split("\n"):
            draw.text((60, y_pos), line, fill=(0, 0, 0))
            y_pos += 30

        # Convert PIL Image to bytes
        img_buffer = io.BytesIO()
        img.save(img_buffer, format="PNG")
        img_bytes = img_buffer.getvalue()
        img.close()

        # Insert image as full page
        page = doc.new_page(width=595, height=842)
        page.insert_image(pymupdf.Rect(0, 0, 595, 842), stream=img_bytes)

    pdf_bytes = doc.write()
    doc.close()
    return pdf_bytes


def create_mixed_pdf() -> bytes:
    """Create a PDF with page 1 = normal text, page 2 = scanned image, page 3 = normal text."""
    doc = pymupdf.open()

    # Page 1: Normal text
    page1 = doc.new_page(width=595, height=842)
    page1.insert_text((50, 70), "PAGE 1 NATIVE TEXT", fontsize=14)
    page1.insert_text((50, 100), "This is a normal text page with plenty of content for extraction.", fontsize=11)
    page1.insert_text((50, 120), "Skills: Python, FastAPI, PostgreSQL, Docker, Kubernetes", fontsize=11)

    # Page 2: Scanned image (no text layer)
    img = Image.new("RGB", (595, 842), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.text((60, 80), "SCANNED PAGE 2", fill=(0, 0, 0))
    draw.text((60, 110), "Education: NIT Rourkela", fill=(0, 0, 0))
    img_buffer = io.BytesIO()
    img.save(img_buffer, format="PNG")
    img_bytes = img_buffer.getvalue()
    img.close()

    page2 = doc.new_page(width=595, height=842)
    page2.insert_image(pymupdf.Rect(0, 0, 595, 842), stream=img_bytes)

    # Page 3: Normal text
    page3 = doc.new_page(width=595, height=842)
    page3.insert_text((50, 70), "PAGE 3 NATIVE TEXT", fontsize=14)
    page3.insert_text((50, 100), "Projects: TalentAI - Full-stack resume processing platform", fontsize=11)
    page3.insert_text((50, 120), "Certifications: AWS Solutions Architect, Kubernetes Administrator", fontsize=11)

    pdf_bytes = doc.write()
    doc.close()
    return pdf_bytes


def create_whitespace_pdf() -> bytes:
    """Create a PDF where pages contain only whitespace characters."""
    doc = pymupdf.open()
    page = doc.new_page(width=595, height=842)
    page.insert_text((50, 70), "   ", fontsize=12)  # Only whitespace
    pdf_bytes = doc.write()
    doc.close()
    return pdf_bytes


def create_sparse_text_pdf(char_count: int = 10) -> bytes:
    """Create a PDF with very little text (below threshold)."""
    doc = pymupdf.open()
    page = doc.new_page(width=595, height=842)
    text = "A" * char_count
    page.insert_text((50, 70), text, fontsize=12)
    pdf_bytes = doc.write()
    doc.close()
    return pdf_bytes


def create_test_image(width: int = 400, height: int = 300, mode: str = "RGB") -> Image.Image:
    """Create a simple test image with text for preprocessing tests."""
    img = Image.new(mode, (width, height), color=(255, 255, 255) if mode != "RGBA" else (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.text((20, 20), "Test Resume Text", fill=(0, 0, 0) if mode != "RGBA" else (0, 0, 0, 255))
    draw.text((20, 50), "Python Developer", fill=(0, 0, 0) if mode != "RGBA" else (0, 0, 0, 255))
    return img


# ---------------------------------------------------------------------------
# Test Runner
# ---------------------------------------------------------------------------

async def run_resume_ocr_tests():
    print("\n============================================================", flush=True)
    print("RUNNING RESUME OCR TESTS (DAY 22)", flush=True)
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
    # SECTION 1: Scanned PDF Detection
    # -------------------------------------------------------------------
    print("\n--- Section 1: Scanned PDF Detection ---", flush=True)

    # 1. Normal text PDF → OCR not required
    normal_pdf = create_normal_text_pdf()
    native_doc = extract_pdf_text(normal_pdf)
    ocr_meta = detect_ocr_pages(native_doc.pages, normal_pdf, min_chars_per_page=30)
    check(ocr_meta.ocr_required is False, "Normal text PDF → OCR not required")

    # 2. Scanned PDF (no text) → OCR required
    scanned_pdf = create_scanned_pdf()
    scanned_doc = extract_pdf_text(scanned_pdf)
    ocr_meta_scanned = detect_ocr_pages(scanned_doc.pages, scanned_pdf, min_chars_per_page=30)
    check(ocr_meta_scanned.ocr_required is True, "Scanned PDF (no text) → OCR required")
    check(1 in ocr_meta_scanned.pages_requiring_ocr, "Scanned page 1 flagged for OCR")

    # 3. Whitespace-only PDF → OCR required
    ws_pdf = create_whitespace_pdf()
    ws_doc = extract_pdf_text(ws_pdf)
    ws_meta = detect_ocr_pages(ws_doc.pages, ws_pdf, min_chars_per_page=30)
    check(ws_meta.ocr_required is True, "Whitespace-only PDF → OCR required")

    # 4. Sparse text PDF → OCR required
    sparse_pdf = create_sparse_text_pdf(char_count=10)
    sparse_doc = extract_pdf_text(sparse_pdf)
    sparse_meta = detect_ocr_pages(sparse_doc.pages, sparse_pdf, min_chars_per_page=30)
    check(sparse_meta.ocr_required is True, "Sparse text PDF (10 chars) → OCR required")

    # 5. Mixed PDF: page 1 native, page 2 scanned, page 3 native
    mixed_pdf = create_mixed_pdf()
    mixed_doc = extract_pdf_text(mixed_pdf)
    mixed_meta = detect_ocr_pages(mixed_doc.pages, mixed_pdf, min_chars_per_page=30)
    check(mixed_meta.ocr_required is True, "Mixed PDF → OCR required")
    check(2 in mixed_meta.pages_requiring_ocr, "Mixed PDF: page 2 flagged for OCR")
    check(1 not in mixed_meta.pages_requiring_ocr, "Mixed PDF: page 1 NOT flagged for OCR")
    check(3 not in mixed_meta.pages_requiring_ocr, "Mixed PDF: page 3 NOT flagged for OCR")

    # -------------------------------------------------------------------
    # SECTION 2: OCR Pipeline
    # -------------------------------------------------------------------
    print("\n--- Section 2: OCR Pipeline ---", flush=True)

    # 6. Render page to image
    normal_pdf_for_render = create_normal_text_pdf(["Render test content here"])
    rendered_img = render_pdf_page_to_image(normal_pdf_for_render, page_index=0, dpi=150)
    check(isinstance(rendered_img, Image.Image), "Render page to image returns PIL Image")
    check(rendered_img.mode == "RGB", "Rendered image is RGB mode")
    check(rendered_img.size[0] > 0 and rendered_img.size[1] > 0, "Rendered image has valid dimensions")
    rendered_img.close()

    # 7. Preprocess image
    test_img = create_test_image()
    preprocessed = preprocess_image_for_ocr(test_img, upscale_factor=2.0, threshold_value=180)
    check(isinstance(preprocessed, Image.Image), "Preprocess image returns PIL Image")
    check(preprocessed.mode == "L", "Preprocessed image is grayscale (L mode)")
    test_img.close()
    preprocessed.close()

    # 8-11. OCR with mocked Tesseract
    mock_image = create_test_image()
    with patch("app.services.resume_processing.ocr.check_tesseract_available", return_value=True):
        with patch("pytesseract.image_to_string", return_value="JOHN DOE\nSoftware Engineer") as mock_its:
            with patch("pytesseract.image_to_data", return_value={"conf": [90, 85, 88]}) as mock_itd:
                text, conf = ocr_single_page(mock_image, lang="eng", psm=6)
                check("JOHN DOE" in text, "OCR returns expected text")
                check(conf is not None and conf > 80, f"OCR confidence is reasonable (got {conf})")
    mock_image.close()

    # OCR result integration into ExtractedDocument
    scanned_pdf_test = create_scanned_pdf(["ALICE SMITH\nData Scientist"])
    scanned_native = extract_pdf_text(scanned_pdf_test)

    with patch("app.services.resume_processing.ocr.check_tesseract_available", return_value=True):
        with patch("app.services.resume_processing.ocr.ocr_single_page", return_value=("ALICE SMITH\nData Scientist", 92.5)):
            hybrid_doc = process_pdf_with_ocr(scanned_pdf_test, scanned_native)
            check("ALICE SMITH" in hybrid_doc.text, "OCR text inserted into ExtractedDocument")
            ocr_page = hybrid_doc.pages[0]
            check(ocr_page.extraction_method == "ocr", "OCR page extraction_method is 'ocr'")

    # Native pages remain native
    mixed_native = extract_pdf_text(mixed_pdf)
    with patch("app.services.resume_processing.ocr.check_tesseract_available", return_value=True):
        with patch("app.services.resume_processing.ocr.ocr_single_page", return_value=("OCR PAGE 2 TEXT", 88.0)):
            hybrid_mixed = process_pdf_with_ocr(mixed_pdf, mixed_native)
            page1 = hybrid_mixed.pages[0]
            page2 = hybrid_mixed.pages[1]
            page3 = hybrid_mixed.pages[2]
            check(page1.extraction_method == "native", "Mixed: page 1 remains extraction_method='native'")
            check(page2.extraction_method == "ocr", "Mixed: page 2 is extraction_method='ocr'")
            check(page3.extraction_method == "native", "Mixed: page 3 remains extraction_method='native'")
            check(hybrid_mixed.extraction_method == "hybrid", "Mixed doc extraction_method is 'hybrid'")

    # -------------------------------------------------------------------
    # SECTION 3: Image Preprocessing
    # -------------------------------------------------------------------
    print("\n--- Section 3: Image Preprocessing ---", flush=True)

    # 12. Grayscale conversion
    rgb_img = create_test_image(mode="RGB")
    gray = preprocess_image_for_ocr(rgb_img, apply_threshold=False)
    check(gray.mode == "L", "RGB image converted to grayscale")
    rgb_img.close()
    gray.close()

    # 13. Upscaling behavior (small image)
    small_img = create_test_image(width=200, height=150)
    upscaled = preprocess_image_for_ocr(small_img, upscale_factor=2.0, apply_threshold=False)
    check(upscaled.size[0] == 400 and upscaled.size[1] == 300, "Small image upscaled by 2x")
    small_img.close()
    upscaled.close()

    # Large image should NOT be upscaled
    large_img = create_test_image(width=2000, height=1500)
    not_upscaled = preprocess_image_for_ocr(large_img, upscale_factor=2.0, apply_threshold=False)
    check(not_upscaled.size[0] == 2000, "Large image not upscaled")
    large_img.close()
    not_upscaled.close()

    # 14. Contrast enhancement (image should be different from raw grayscale)
    contrast_img = create_test_image(width=200, height=150)
    enhanced = preprocess_image_for_ocr(contrast_img, apply_threshold=False)
    raw_gray = contrast_img.convert("L")
    # Pixel values should differ due to contrast enhancement
    check(enhanced.tobytes() != raw_gray.tobytes(), "Contrast enhancement modifies pixel values")
    contrast_img.close()
    enhanced.close()
    raw_gray.close()

    # 15. Thresholding produces binary image
    thresh_img = create_test_image(width=200, height=150)
    binarized = preprocess_image_for_ocr(thresh_img, threshold_value=128, apply_threshold=True)
    unique_pixels = set(binarized.tobytes())
    check(unique_pixels.issubset({0, 255}), "Thresholded image contains only 0 and 255 values")
    thresh_img.close()
    binarized.close()

    # 16. Original image is NOT mutated
    original = create_test_image(width=300, height=200)
    original_data = original.tobytes()
    _ = preprocess_image_for_ocr(original)
    check(original.tobytes() == original_data, "Original image is not mutated by preprocessing")
    original.close()

    # RGBA image handling
    rgba_img = create_test_image(width=300, height=200, mode="RGBA")
    rgba_result = preprocess_image_for_ocr(rgba_img, apply_threshold=False)
    check(rgba_result.mode == "L", "RGBA image correctly processed to grayscale")
    rgba_img.close()
    rgba_result.close()

    # -------------------------------------------------------------------
    # SECTION 4: Error Handling
    # -------------------------------------------------------------------
    print("\n--- Section 4: Error Handling ---", flush=True)

    # 17. Tesseract unavailable
    reset_tesseract_cache()
    with patch("app.services.resume_processing.ocr.check_tesseract_available", return_value=False):
        try:
            ocr_single_page(create_test_image(), lang="eng", psm=6)
            check(False, "Tesseract unavailable raises ResumeParsingError")
        except ResumeParsingError as e:
            check("OCR processing is unavailable" in str(e), "Tesseract unavailable raises ResumeParsingError")
    reset_tesseract_cache()

    # 18. Tesseract command invalid
    with patch("app.services.resume_processing.ocr.check_tesseract_available", return_value=True):
        with patch("pytesseract.image_to_string", side_effect=Exception("tesseract is not found")):
            try:
                ocr_single_page(create_test_image(), lang="eng", psm=6)
                check(False, "Invalid Tesseract command raises ResumeParsingError")
            except ResumeParsingError as e:
                check("not properly installed" in str(e), "Invalid Tesseract command raises safe error")

    # 19. Missing language data
    with patch("app.services.resume_processing.ocr.check_tesseract_available", return_value=True):
        with patch("pytesseract.image_to_string", side_effect=Exception("Failed loading language 'xyz'")):
            try:
                ocr_single_page(create_test_image(), lang="xyz", psm=6)
                check(False, "Missing language data raises ResumeParsingError")
            except ResumeParsingError as e:
                check("missing language data" in str(e), "Missing language data raises safe error")

    # 20. PDF rendering failure
    try:
        render_pdf_page_to_image(b"NOT A PDF", page_index=0, dpi=150)
        check(False, "Invalid PDF for rendering raises ResumeParsingError")
    except ResumeParsingError:
        check(True, "Invalid PDF for rendering raises ResumeParsingError")

    # Out of range page
    try:
        valid_pdf = create_normal_text_pdf(["test"])
        render_pdf_page_to_image(valid_pdf, page_index=99, dpi=150)
        check(False, "Out-of-range page raises ResumeParsingError")
    except ResumeParsingError:
        check(True, "Out-of-range page raises ResumeParsingError")

    # 21. OCR exception (generic)
    with patch("app.services.resume_processing.ocr.check_tesseract_available", return_value=True):
        with patch("pytesseract.image_to_string", side_effect=RuntimeError("Unexpected OCR crash")):
            try:
                ocr_single_page(create_test_image(), lang="eng", psm=6)
                check(False, "Generic OCR exception raises ResumeParsingError")
            except ResumeParsingError as e:
                check("unexpected error" in str(e).lower(), "Generic OCR exception produces safe message")

    # 22. Empty OCR result
    scanned_empty = create_scanned_pdf([""])
    scanned_empty_native = extract_pdf_text(scanned_empty)
    with patch("app.services.resume_processing.ocr.check_tesseract_available", return_value=True):
        with patch("app.services.resume_processing.ocr.ocr_single_page", return_value=("", None)):
            try:
                process_pdf_with_ocr(scanned_empty, scanned_empty_native)
                check(False, "Empty OCR result for all pages raises ResumeParsingError")
            except ResumeParsingError as e:
                check("No readable text" in str(e), "Empty OCR result produces controlled error")

    # 23. All pages produce no usable text
    multi_scanned = create_scanned_pdf(["page1_scan", "page2_scan"])
    multi_native = extract_pdf_text(multi_scanned)
    with patch("app.services.resume_processing.ocr.check_tesseract_available", return_value=True):
        with patch("app.services.resume_processing.ocr.ocr_single_page", return_value=("  ", None)):
            try:
                process_pdf_with_ocr(multi_scanned, multi_native)
                check(False, "All pages empty raises ResumeParsingError")
            except ResumeParsingError as e:
                check("No readable text" in str(e), "All pages empty produces controlled error")

    # 24. One OCR page fails while others succeed
    mixed_for_partial = create_scanned_pdf(["page1_text", "page2_text"])
    mixed_partial_native = extract_pdf_text(mixed_for_partial)

    call_count = [0]
    def side_effect_partial(*args, **kwargs):
        call_count[0] += 1
        if call_count[0] == 1:
            return ("FIRST PAGE OCR TEXT with enough characters for extraction", 90.0)
        raise ResumeParsingError("OCR failed for page 2")

    with patch("app.services.resume_processing.ocr.check_tesseract_available", return_value=True):
        with patch("app.services.resume_processing.ocr.ocr_single_page", side_effect=side_effect_partial):
            result = process_pdf_with_ocr(mixed_for_partial, mixed_partial_native)
            check(result.pages[0].character_count > 0, "Partial OCR: first page succeeded")
            check(result.pages[1].character_count == 0, "Partial OCR: second page recorded as failed")
            check(result.ocr_metadata is not None, "Partial OCR: metadata present")
            check(2 in result.ocr_metadata.pages_ocr_failed, "Partial OCR: failed page tracked in metadata")

    # -------------------------------------------------------------------
    # SECTION 5: Processing Flow
    # -------------------------------------------------------------------
    print("\n--- Section 5: Processing Flow ---", flush=True)

    # 25. Successful scanned PDF → extract_document returns PROCESSED-compatible result
    with patch("app.services.resume_processing.ocr.check_tesseract_available", return_value=True):
        with patch("app.services.resume_processing.ocr.ocr_single_page", return_value=("SCANNED TEXT EXTRACTED SUCCESSFULLY with sufficient length", 91.0)):
            scanned_result = extract_document(scanned_pdf, extension=".pdf", mime_type="application/pdf")
            check(scanned_result.has_extractable_text is True, "Scanned PDF: has_extractable_text is True after OCR")
            check(scanned_result.character_count > 0, "Scanned PDF: character count > 0 after OCR")

    # 26. OCR unavailable for scanned PDF → should raise ResumeParsingError
    with patch("app.services.resume_processing.ocr.check_tesseract_available", return_value=False):
        try:
            extract_document(scanned_pdf, extension=".pdf")
            check(False, "Scanned PDF with OCR unavailable raises ResumeParsingError")
        except ResumeParsingError as e:
            check("OCR processing is required" in str(e), "Scanned PDF without Tesseract → controlled error")

    # 27. OCR produces no readable text → FAILED
    with patch("app.services.resume_processing.ocr.check_tesseract_available", return_value=True):
        with patch("app.services.resume_processing.ocr.ocr_single_page", return_value=("", None)):
            try:
                extract_document(scanned_pdf, extension=".pdf")
                check(False, "OCR with no readable text raises ResumeParsingError")
            except ResumeParsingError as e:
                check("No readable text" in str(e), "No readable OCR text → controlled error")

    # 28. Normal PDF with Tesseract unavailable → still processes successfully
    with patch("app.services.resume_processing.ocr.check_tesseract_available", return_value=False):
        normal_result = extract_document(normal_pdf, extension=".pdf")
        check(normal_result.has_extractable_text is True, "Normal PDF still works without Tesseract")
        check(normal_result.character_count > 0, "Normal PDF has text without Tesseract")
        check(normal_result.ocr_metadata is not None, "Normal PDF has OCR metadata (with ocr_required=False)")
        check(normal_result.ocr_metadata.ocr_required is False, "Normal PDF OCR not required")

    # 29. extract_document still works for DOCX (unchanged)
    import docx as python_docx
    docx_doc = python_docx.Document()
    docx_doc.add_paragraph("DOCX Resume Test")
    buf = io.BytesIO()
    docx_doc.save(buf)
    docx_bytes = buf.getvalue()
    docx_result = extract_document(docx_bytes, extension=".docx")
    check(docx_result.document_type == "docx", "DOCX extraction still works (Day 21 backward compatible)")

    # 30. Extraction method annotations on normal PDF pages
    annotated = extract_document(normal_pdf, extension=".pdf")
    check(all(p.extraction_method == "native" for p in annotated.pages), "All normal PDF pages annotated as 'native'")

    # -------------------------------------------------------------------
    # SECTION 6: Integration Test (Real Tesseract)
    # -------------------------------------------------------------------
    print("\n--- Section 6: Integration Test (Real Tesseract) ---", flush=True)

    reset_tesseract_cache()
    tesseract_available = check_tesseract_available()

    if tesseract_available:
        # 31. Real OCR integration test
        scanned_resume = create_scanned_pdf([
            "JOHN DOE\nSoftware Engineer\nPython\nFastAPI\nPostgreSQL"
        ])
        try:
            real_result = extract_document(scanned_resume, extension=".pdf")
            # Check that some recognizable text was extracted
            has_recognizable = any(
                keyword in real_result.text.upper()
                for keyword in ["JOHN", "DOE", "SOFTWARE", "ENGINEER", "PYTHON", "FASTAPI", "POSTGRESQL"]
            )
            check(has_recognizable, "Real Tesseract OCR extracts recognizable text from scanned PDF")
            check(real_result.ocr_metadata is not None, "Real OCR: metadata populated")
            check(real_result.ocr_metadata.ocr_required is True, "Real OCR: ocr_required=True")
            check(len(real_result.ocr_metadata.pages_ocr_succeeded) > 0, "Real OCR: pages_ocr_succeeded populated")
            check(
                real_result.ocr_metadata.ocr_processing_duration_seconds is not None and
                real_result.ocr_metadata.ocr_processing_duration_seconds > 0,
                "Real OCR: processing duration recorded"
            )
        except Exception as e:
            check(False, f"Real Tesseract integration test failed: {e}")
    else:
        print("  SKIP [31] Real Tesseract integration test (Tesseract not available)", flush=True)

    # -------------------------------------------------------------------
    # Summary
    # -------------------------------------------------------------------
    print(f"\n============================================================", flush=True)
    print(f"RESUME OCR TESTS: {passed} passed, {failed} failed, {total} total", flush=True)
    print(f"============================================================", flush=True)

    if failed > 0:
        sys.exit(1)


@pytest.mark.asyncio
async def test_resume_ocr():
    await run_resume_ocr_tests()


if __name__ == "__main__":
    asyncio.run(run_resume_ocr_tests())

