"""Phase 4 Day 29 — Resume Classification Taxonomy and Scoring Weights.

Centralized domain, role, and experience level definitions, title aliases,
and evidence scoring weights.
"""

from typing import Dict, List, Set, Tuple

# Candidate Domains
DOMAIN_TAXONOMY: Set[str] = {
    "SOFTWARE_ENGINEERING",
    "DATA_SCIENCE",
    "MACHINE_LEARNING",
    "ARTIFICIAL_INTELLIGENCE",
    "DATA_ANALYTICS",
    "CYBERSECURITY",
    "CLOUD_DEVOPS",
    "ELECTRICAL_ENGINEERING",
    "ELECTRONICS_ENGINEERING",
    "EMBEDDED_SYSTEMS",
    "MECHANICAL_ENGINEERING",
    "CIVIL_ENGINEERING",
    "PRODUCT_MANAGEMENT",
    "UI_UX_DESIGN",
    "QA_TESTING",
    "RESEARCH",
    "BUSINESS",
    "FINANCE",
    "OTHER",
    "UNKNOWN",
}

# Candidate Roles
ROLE_TAXONOMY: Set[str] = {
    "SOFTWARE_ENGINEER",
    "BACKEND_DEVELOPER",
    "FRONTEND_DEVELOPER",
    "FULL_STACK_DEVELOPER",
    "MOBILE_DEVELOPER",
    "DEVOPS_ENGINEER",
    "CLOUD_ENGINEER",
    "DATA_ENGINEER",
    "DATA_SCIENTIST",
    "DATA_ANALYST",
    "MACHINE_LEARNING_ENGINEER",
    "AI_ENGINEER",
    "NLP_ENGINEER",
    "COMPUTER_VISION_ENGINEER",
    "CYBERSECURITY_ENGINEER",
    "QA_ENGINEER",
    "TEST_ENGINEER",
    "PRODUCT_MANAGER",
    "UI_UX_DESIGNER",
    "RESEARCHER",
    "ELECTRICAL_ENGINEER",
    "ELECTRONICS_ENGINEER",
    "EMBEDDED_ENGINEER",
    "FIRMWARE_ENGINEER",
    "SYSTEMS_ENGINEER",
    "OTHER",
    "UNKNOWN",
}

# Seniority / Experience Levels (reusing Day 26 taxonomy)
EXPERIENCE_LEVEL_TAXONOMY: Set[str] = {
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
}

# Scoring Weights
SKILL_WEIGHT: float = 0.35
PROJECT_WEIGHT: float = 0.30
EXPERIENCE_WEIGHT: float = 0.20
EDUCATION_WEIGHT: float = 0.10
TITLE_WEIGHT: float = 0.05

