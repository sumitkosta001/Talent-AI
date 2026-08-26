"""Centralized Resume Degree Dictionary and Taxonomy for Day 25.

Defines:
1. DEGREE_LEVELS taxonomy list.
2. DEGREE_DICTIONARY mapping canonical degree names to level, aliases, and regex matching patterns.
3. INSTITUTION_ALIASES mapping known institution abbreviations to canonical names.
4. INSTITUTION_KEYWORDS indicator list for institution extraction.
"""

from typing import Dict, Any, List, Set, Tuple
import re

DEGREE_LEVELS: List[str] = [
    "UNDERGRADUATE",
    "POSTGRADUATE",
    "DOCTORATE",
    "DIPLOMA",
    "SECONDARY",
    "OTHER",
]

# Centralized Curated Degree Vocabulary
DEGREE_DICTIONARY: Dict[str, Dict[str, Any]] = {
    # -----------------------------------------------------------------------
    # UNDERGRADUATE DEGREES
    # -----------------------------------------------------------------------
    "Bachelor of Technology": {
        "level": "UNDERGRADUATE",
        "aliases": ["b.tech", "btech", "b. tech", "bachelor of technology"],
        "pattern": re.compile(r'(?<!\w)B\.?\s*Tech(?:\.|\b)|Bachelor\s+of\s+Technology(?!\w)', re.IGNORECASE),
    },
    "Bachelor of Engineering": {
        "level": "UNDERGRADUATE",
        "aliases": ["b.e.", "be", "b. e.", "bachelor of engineering"],
        "pattern": re.compile(r'(?<!\w)B\.?\s*E(?:\.|\b)|Bachelor\s+of\s+Engineering(?!\w)', re.IGNORECASE),
    },
    "Bachelor of Science": {
        "level": "UNDERGRADUATE",
        "aliases": ["b.sc.", "bsc", "b. sc.", "bachelor of science", "bs", "b.s."],
        "pattern": re.compile(r'(?<!\w)B\.?\s*Sc(?:\.|\b)|Bachelor\s+of\s+Science(?!\w)', re.IGNORECASE),
    },
    "Bachelor of Computer Applications": {
        "level": "UNDERGRADUATE",
        "aliases": ["bca", "b.c.a.", "bachelor of computer applications"],
        "pattern": re.compile(r'(?<!\w)B\.?\s*C\.?\s*A(?:\.|\b)|Bachelor\s+of\s+Computer\s+Applications(?!\w)', re.IGNORECASE),
    },
    "Bachelor of Business Administration": {
        "level": "UNDERGRADUATE",
        "aliases": ["bba", "b.b.a.", "bachelor of business administration"],
        "pattern": re.compile(r'(?<!\w)B\.?\s*B\.?\s*A(?:\.|\b)|Bachelor\s+of\s+Business\s+Administration(?!\w)', re.IGNORECASE),
    },
    "Bachelor of Commerce": {
        "level": "UNDERGRADUATE",
        "aliases": ["b.com", "bcom", "b. com", "bachelor of commerce"],
        "pattern": re.compile(r'(?<!\w)B\.?\s*Com(?:\.|\b)|Bachelor\s+of\s+Commerce(?!\w)', re.IGNORECASE),
    },
    "Bachelor of Architecture": {
        "level": "UNDERGRADUATE",
        "aliases": ["b.arch", "barch", "bachelor of architecture"],
        "pattern": re.compile(r'(?<!\w)B\.?\s*Arch(?:\.|\b)|Bachelor\s+of\s+Architecture(?!\w)', re.IGNORECASE),
    },

    # -----------------------------------------------------------------------
    # POSTGRADUATE DEGREES
    # -----------------------------------------------------------------------
    "Master of Technology": {
        "level": "POSTGRADUATE",
        "aliases": ["m.tech", "mtech", "m. tech", "master of technology"],
        "pattern": re.compile(r'(?<!\w)M\.?\s*Tech(?:\.|\b)|Master\s+of\s+Technology(?!\w)', re.IGNORECASE),
    },
    "Master of Engineering": {
        "level": "POSTGRADUATE",
        "aliases": ["m.e.", "me", "m. e.", "master of engineering"],
        "pattern": re.compile(r'(?<!\w)M\.?\s*E(?:\.|\b)|Master\s+of\s+Engineering(?!\w)', re.IGNORECASE),
    },
    "Master of Science": {
        "level": "POSTGRADUATE",
        "aliases": ["m.sc.", "msc", "m. sc.", "master of science", "ms", "m.s."],
        "pattern": re.compile(r'(?<!\w)M\.?\s*Sc(?:\.|\b)|Master\s+of\s+Science(?!\w)', re.IGNORECASE),
    },
    "Master of Computer Applications": {
        "level": "POSTGRADUATE",
        "aliases": ["mca", "m.c.a.", "master of computer applications"],
        "pattern": re.compile(r'(?<!\w)M\.?\s*C\.?\s*A(?:\.|\b)|Master\s+of\s+Computer\s+Applications(?!\w)', re.IGNORECASE),
    },
    "Master of Business Administration": {
        "level": "POSTGRADUATE",
        "aliases": ["mba", "m.b.a.", "master of business administration"],
        "pattern": re.compile(r'(?<!\w)M\.?\s*B\.?\s*A(?:\.|\b)|Master\s+of\s+Business\s+Administration(?!\w)', re.IGNORECASE),
    },
    "Master of Commerce": {
        "level": "POSTGRADUATE",
        "aliases": ["m.com", "mcom", "m. com", "master of commerce"],
        "pattern": re.compile(r'(?<!\w)M\.?\s*Com(?:\.|\b)|Master\s+of\s+Commerce(?!\w)', re.IGNORECASE),
    },
    "Master of Architecture": {
        "level": "POSTGRADUATE",
        "aliases": ["m.arch", "march", "master of architecture"],
        "pattern": re.compile(r'(?<!\w)M\.?\s*Arch(?:\.|\b)|Master\s+of\s+Architecture(?!\w)', re.IGNORECASE),
    },

    # -----------------------------------------------------------------------
    # DOCTORATE DEGREES
    # -----------------------------------------------------------------------
    "Doctor of Philosophy": {
        "level": "DOCTORATE",
        "aliases": ["phd", "ph.d.", "ph.d", "doctor of philosophy"],
        "pattern": re.compile(r'(?<!\w)Ph\.?\s*D\.?|Doctor\s+of\s+Philosophy(?!\w)', re.IGNORECASE),
    },

    # -----------------------------------------------------------------------
    # DIPLOMA
    # -----------------------------------------------------------------------
    "Diploma": {
        "level": "DIPLOMA",
        "aliases": ["diploma", "diploma in engineering", "polytechnic"],
        "pattern": re.compile(r'(?<!\w)Diploma(?:\s+in\s+Engineering)?|Polytechnic(?!\w)', re.IGNORECASE),
    },

    # -----------------------------------------------------------------------
    # SECONDARY / SCHOOL EDUCATION
    # -----------------------------------------------------------------------
    "Senior Secondary": {
        "level": "SECONDARY",
        "aliases": [
            "class xii", "class 12", "12th", "higher secondary", "senior secondary",
            "class xii (12th)", "intermediate", "up board, science", "up board intermediate",
            "cbse 12", "cbse xii", "icse 12", "hsc", "plus two", "+2"
        ],
        "pattern": re.compile(
            r'(?<!\w)(?:Class\s+(?:XII|12)|12th|Higher\s+Secondary|Senior\s+Secondary|Intermediate|UP\s+Board,\s*Science(?:\s*\(PCM\))?|HSC|Plus\s+Two|\+2)(?!\w)',
            re.IGNORECASE,
        ),
    },
    "Secondary": {
        "level": "SECONDARY",
        "aliases": [
            "class x", "class 10", "10th", "secondary school", "secondary education",
            "high school", "matriculation", "ssc", "cbse 10", "cbse x", "icse 10", "up board"
        ],
        "pattern": re.compile(
            r'(?<!\w)(?:Class\s+(?:X|10)|10th|Secondary\s+School|High\s+School|Matriculation|SSC|UP\s+Board)(?!\w)',
            re.IGNORECASE,
        ),
    },
}


