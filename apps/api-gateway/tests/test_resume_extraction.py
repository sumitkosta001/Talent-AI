"""Comprehensive Test Suite for Phase 4 Day 21: Resume Text & Structure Extraction.

Tests:
1. PyMuPDF PDF text extraction (valid text, multi-page, page boundaries, blocks, coordinates, metadata)
2. Scanned / empty PDF detection (has_extractable_text signal for Day 22 OCR)
3. PDF error handling (empty content, corrupted bytes, 0 pages)
4. python-docx DOCX text extraction (paragraphs, heading styles, tables, rows/cells, core metadata)
5. DOCX error handling (empty content, corrupted bytes, invalid zip structure)
6. Unified document dispatcher (PDF routing, DOCX routing, unsupported extensions, unsupported MIME types)
7. End-to-end API processing lifecycle with real extraction (UPLOADED -> PROCESSING -> PROCESSED)
8. End-to-end extraction failure handling (corrupted document -> FAILED with safe failure_reason)
9. Retry processing lifecycle after failure
10. Security, auth, candidate isolation, and invariant preservation
"""

import asyncio
import io
import sys
import uuid
import pytest
import docx
import pymupdf
from datetime import datetime, timezone
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch, AsyncMock

from app.main import app
from app.database.session import SessionLocal
from app.models.user import User
from app.models.enums import UserRole, ResumeStatus
from app.models.resume import Resume
from app.exceptions.resume import ResumeParsingError
from app.services.resume_processing import (
    extract_document,
    extract_pdf_text,
    extract_docx_text,
    ExtractedDocument,
    DocumentPage,
    DocumentBlock,
    DocumentParagraph,
    DocumentTable,
)

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


# ---------------------------------------------------------------------------
# Synthetic Test Document Generators
# ---------------------------------------------------------------------------

def create_synthetic_pdf(
    pages_text: list[str] = None,
    title: str = "Candidate Resume",
    author: str = "Test Candidate",
) -> bytes:
    """Create a valid in-memory PDF with specified pages and metadata."""
    if pages_text is None:
        pages_text = [
            "JOHN DOE\nSenior Software Engineer\n\nEXPERIENCE\nTech Corp - Backend Lead (2021-Present)\n- Architected high-throughput microservices in Python\n\nEDUCATION\nNIT Rourkela - B.Tech (2017-2021)"
        ]

    doc = pymupdf.open()
    for page_idx, text in enumerate(pages_text):
        page = doc.new_page(width=595, height=842)  # A4 size
        # Insert header
        page.insert_text((50, 70), f"Page {page_idx + 1}", fontsize=10)
        # Insert body blocks
        y_pos = 110
        for block in text.split("\n\n"):
            page.insert_text((50, y_pos), block, fontsize=12)
            y_pos += 40 + len(block.split("\n")) * 15

    doc.set_metadata({
        "title": title,
        "author": author,
        "subject": "Curriculum Vitae",
        "creator": "TalentAI Synthetic Generator",
    })

    pdf_bytes = doc.write()
    doc.close()
    return pdf_bytes


def create_synthetic_docx(
    paragraphs: list[tuple[str, str | None]] = None,
    tables_data: list[list[list[str]]] = None,
    title: str = "Candidate Resume",
    author: str = "Test Candidate",
) -> bytes:
    """Create a valid in-memory DOCX with paragraphs, headings, tables, and metadata."""
    doc = docx.Document()

    # Core Properties
    doc.core_properties.title = title
    doc.core_properties.author = author

    if paragraphs is None:
        paragraphs = [
            ("ALICE SMITH", "Title"),
            ("Full Stack Developer", "Subtitle"),
            ("EXPERIENCE", "Heading 1"),
            ("Senior Engineer at CloudCorp (2020-Present)\nLed frontend and backend development in TypeScript and FastAPI.", "Normal"),
            ("EDUCATION", "Heading 1"),
            ("National Institute of Technology - Computer Science (2016-2020)", "Normal"),
        ]

    for text, style in paragraphs:
        if style:
            try:
                doc.add_paragraph(text, style=style)
            except Exception:
                doc.add_paragraph(text)
        else:
            doc.add_paragraph(text)

    if tables_data:
        for t_data in tables_data:
            if not t_data:
                continue
            num_rows = len(t_data)
            num_cols = max(len(row) for row in t_data) if num_rows > 0 else 0
            table = doc.add_table(rows=num_rows, cols=num_cols)
            for r_idx, row_values in enumerate(t_data):
                for c_idx, val in enumerate(row_values):
                    table.cell(r_idx, c_idx).text = val

    buf = io.BytesIO()
    doc.save(buf)
    return buf.getvalue()