# Job Title Aliases Map -> Canonical Role
TITLE_ALIAS_MAP: Dict[str, str] = {
    "sde": "SOFTWARE_ENGINEER",
    "sde-1": "SOFTWARE_ENGINEER",
    "sde 1": "SOFTWARE_ENGINEER",
    "sde i": "SOFTWARE_ENGINEER",
    "sde-2": "SOFTWARE_ENGINEER",
    "sde 2": "SOFTWARE_ENGINEER",
    "sde ii": "SOFTWARE_ENGINEER",
    "sde iii": "SOFTWARE_ENGINEER",
    "software developer": "SOFTWARE_ENGINEER",
    "software engineer": "SOFTWARE_ENGINEER",
    "full stack developer": "FULL_STACK_DEVELOPER",
    "full stack engineer": "FULL_STACK_DEVELOPER",
    "fullstack developer": "FULL_STACK_DEVELOPER",
    "fullstack engineer": "FULL_STACK_DEVELOPER",
    "backend developer": "BACKEND_DEVELOPER",
    "backend engineer": "BACKEND_DEVELOPER",
    "frontend developer": "FRONTEND_DEVELOPER",
    "frontend engineer": "FRONTEND_DEVELOPER",
    "web developer": "FULL_STACK_DEVELOPER",
    "mobile developer": "MOBILE_DEVELOPER",
    "ios developer": "MOBILE_DEVELOPER",
    "android developer": "MOBILE_DEVELOPER",
    "devops engineer": "DEVOPS_ENGINEER",
    "cloud engineer": "CLOUD_ENGINEER",
    "site reliability engineer": "DEVOPS_ENGINEER",
    "sre": "DEVOPS_ENGINEER",
    "data engineer": "DATA_ENGINEER",
    "data scientist": "DATA_SCIENTIST",
    "data analyst": "DATA_ANALYST",
    "machine learning engineer": "MACHINE_LEARNING_ENGINEER",
    "ml engineer": "MACHINE_LEARNING_ENGINEER",
    "ai engineer": "AI_ENGINEER",
    "artificial intelligence engineer": "AI_ENGINEER",
    "nlp engineer": "NLP_ENGINEER",
    "computer vision engineer": "COMPUTER_VISION_ENGINEER",
    "embedded engineer": "EMBEDDED_ENGINEER",
    "embedded systems engineer": "EMBEDDED_ENGINEER",
    "firmware engineer": "FIRMWARE_ENGINEER",
    "electrical engineer": "ELECTRICAL_ENGINEER",
    "electronics engineer": "ELECTRONICS_ENGINEER",
    "qa engineer": "QA_ENGINEER",
    "test engineer": "TEST_ENGINEER",
    "product manager": "PRODUCT_MANAGER",
    "ui/ux designer": "UI_UX_DESIGNER",
    "ux designer": "UI_UX_DESIGNER",
}

# Domain Category Skill Map
DOMAIN_SKILL_MAP: Dict[str, Set[str]] = {
    "SOFTWARE_ENGINEERING": {
        "python", "javascript", "typescript", "java", "c++", "c#", "go", "rust",
        "react.js", "react", "next.js", "angular", "vue.js", "node.js", "express.js",
        "fastapi", "django", "flask", "spring boot", "postgresql", "mysql", "mongodb",
        "redis", "git", "rest api", "graphql"
    },
    "MACHINE_LEARNING": {
        "tensorflow", "pytorch", "scikit-learn", "keras", "opencv", "spacy", "nltk",
        "machine learning", "deep learning", "nlp", "computer vision", "hugging face"
    },
    "ARTIFICIAL_INTELLIGENCE": {
        "tensorflow", "pytorch", "artificial intelligence", "deep learning", "llm",
        "openai", "transformers", "neural networks"
    },
    "DATA_SCIENCE": {
        "python", "r", "pandas", "numpy", "scipy", "scikit-learn", "data science",
        "data mining", "statistical modeling", "jupyter"
    },
    "DATA_ANALYTICS": {
        "sql", "excel", "tableau", "power bi", "data analytics", "data visualization",
        "google analytics"
    },
    "CLOUD_DEVOPS": {
        "docker", "kubernetes", "aws", "azure", "gcp", "terraform", "ansible",
        "jenkins", "ci/cd", "linux", "bash", "shell scripting"
    },
    "EMBEDDED_SYSTEMS": {
        "c", "c++", "embedded c", "arduino", "stm32", "raspberry pi", "rtos",
        "microcontrollers", "arm", "fpga", "vhdl", "verilog"
    },
    "ELECTRICAL_ENGINEERING": {
        "matlab", "simulink", "electrical engineering", "circuit design", "pcb design",
        "power electronics", "plc", "scada", "multisim"
    },
    "ELECTRONICS_ENGINEERING": {
        "vlsi", "cadence", "proteus", "embedded c", "microcontrollers", "signal processing"
    },
    "CYBERSECURITY": {
        "cybersecurity", "penetration testing", "wireshark", "metasploit", "ethical hacking",
        "network security", "siem", "cryptography"
    },
}
