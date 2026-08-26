# Phase 4 — Day 35: ML Testing & End-to-End Pipeline Validation Plan

## 1. Executive Summary & Testing Objectives
Phase 4 Day 35 represents the final validation gate for the Talent-AI resume processing and Machine Learning pipeline. The primary objective is to comprehensively test, validate, harden, and verify the entire pipeline implemented during Days 21–34.

Day 35 does NOT introduce new ML features or rewrite working implementations. It establishes automated test coverage, regression testing, failure handling, input immutability, determinism, security sanity, and live localhost verification to prove that Days 21–34 function reliably both individually and together.

---

## 2. Comprehensive Test Audit & Gap Analysis

### Existing Test Suite Summary (Days 21–34)
The repository currently contains 237 passing automated tests across 23 test modules:
- `test_resume_extraction.py` (58 tests): Day 21 PDF/DOCX text & block extraction.
- `test_resume_ocr.py` (1 test): Day 22 Scanned PDF detection & OCR.
- `test_resume_text_processing.py` (3 tests): Day 23 Text cleaning, normalization, section detection.
- `test_resume_skills.py` (5 tests): Day 24 Skills extraction & canonical normalization.
- `test_resume_education.py` (1 test): Day 25 Degree, institution, year, CGPA extraction.
- `test_resume_experience.py` (1 test): Day 26 Experience duration, company, title, seniority extraction.
- `test_resume_projects.py` (1 test): Day 27 Project name, tech, classification extraction.
- `test_resume_structured.py` (1 test): Day 28 Structured resume JSON validation & persistence.
- `test_resume_classification.py` (1 test): Day 29 Role prediction & domain classification.
- `test_resume_ats_scoring.py` (1 test): Day 30 ATS scoring, keyword matching, score breakdown.
- `test_resume_similarity.py` (15 tests): Day 31 Semantic similarity matching & embeddings.
- `test_resume_faiss.py` (10 tests): Day 32 FAISS vector indexing & similarity search.
- `test_resume_recommendations.py` (12 tests): Day 33 Hybrid job/candidate recommendations.
- `test_resume_interview_questions.py` (13 tests): Day 34 AI interview question generation.
- Auxiliary modules (`test_candidate_profile.py`, `test_minio_storage.py`, `test_resume_delete.py`, `test_resume_history.py`, `test_resume_listing.py`, `test_resume_preview.py`, `test_resume_upload.py`, `test_resume_versioning.py`): 112 tests for DB/storage/API lifecycle.

### Identified Missing Coverage Gaps
1. **Full Pipeline Cross-Day Integration**: Need an explicit test that executes the full pipeline from Day 21 raw PDF/DOCX $\rightarrow$ Day 34 AI Interview Questions in sequence on a single synthetic candidate profile (`Alex Sharma`).
2. **Failure Injection & Malformed Input Handling**: Need tests for corrupt PDFs, corrupt DOCXs, missing OCR executables, empty resume strings, NaN/Inf vector embeddings, empty FAISS indices, missing skills/education/experience/projects, and unconfigured LLMs.
3. **Input Immutability**: Need tests verifying that pure processing functions (text cleaner, tokenizer, section detector, skill extractor, education extractor, experience extractor, project extractor, ATS scorer, classifier, recommendation engine, interview question generator) do NOT mutate their input objects.
4. **Determinism Verification**: Need tests confirming that running deterministic functions twice with identical input produces identical outputs.
5. **Security & Prompt Injection Sanity**: Need tests verifying that malicious or prompt-injection text embedded within candidate resume fields cannot override application logic or corrupt structured outputs.
6. **Edge Case Normalization**: Need tests for degree score boundaries, complex date ranges, overlapping skill aliases, multi-word project titles, and extreme ATS score clamping (0 and 100).

---

## 3. Day 35 Testing Strategy Matrix

### A. Unit Testing Strategy
- Cover pure functions (normalizers, tokenizers, section detectors, scoring functions, clamping utilities, deduplicators).
- Test inputs: normal, empty, `None`, malformed, boundary values, duplicate items, case variations.