# ---------------------------------------------------------------------------
# Test Runner
# ---------------------------------------------------------------------------

async def run_resume_extraction_tests():
    patcher = patch("app.services.email_service.EmailService.send_verification_email", new_callable=AsyncMock)
    patcher.start()

    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        print("\n============================================================", flush=True)
        print("RUNNING RESUME TEXT & STRUCTURE EXTRACTION TESTS (DAY 21)", flush=True)
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
        # SECTION 1: PDF Extractor Unit Tests
        # -------------------------------------------------------------------
        print("\n--- Section 1: PDF Text & Structure Extraction ---", flush=True)

        # 1. Valid single-page PDF
        pdf_bytes_1 = create_synthetic_pdf(
            ["JOHN DOE\nSoftware Engineer\n\nSKILLS\nPython, FastAPI, Docker"],
            title="John Doe CV",
            author="John Doe",
        )
        res_pdf = extract_pdf_text(pdf_bytes_1)
        check(isinstance(res_pdf, ExtractedDocument), "PDF extraction returns ExtractedDocument")
        check(res_pdf.document_type == "pdf", "PDF document_type is 'pdf'")
        check(res_pdf.extraction_method == "pymupdf", "PDF extraction_method is 'pymupdf'")
        check(res_pdf.page_count == 1, "PDF page_count is 1")
        check(len(res_pdf.pages) == 1, "PDF pages list length is 1")
        check("JOHN DOE" in res_pdf.text, "PDF full text contains candidate name")
        check("FastAPI" in res_pdf.text, "PDF full text contains extracted skills")
        check(res_pdf.has_extractable_text is True, "PDF has_extractable_text is True")
        check(res_pdf.character_count > 20, "PDF character_count is accurately computed")
        check(res_pdf.word_count > 5, "PDF word_count is accurately computed")

        # 2. Block preservation and coordinates
        first_page = res_pdf.pages[0]
        check(first_page.page_number == 1, "Page number is 1-indexed")
        check(len(first_page.blocks) >= 2, "Page blocks list preserves multiple text blocks")
        first_block = first_page.blocks[0]
        check(isinstance(first_block, DocumentBlock), "Block is instance of DocumentBlock")
        check(first_block.bbox is not None and len(first_block.bbox) == 4, "Block preserves (x0, y0, x1, y1) bounding box")
        check(first_block.block_index == 0, "First block index is 0")

        # 3. Multi-page PDF
        multi_page_pdf = create_synthetic_pdf(
            [
                "PAGE 1 CONTENT\nCandidate Experience Section\nGoogle - Staff Engineer",
                "PAGE 2 CONTENT\nEducation & Certifications\nNIT Rourkela - Gold Medalist",
                "PAGE 3 CONTENT\nOpen Source Projects\nTalentAI - Contributor",
            ],
            title="Multi-page Resume",
        )
        res_multi = extract_pdf_text(multi_page_pdf)
        check(res_multi.page_count == 3, "Multi-page PDF page_count is 3")
        check(len(res_multi.pages) == 3, "Multi-page PDF preserves all 3 page objects")
        check(res_multi.pages[0].page_number == 1 and "PAGE 1" in res_multi.pages[0].text, "Page 1 contains Page 1 text")
        check(res_multi.pages[1].page_number == 2 and "PAGE 2" in res_multi.pages[1].text, "Page 2 contains Page 2 text")
        check(res_multi.pages[2].page_number == 3 and "PAGE 3" in res_multi.pages[2].text, "Page 3 contains Page 3 text")
        check("--- Page Break ---" in res_multi.text, "Normalized full text preserves page break boundaries")

        # 4. Metadata extraction
        check(res_pdf.metadata.title == "John Doe CV", "PDF metadata title extracted")
        check(res_pdf.metadata.author == "John Doe", "PDF metadata author extracted")

        # 5. Scanned / Empty PDF (has_extractable_text signal for Day 22 OCR)
        doc_blank = pymupdf.open()
        doc_blank.new_page(width=595, height=842)
        blank_pdf_bytes = doc_blank.write()
        doc_blank.close()
        res_blank = extract_pdf_text(blank_pdf_bytes)
        check(res_blank.has_extractable_text is False, "Blank/Scanned PDF correctly flags has_extractable_text=False")
        check(res_blank.character_count == 0, "Blank PDF character_count is 0")

        # 6. PDF Error handling
        try:
            extract_pdf_text(b"")
            check(False, "Empty PDF bytes raises ResumeParsingError")
        except ResumeParsingError:
            check(True, "Empty PDF bytes raises ResumeParsingError")

        try:
            extract_pdf_text(b"%PDF-1.4 this is completely corrupted content and not a real pdf structure")
            check(False, "Corrupted PDF raises ResumeParsingError")
        except ResumeParsingError:
            check(True, "Corrupted PDF raises ResumeParsingError")

        # -------------------------------------------------------------------
        # SECTION 2: DOCX Extractor Unit Tests
        # -------------------------------------------------------------------
        print("\n--- Section 2: DOCX Text & Structure Extraction ---", flush=True)

        # 7. Valid DOCX with headings and paragraphs
        docx_bytes_1 = create_synthetic_docx(
            paragraphs=[
                ("EMILY CHEN", "Title"),
                ("Machine Learning Engineer", "Subtitle"),
                ("WORK EXPERIENCE", "Heading 1"),
                ("AI Research Scientist at Meta (2022-2025)\nTrained large multimodal transformer models.", "Normal"),
                ("EDUCATION", "Heading 1"),
                ("IIT Bombay - M.Tech AI (2020-2022)", "Normal"),
            ],
            title="Emily Chen Resume",
            author="Emily Chen",
        )
        res_docx = extract_docx_text(docx_bytes_1)
        check(isinstance(res_docx, ExtractedDocument), "DOCX extraction returns ExtractedDocument")
        check(res_docx.document_type == "docx", "DOCX document_type is 'docx'")
        check(res_docx.extraction_method == "python-docx", "DOCX extraction_method is 'python-docx'")
        check("EMILY CHEN" in res_docx.text, "DOCX full text contains candidate name")
        check("WORK EXPERIENCE" in res_docx.text, "DOCX full text contains headings")
        check(len(res_docx.paragraphs) >= 5, "DOCX paragraphs list contains all extracted paragraphs")
        check(res_docx.has_extractable_text is True, "DOCX has_extractable_text is True")

        # 8. Heading style detection
        heading_paras = [p for p in res_docx.paragraphs if p.is_heading]
        check(len(heading_paras) >= 3, "DOCX detects Title, Subtitle, and Heading styles")
        check(any(p.text == "WORK EXPERIENCE" for p in heading_paras), "Heading 1 WORK EXPERIENCE correctly flagged as heading")

        # 9. Table extraction
        table_data = [
            ["Skill Category", "Proficiency", "Years of Experience"],
            ["Python / FastAPI", "Expert", "5 Years"],
            ["PostgreSQL / Redis", "Advanced", "4 Years"],
            ["Machine Learning", "Proficient", "3 Years"],
        ]
        docx_with_table = create_synthetic_docx(
            paragraphs=[("SKILLS SUMMARY", "Heading 1")],
            tables_data=[table_data],
        )
        res_table_docx = extract_docx_text(docx_with_table)
        check(len(res_table_docx.tables) == 1, "DOCX table count is 1")
        first_table = res_table_docx.tables[0]
        check(isinstance(first_table, DocumentTable), "Table is instance of DocumentTable")
        check(len(first_table.rows) == 4, "Table has 4 rows")
        check(len(first_table.rows[0].cells) == 3, "Table row 0 has 3 cells")
        check(first_table.rows[1].cells[0].text == "Python / FastAPI", "Table cell value preserved")
        check("Skill Category | Proficiency | Years of Experience" in res_table_docx.text, "Table text representation merged into normalized document text")

        # 10. Multiple tables
        multi_table_docx = create_synthetic_docx(
            tables_data=[
                [["Project", "Role"], ["TalentAI", "Lead Architect"]],
                [["Degree", "Year"], ["B.Tech", "2024"]],
            ]
        )
        res_multi_tbl = extract_docx_text(multi_table_docx)
        check(len(res_multi_tbl.tables) == 2, "Multiple tables in DOCX extracted (count=2)")

        # 11. DOCX Error handling
        try:
            extract_docx_text(b"")
            check(False, "Empty DOCX bytes raises ResumeParsingError")
        except ResumeParsingError:
            check(True, "Empty DOCX bytes raises ResumeParsingError")

        try:
            extract_docx_text(b"PK\x03\x04 fake corrupted zip data that is not a valid openxml document")
            check(False, "Corrupted DOCX raises ResumeParsingError")
        except ResumeParsingError:
            check(True, "Corrupted DOCX raises ResumeParsingError")

        # -------------------------------------------------------------------
        # SECTION 3: Unified Dispatcher Unit Tests
        # -------------------------------------------------------------------
        print("\n--- Section 3: Document Dispatcher ---", flush=True)

        disp_pdf = extract_document(pdf_bytes_1, extension=".pdf", mime_type="application/pdf")
        check(disp_pdf.document_type == "pdf", "Dispatcher routes .pdf to PDF extractor")

        disp_docx = extract_document(docx_bytes_1, extension=".docx", mime_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        check(disp_docx.document_type == "docx", "Dispatcher routes .docx to DOCX extractor")

        # Extension without leading dot
        disp_pdf_nodot = extract_document(pdf_bytes_1, extension="pdf")
        check(disp_pdf_nodot.document_type == "pdf", "Dispatcher handles extension without leading dot ('pdf')")

        # Unsupported extension
        try:
            extract_document(b"fake text content", extension=".txt")
            check(False, "Unsupported extension .txt raises ResumeParsingError")
        except ResumeParsingError:
            check(True, "Unsupported extension .txt raises ResumeParsingError")

        # Unsupported MIME
        try:
            extract_document(b"fake image content", extension=".png", mime_type="image/png")
            check(False, "Unsupported MIME image/png raises ResumeParsingError")
        except ResumeParsingError:
            check(True, "Unsupported MIME image/png raises ResumeParsingError")

        # -------------------------------------------------------------------
        # SECTION 4: Integration with Resume Service & Processing Lifecycle
        # -------------------------------------------------------------------
        print("\n--- Section 4: End-to-End Extraction & Processing Lifecycle ---", flush=True)

        # Setup Candidate A & Candidate B
        rand_id = uuid.uuid4().hex[:8]
        cand_a_email = f"extract_cand_a_{rand_id}@example.com"
        cand_b_email = f"extract_cand_b_{rand_id}@example.com"
        password = "Password123!"

        reg_a = await client.post("/api/v1/auth/register", json={
            "email": cand_a_email,
            "password": password,
            "confirm_password": password,
            "first_name": "Extract",
            "last_name": "TesterA",
        })
        check(reg_a.status_code == 201, "Candidate A registration returns 201")
        user_a_id = uuid.UUID(reg_a.json()["user"]["id"])

        reg_b = await client.post("/api/v1/auth/register", json={
            "email": cand_b_email,
            "password": password,
            "confirm_password": password,
            "first_name": "Extract",
            "last_name": "TesterB",
        })
        check(reg_b.status_code == 201, "Candidate B registration returns 201")
        user_b_id = uuid.UUID(reg_b.json()["user"]["id"])

        # Mark users as verified CANDIDATE in database
        async with SessionLocal() as db:
            for uid in [user_a_id, user_b_id]:
                u = await db.get(User, uid)
                if u:
                    u.is_verified = True
                    u.role = UserRole.CANDIDATE
            await db.commit()

        login_a = await client.post("/api/v1/auth/login", json={"email": cand_a_email, "password": password})
        token_a = login_a.json()["tokens"]["access_token"]
        headers_a = {"Authorization": f"Bearer {token_a}"}

        login_b = await client.post("/api/v1/auth/login", json={"email": cand_b_email, "password": password})
        token_b = login_b.json()["tokens"]["access_token"]
        headers_b = {"Authorization": f"Bearer {token_b}"}

        # Initialize candidate profiles
        await client.get("/api/v1/candidates/me", headers=headers_a)
        await client.get("/api/v1/candidates/me", headers=headers_b)

        # 12. Upload Valid PDF and execute real processing
        valid_pdf_content = create_synthetic_pdf([
            "ROBERT BRUCE\nStaff Infrastructure Engineer\n\nEXPERIENCE\nKubernetes, Cloud Architecture, Python, Go\nAmazon Web Services (2019-2024)"
        ])
        pdf_upload = await client.post(
            "/api/v1/candidates/me/resumes",
            headers=headers_a,
            files={"file": ("robert_resume.pdf", io.BytesIO(valid_pdf_content), "application/pdf")},
        )
        check(pdf_upload.status_code == 201, "PDF upload returns 201")
        pdf_id = pdf_upload.json()["resume"]["id"]
        check(pdf_upload.json()["resume"]["status"] == "uploaded", "Initial status is 'uploaded'")

        # Process the uploaded PDF -> Real PyMuPDF extraction takes place
        proc_res = await client.post(f"/api/v1/candidates/me/resumes/{pdf_id}/process", headers=headers_a)
        check(proc_res.status_code == 200, "Process PDF returns 200")
        check(proc_res.json()["success"] is True, "Process PDF response success is True")
        check(proc_res.json()["resume"]["status"] == "processed", "PDF status transitioned to 'processed'")
        check(proc_res.json()["resume"]["processing_completed_at"] is not None, "processing_completed_at is populated")
        check(proc_res.json()["resume"]["failure_reason"] is None, "failure_reason is None on success")

        # 13. Upload Valid DOCX and execute real processing
        valid_docx_content = create_synthetic_docx(
            paragraphs=[
                ("SARAH CONNOR", "Title"),
                ("Principal Security Engineer", "Subtitle"),
                ("EXPERIENCE", "Heading 1"),
                ("Cyberdyne Systems - Lead Vulnerability Assessor (2021-2025)", "Normal"),
            ],
            tables_data=[[["Tool", "Skill"], ["Ghidra", "Expert"], ["Wireshark", "Advanced"]]],
        )
        docx_upload = await client.post(
            "/api/v1/candidates/me/resumes",
            headers=headers_a,
            files={"file": ("sarah_resume.docx", io.BytesIO(valid_docx_content), "application/vnd.openxmlformats-officedocument.wordprocessingml.document")},
        )
        check(docx_upload.status_code == 201, "DOCX upload returns 201")
        docx_id = docx_upload.json()["resume"]["id"]

        proc_docx = await client.post(f"/api/v1/candidates/me/resumes/{docx_id}/process", headers=headers_a)
        check(proc_docx.status_code == 200, "Process DOCX returns 200")
        check(proc_docx.json()["resume"]["status"] == "processed", "DOCX status transitioned to 'processed'")

        # 14. Corrupted Document Extraction Failure Lifecycle
        # Upload valid-looking header to pass magic-bytes validation, but with corrupted internal structure
        corrupted_content = b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog >>\nendobj\nCORRUPTED_STREAM_CONTENT_NON_PARSABLE"
        corrupt_upload = await client.post(
            "/api/v1/candidates/me/resumes",
            headers=headers_a,
            files={"file": ("corrupt.pdf", io.BytesIO(corrupted_content), "application/pdf")},
        )
        check(corrupt_upload.status_code == 201, "Corrupted PDF upload returns 201")
        corrupt_id = corrupt_upload.json()["resume"]["id"]


        # Processing should attempt extraction, fail safely, and transition status to FAILED
        proc_corrupt = await client.post(f"/api/v1/candidates/me/resumes/{corrupt_id}/process", headers=headers_a)
        check(proc_corrupt.status_code == 200, "Corrupt processing call returns 200 with failed status envelope")
        check(proc_corrupt.json()["success"] is False, "Failure response success is False")
        check(proc_corrupt.json()["resume"]["status"] == "failed", "Corrupt resume status is 'failed'")
        check(proc_corrupt.json()["resume"]["failure_reason"] is not None, "failure_reason is populated")
        check(len(proc_corrupt.json()["resume"]["failure_reason"]) > 0, "failure_reason contains safe description")


        # 15. Retry Processing Lifecycle
        retry_res = await client.post(f"/api/v1/candidates/me/resumes/{corrupt_id}/retry", headers=headers_a)
        check(retry_res.status_code == 200, "Retry endpoint handles failed resume")
        # Retrying same corrupted bytes remains failed safely
        check(retry_res.json()["resume"]["status"] == "failed", "Retrying corrupted object records failure safely")

        # 16. Invariant & Security Checks
        # Already processed resume cannot be re-processed
        already_proc = await client.post(f"/api/v1/candidates/me/resumes/{pdf_id}/process", headers=headers_a)
        check(already_proc.status_code == 400, "Processing already processed resume returns 400")

        # Unauthenticated request
        unauth_proc = await client.post(f"/api/v1/candidates/me/resumes/{pdf_id}/process")
        check(unauth_proc.status_code == 401, "Unauthenticated process request returns 401")

        # IDOR protection: Candidate B cannot process Candidate A's resume
        idor_proc = await client.post(f"/api/v1/candidates/me/resumes/{pdf_id}/process", headers=headers_b)
        check(idor_proc.status_code == 404, "Candidate B cannot process Candidate A's resume (404)")

        # Cleanup test data
        async with SessionLocal() as db:
            from sqlalchemy import select, delete
            stmt = select(User).where(User.email.in_([cand_a_email, cand_b_email]))
            users = (await db.execute(stmt)).scalars().all()
            for u in users:
                await db.delete(u)
            await db.commit()


        print(f"\n============================================================", flush=True)
        print(f"RESUME EXTRACTION TESTS: {passed} passed, {failed} failed, {total} total", flush=True)
        print(f"============================================================", flush=True)

        if failed > 0:
            sys.exit(1)


@pytest.mark.asyncio
async def test_resume_extraction():
    await run_resume_extraction_tests()


if __name__ == "__main__":
    asyncio.run(run_resume_extraction_tests())

