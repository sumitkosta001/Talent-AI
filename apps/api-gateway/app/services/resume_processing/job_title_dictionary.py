"""Centralized Job Title Taxonomy, Seniority, and Company Dictionary for Day 26.

Defines:
1. SENIORITY_LEVELS taxonomy list.
2. EMPLOYMENT_TYPES taxonomy list.
3. TITLE_ALIAS_MAP for job title canonicalization.
4. COMPANY_ALIAS_MAP for safe company alias resolution.
5. JOB_TITLE_PATTERNS compiled regexes for job title detection.
"""

from typing import Dict, List, Tuple, Any
import re

SENIORITY_LEVELS: List[str] = [
    "INTERN",
    "ENTRY_LEVEL",
    "JUNIOR",
    "MID_LEVEL",
    "SENIOR",
    "LEAD",
    "STAFF",
    "PRINCIPAL",
    "MANAGER",
    "DIRECTOR",
    "EXECUTIVE",
    "UNKNOWN",
]

EMPLOYMENT_TYPES: List[str] = [
    "FULL_TIME",
    "PART_TIME",
    "INTERNSHIP",
    "CONTRACT",
    "FREELANCE",
    "TEMPORARY",
    "APPRENTICESHIP",
    "VOLUNTEER",
    "RESEARCH",
    "UNKNOWN",
]

# Canonical Job Title Aliases Map (lowercase raw alias -> canonical title string)
TITLE_ALIAS_MAP: Dict[str, str] = {
    "sde": "Software Development Engineer",
    "sde i": "Software Development Engineer I",
    "sde ii": "Software Development Engineer II",
    "sde iii": "Software Development Engineer III",
    "swe": "Software Engineer",
    "sr. software engineer": "Senior Software Engineer",
    "sr. developer": "Senior Software Developer",
    "sr developer": "Senior Software Developer",
    "jr. software engineer": "Junior Software Engineer",
    "jr. developer": "Junior Software Developer",
    "jr developer": "Junior Software Developer",
    "swe intern": "Software Engineering Intern",
    "sde intern": "Software Engineering Intern",
    "devops eng": "DevOps Engineer",
    "qa eng": "QA Engineer",
    "ml engineer": "Machine Learning Engineer",
    "data sci": "Data Scientist",
}

# Safe Company Aliases Map (lowercase raw alias -> canonical company name)
COMPANY_ALIAS_MAP: Dict[str, str] = {
    "google llc": "Google",
    "google inc": "Google",
    "microsoft corporation": "Microsoft",
    "microsoft corp": "Microsoft",
    "microsoft corp.": "Microsoft",
    "tcs": "Tata Consultancy Services",
    "tata consultancy services ltd": "Tata Consultancy Services",
    "tata consultancy services limited": "Tata Consultancy Services",
    "infosys ltd": "Infosys",
    "infosys limited": "Infosys",
    "wipro ltd": "Wipro",
    "wipro limited": "Wipro",
    "amazon.com": "Amazon",
    "amazon web services": "Amazon Web Services",
    "aws": "Amazon Web Services",
    "meta platforms": "Meta",
    "facebook": "Meta",
}

# Common Job Title Regex Patterns
JOB_TITLE_PATTERNS: List[re.Pattern] = [
    re.compile(
        r'\b(?:Senior|Sr\.|Junior|Jr\.|Lead|Staff|Principal|Associate|Chief)?\s*'
        r'(?:Software|Frontend|Backend|Full\s*Stack|Web|Mobile|Android|iOS|Cloud|DevOps|Data|ML|Machine\s+Learning|AI|QA|Test|Automation|Systems?|Network|Embedded|Product|Project|Engineering)?\s*'
        r'(?:Engineer|Developer|Architect|Scientist|Analyst|Manager|Director|Consultant|Intern|Assistant|Trainee|Lead|Specialist)\b',
        re.IGNORECASE,
    ),
    re.compile(
        r'\b(?:Software\s+Development\s+Engineer|Graduate\s+Engineer\s+Trainee|Research\s+Assistant|Research\s+Intern|Tech\s+Lead|Team\s+Lead)\b',
        re.IGNORECASE,
    ),
]
