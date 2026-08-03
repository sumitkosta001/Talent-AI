# Integrations Module (`app/integrations/`)

## Purpose
The `app/integrations/` module provides isolated SDK wrapper clients for third-party cloud SaaS providers and external AI model APIs.

## Responsibilities
- **`cloudinary.py`**: Document & media file uploads, signed CDN URL generation.
- **`openai.py`**: GPT-4o chat completions for resume parsing & structured generation.
- **`gemini.py`**: Google Gemini 1.5 Flash/Pro SDK integration for high-speed ATS analysis.
- **`huggingface.py`**: Text embedding vector generation for semantic candidate matching.
- **`resend.py`**: Transactional email notifications (verification codes, password reset links, status updates).

## What Belongs Here
- Pure integration wrapper classes wrapping third-party SDKs (`cloudinary`, `openai`, `google-generativeai`, `resend`).
- Isolated error mapping from third-party SDK errors into `TalentAIException`.

## What Should NOT Belong Here
- Hardcoded API secret keys or tokens (must be injected via `app/config/settings.py`).
- Higher-level business domain logic or database persistence.
