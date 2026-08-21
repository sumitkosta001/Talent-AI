"""Regex-based resume tokenizer module for Day 23.

Implements tokenization tailored for technical resumes without spaCy/NLTK.
Preserves technical terms (C++, C#, .NET, Node.js, React.js, Next.js, Vue.js, CI/CD),
emails, URLs, dates, and version strings intact.

Generates:
  - tokens: Case-preserved token strings
  - normalized_tokens: Lowercased token strings
"""

import re
from typing import List, Tuple

# Engineered regex pattern for technical resume tokenization
# Order matters: complex multi-character technical patterns come first!
RESUME_TOKEN_PATTERN = re.compile(
    r"""
    (?P<EMAIL>[\w.-]+@[\w.-]+\.\w+)                              | # Email addresses
    (?P<URL>https?://[^\s/$.?#].[^\s]*|www\.[^\s/$.?#].[^\s]*)   | # Web URLs
    (?P<CPP>C\+\+)                                                | # C++
    (?P<CSHARP>C\#)                                               | # C#
    (?P<DOTNET>\.NET)                                             | # .NET
    (?P<NODEJS>Node\.js)                                          | # Node.js
    (?P<REACTJS>React\.js)                                        | # React.js
    (?P<NEXTJS>Next\.js)                                          | # Next.js
    (?P<VUEJS>Vue\.js)                                            | # Vue.js
    (?P<CICD>CI/CD)                                               | # CI/CD
    (?P<TCPIP>TCP/IP)                                             | # TCP/IP
    (?P<SCIKIT>scikit-learn)                                      | # scikit-learn
    (?P<VERSION>[vV]?\d+\.\d+(\.\d+)?)                            | # Version numbers (e.g. v3.12, 16.0)
    (?P<DATE>\b\d{4}[-/]\d{2}([-/]\d{2})?\b|\b\d{4}\b)            | # Dates (e.g. 2022-2025, 2024)
    (?P<WORD>[\w'-]+)                                               # Standard words and hyphenated terms
    """,
    re.VERBOSE | re.IGNORECASE,
)


def tokenize_resume_text(text: str) -> Tuple[List[str], List[str]]:
    """Tokenize resume text while preserving technical symbols, emails, and URLs.

    Args:
        text: Cleaned resume text string.

    Returns:
        Tuple of (case_preserved_tokens, lowercase_normalized_tokens).
    """
    if not text:
        return [], []

    tokens: List[str] = []
    normalized_tokens: List[str] = []

    for match in RESUME_TOKEN_PATTERN.finditer(text):
        token_str = match.group(0).strip()
        if not token_str:
            continue

        # Strip trailing punctuation if it was matched at the end of a word (e.g., "Python," -> "Python")
        # BUT do NOT strip '+' from 'C++', '#' from 'C#', or '.' from '.NET' / 'Node.js'
        if token_str not in ("C++", "C#", ".NET", "Node.js", "React.js", "Next.js", "Vue.js"):
            token_str = token_str.rstrip(".,;:!?'\"()[]{}")

        if not token_str:
            continue

        tokens.append(token_str)
        normalized_tokens.append(token_str.lower())

    return tokens, normalized_tokens