# Reverse lookup alias map: lowercase alias -> (canonical_name, level)
DEGREE_ALIAS_MAP: Dict[str, Tuple[str, str]] = {}
for canonical_name, info in DEGREE_DICTIONARY.items():
    level = info["level"]
    DEGREE_ALIAS_MAP[canonical_name.lower()] = (canonical_name, level)
    for alias in info["aliases"]:
        DEGREE_ALIAS_MAP[alias.lower()] = (canonical_name, level)


# Explicit Institution Aliases (safe normalization for well-known acronyms)
INSTITUTION_ALIASES: Dict[str, str] = {
    "nit rourkela": "National Institute of Technology, Rourkela",
    "national institute of technology rourkela": "National Institute of Technology, Rourkela",
    "national institute of technology, rourkela": "National Institute of Technology, Rourkela",
    "iit delhi": "Indian Institute of Technology Delhi",
    "indian institute of technology delhi": "Indian Institute of Technology Delhi",
    "indian institute of technology, delhi": "Indian Institute of Technology Delhi",
    "iit bombay": "Indian Institute of Technology Bombay",
    "delhi university": "University of Delhi",
    "university of delhi": "University of Delhi",
}

# Institution keyword indicators
INSTITUTION_KEYWORDS: List[str] = [
    "University",
    "College",
    "Institute",
    "Institution",
    "School",
    "Academy",
    "Polytechnic",
    "IIT",
    "NIT",
    "IIIT",
    "BITS",
    "VIT",
    "MIT",
    "IIM",
    "AIIMS",
    "Inter College",
    "International School",
    "Public School",
    "High School",
    "Junior College",
    "Vidya Mandir",
    "Grammar School",
]