### B. Extraction & OCR Testing Strategy (Days 21–22)
- Test multi-page PDFs, empty PDFs, PDFs with special symbols, and DOCX files.
- Test fallback when PyMuPDF/pdfplumber fails.
- Test OCR scanned document detection and image preprocessing fallback when Tesseract is uninstalled/unavailable.

### C. Text Processing & Tokenization Strategy (Day 23)
- Test CRLF $\rightarrow$ LF, control char removal, Unicode normalization, bullet/dash normalization.
- Test noise removal (page numbers, headers, footers).
- Test tokenization preservation for special tech tokens (`C++`, `C#`, `.NET`, `Node.js`, `React.js`, `scikit-learn`, emails, URLs).

### D. Skill, Education, Experience & Project Extraction Strategy (Days 24–27)
- Test canonical skill mapping (`ReactJS` $\rightarrow$ `React.js`, `Postgres` $\rightarrow$ `PostgreSQL`, `sklearn` $\rightarrow$ `scikit-learn`).
- Test degree score formats (`8.5/10`, `95%`, `3.8/4.0`).
- Test current employment indicators (`Present`, `Ongoing`, `Current`).
- Test project classification categories (`FULL_STACK`, `MACHINE_LEARNING`, `DEVOPS`).

### E. Structured Resume, Classification & ATS Scoring Strategy (Days 28–30)
- Test Pydantic JSON validation, status lifecycle (`UPLOADED` $\rightarrow$ `PROCESSING` $\rightarrow$ `PROCESSED` / `FAILED`).
- Test domain & role prediction accuracy for synthetic developer profiles.
- Test ATS score clamping strictly between `0.0` and `100.0` and evidence match explanations.

### F. Embedding, FAISS, Recommendation & Interview Question Strategy (Days 31–34)
- Test 384-dim embedding generation, L2 normalization, cosine similarity.
- Test FAISS index insertion, search, deletion, reload, and persistence.
- Test hybrid recommendation score formula: $\text{clamp}(\text{semantic\_score} \times 0.50 + \text{ats\_score} \times 0.50, 0.0, 100.0)$.
- Test interview question generation across Easy, Medium, Hard, Expert difficulties and deterministic fallback provider.

### G. Cross-Day End-to-End Pipeline Integration Strategy
- Execute a complete synthetic resume (`Alex Sharma`, B.Tech NIT, 6 skills, 1 intern experience, 2 projects) sequentially through all 14 stages:
  $$\text{Raw File} \rightarrow \text{Extraction} \rightarrow \text{OCR Check} \rightarrow \text{Text Processing} \rightarrow \text{Skills} \rightarrow \text{Education} \rightarrow \text{Experience} \rightarrow \text{Projects} \rightarrow \text{Structured Resume} \rightarrow \text{Classification} \rightarrow \text{ATS Scoring} \rightarrow \text{Embeddings} \rightarrow \text{FAISS Index} \rightarrow \text{Recommendations} \rightarrow \text{Interview Questions}$$

### H. Failure Injection & Immutability Strategy
- Inject invalid PDFs/DOCXs, empty documents, corrupt JSON, NaN embeddings, missing attributes.
- Compare deep copies of input objects before and after function execution to guarantee zero side-effect mutations.

---

## 4. Localhost Live API & Server Restart Verification Strategy
- Launch Uvicorn dev server on `http://127.0.0.1:8000`.
- Run automated HTTP client script (`scratch/test_localhost_day35_e2e.py`) to execute full authentication, resume upload, processing, ATS scoring, FAISS indexing, recommendation, and interview question generation.
- Restart Uvicorn server to verify disk persistence of FAISS vector indices and SQLite/Postgres data.

---

## 5. Verification Gate Criteria
1. `python -m compileall app` passes with 0 syntax/compilation errors.
2. All Day 35 new test modules pass 100%.
3. Full regression test suite (237 existing + all new Day 35 tests) passes 100%.
4. Live localhost verification script (`scratch/test_localhost_day35_e2e.py`) passes 100% against running Uvicorn server.
5. Server restart verification confirms post-restart FAISS index and DB persistence.
