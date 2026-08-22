"""Centralized Resume Skill Dictionary and Taxonomy for Day 24.

Defines:
1. SKILL_CATEGORIES taxonomy list.
2. SKILL_DICTIONARY mapping canonical skill names to aliases and categories.
3. Fast reverse lookup mappings (lowercase alias -> (canonical_name, category)).
4. False-positive guard lists for ambiguous short tokens (C, R, Go, IT, AI).
"""

from typing import Dict, Any, List, Set, Tuple

# Canonical Skill Categories Taxonomy
SKILL_CATEGORIES: List[str] = [
    "PROGRAMMING_LANGUAGE",
    "FRONTEND",
    "BACKEND",
    "DATABASE",
    "CLOUD",
    "DEVOPS",
    "MOBILE",
    "DATA_SCIENCE",
    "MACHINE_LEARNING",
    "AI",
    "WEB",
    "TESTING",
    "VERSION_CONTROL",
    "TOOLS",
    "FRAMEWORK",
    "LIBRARY",
    "SECURITY",
    "NETWORKING",
    "OPERATING_SYSTEM",
    "SOFT_SKILL",
    "OTHER",
]

# Centralized Curated Resume Skill Vocabulary
SKILL_DICTIONARY: Dict[str, Dict[str, Any]] = {
    # -----------------------------------------------------------------------
    # PROGRAMMING LANGUAGES
    # -----------------------------------------------------------------------
    "Python": {
        "aliases": ["python", "py"],
        "category": "PROGRAMMING_LANGUAGE",
    },
    "Java": {
        "aliases": ["java"],
        "category": "PROGRAMMING_LANGUAGE",
    },
    "C": {
        "aliases": ["c language", "c programming"],
        "category": "PROGRAMMING_LANGUAGE",
        "is_short_ambiguous": True,
    },
    "C++": {
        "aliases": ["c++", "cpp", "c plus plus"],
        "category": "PROGRAMMING_LANGUAGE",
    },
    "C#": {
        "aliases": ["c#", "csharp", "c sharp"],
        "category": "PROGRAMMING_LANGUAGE",
    },
    "JavaScript": {
        "aliases": ["javascript", "js", "ecmascript"],
        "category": "PROGRAMMING_LANGUAGE",
    },
    "TypeScript": {
        "aliases": ["typescript", "ts"],
        "category": "PROGRAMMING_LANGUAGE",
    },
    "Go": {
        "aliases": ["golang", "go language", "go lang"],
        "category": "PROGRAMMING_LANGUAGE",
        "is_short_ambiguous": True,
    },
    "Rust": {
        "aliases": ["rust", "rustlang"],
        "category": "PROGRAMMING_LANGUAGE",
    },
    "PHP": {
        "aliases": ["php"],
        "category": "PROGRAMMING_LANGUAGE",
    },
    "Ruby": {
        "aliases": ["ruby", "ruby lang"],
        "category": "PROGRAMMING_LANGUAGE",
    },
    "Kotlin": {
        "aliases": ["kotlin"],
        "category": "PROGRAMMING_LANGUAGE",
    },
    "Swift": {
        "aliases": ["swift", "swift lang"],
        "category": "PROGRAMMING_LANGUAGE",
    },
    "R": {
        "aliases": ["r language", "r programming"],
        "category": "PROGRAMMING_LANGUAGE",
        "is_short_ambiguous": True,
    },
    "MATLAB": {
        "aliases": ["matlab"],
        "category": "PROGRAMMING_LANGUAGE",
    },
    "SQL": {
        "aliases": ["sql", "structured query language"],
        "category": "PROGRAMMING_LANGUAGE",
    },
    "Scala": {
        "aliases": ["scala"],
        "category": "PROGRAMMING_LANGUAGE",
    },
    "Perl": {
        "aliases": ["perl"],
        "category": "PROGRAMMING_LANGUAGE",
    },
    "Dart": {
        "aliases": ["dart"],
        "category": "PROGRAMMING_LANGUAGE",
    },

    # -----------------------------------------------------------------------
    # FRONTEND
    # -----------------------------------------------------------------------
    "HTML": {
        "aliases": ["html", "html5"],
        "category": "FRONTEND",
    },
    "CSS": {
        "aliases": ["css", "css3"],
        "category": "FRONTEND",
    },
    "React.js": {
        "aliases": ["react", "react.js", "reactjs", "react js"],
        "category": "FRONTEND",
    },
    "Next.js": {
        "aliases": ["next.js", "nextjs", "next js"],
        "category": "FRONTEND",
    },
    "Vue.js": {
        "aliases": ["vue", "vue.js", "vuejs", "vue js"],
        "category": "FRONTEND",
    },
    "Angular": {
        "aliases": ["angular", "angularjs", "angular.js", "angular 2+"],
        "category": "FRONTEND",
    },
    "Svelte": {
        "aliases": ["svelte", "sveltejs"],
        "category": "FRONTEND",
    },
    "Tailwind CSS": {
        "aliases": ["tailwind", "tailwind css", "tailwindcss"],
        "category": "FRONTEND",
    },
    "Bootstrap": {
        "aliases": ["bootstrap", "bootstrap 5"],
        "category": "FRONTEND",
    },

    # -----------------------------------------------------------------------
    # BACKEND
    # -----------------------------------------------------------------------
    "Node.js": {
        "aliases": ["node", "node.js", "nodejs", "node js"],
        "category": "BACKEND",
    },
    "Express.js": {
        "aliases": ["express", "express.js", "expressjs", "express js"],
        "category": "BACKEND",
    },
    "FastAPI": {
        "aliases": ["fastapi", "fast api"],
        "category": "BACKEND",
    },
    "Django": {
        "aliases": ["django", "django rest framework", "drf"],
        "category": "BACKEND",
    },
    "Flask": {
        "aliases": ["flask"],
        "category": "BACKEND",
    },
    "Spring Boot": {
        "aliases": ["spring boot", "springboot"],
        "category": "BACKEND",
    },
    "Spring": {
        "aliases": ["spring framework"],
        "category": "BACKEND",
    },
    ".NET": {
        "aliases": [".net", "dotnet", ".net core", "asp.net"],
        "category": "BACKEND",
    },
    "Laravel": {
        "aliases": ["laravel"],
        "category": "BACKEND",
    },

    # -----------------------------------------------------------------------
    # DATABASE
    # -----------------------------------------------------------------------
    "PostgreSQL": {
        "aliases": ["postgresql", "postgres", "psql"],
        "category": "DATABASE",
    },
    "MySQL": {
        "aliases": ["mysql"],
        "category": "DATABASE",
    },
    "SQLite": {
        "aliases": ["sqlite", "sqlite3"],
        "category": "DATABASE",
    },
    "MongoDB": {
        "aliases": ["mongodb", "mongo"],
        "category": "DATABASE",
    },
    "Redis": {
        "aliases": ["redis"],
        "category": "DATABASE",
    },
    "Cassandra": {
        "aliases": ["cassandra", "apache cassandra"],
        "category": "DATABASE",
    },
    "DynamoDB": {
        "aliases": ["dynamodb", "aws dynamodb"],
        "category": "DATABASE",
    },
    "Oracle Database": {
        "aliases": ["oracle", "oracle db", "oracle database"],
        "category": "DATABASE",
    },
    "SQL Server": {
        "aliases": ["sql server", "mssql", "microsoft sql server"],
        "category": "DATABASE",
    },

    # -----------------------------------------------------------------------
    # CLOUD
    # -----------------------------------------------------------------------
    "AWS": {
        "aliases": ["aws", "amazon web services", "amazon aws"],
        "category": "CLOUD",
    },
    "Microsoft Azure": {
        "aliases": ["azure", "microsoft azure"],
        "category": "CLOUD",
    },
    "Google Cloud": {
        "aliases": ["gcp", "google cloud", "google cloud platform"],
        "category": "CLOUD",
    },
    "Firebase": {
        "aliases": ["firebase"],
        "category": "CLOUD",
    },

    # -----------------------------------------------------------------------
    # DEVOPS & INFRASTRUCTURE
    # -----------------------------------------------------------------------
    "Docker": {
        "aliases": ["docker", "containerization"],
        "category": "DEVOPS",
    },
    "Kubernetes": {
        "aliases": ["kubernetes", "k8s"],
        "category": "DEVOPS",
    },
    "Jenkins": {
        "aliases": ["jenkins"],
        "category": "DEVOPS",
    },
    "GitHub Actions": {
        "aliases": ["github actions", "gh actions"],
        "category": "DEVOPS",
    },
    "GitLab CI": {
        "aliases": ["gitlab ci", "gitlab-ci"],
        "category": "DEVOPS",
    },
    "CI/CD": {
        "aliases": ["ci/cd", "ci-cd", "continuous integration"],
        "category": "DEVOPS",
    },
    "Terraform": {
        "aliases": ["terraform"],
        "category": "DEVOPS",
    },
    "Ansible": {
        "aliases": ["ansible"],
        "category": "DEVOPS",
    },
    "Linux": {
        "aliases": ["linux", "ubuntu", "debian", "centos", "redhat"],
        "category": "OPERATING_SYSTEM",
    },
    "Nginx": {
        "aliases": ["nginx"],
        "category": "DEVOPS",
    },

    # -----------------------------------------------------------------------
    # VERSION CONTROL
    # -----------------------------------------------------------------------
    "Git": {
        "aliases": ["git"],
        "category": "VERSION_CONTROL",
    },
    "GitHub": {
        "aliases": ["github"],
        "category": "VERSION_CONTROL",
    },
    "GitLab": {
        "aliases": ["gitlab"],
        "category": "VERSION_CONTROL",
    },
    "Bitbucket": {
        "aliases": ["bitbucket"],
        "category": "VERSION_CONTROL",
    },

    # -----------------------------------------------------------------------
    # MOBILE
    # -----------------------------------------------------------------------
    "React Native": {
        "aliases": ["react native"],
        "category": "MOBILE",
    },
    "Flutter": {
        "aliases": ["flutter"],
        "category": "MOBILE",
    },
    "Android Development": {
        "aliases": ["android", "android dev"],
        "category": "MOBILE",
    },
    "iOS Development": {
        "aliases": ["ios", "ios dev"],
        "category": "MOBILE",
    },

    # -----------------------------------------------------------------------
    # DATA SCIENCE & MACHINE LEARNING
    # -----------------------------------------------------------------------
    "NumPy": {
        "aliases": ["numpy"],
        "category": "DATA_SCIENCE",
    },
    "Pandas": {
        "aliases": ["pandas"],
        "category": "DATA_SCIENCE",
    },
    "Matplotlib": {
        "aliases": ["matplotlib"],
        "category": "DATA_SCIENCE",
    },
    "Seaborn": {
        "aliases": ["seaborn"],
        "category": "DATA_SCIENCE",
    },
    "SciPy": {
        "aliases": ["scipy"],
        "category": "DATA_SCIENCE",
    },
    "Jupyter": {
        "aliases": ["jupyter", "jupyter notebook"],
        "category": "DATA_SCIENCE",
    },
    "Data Analysis": {
        "aliases": ["data analysis", "data analytics"],
        "category": "DATA_SCIENCE",
    },
    "Data Visualization": {
        "aliases": ["data visualization"],
        "category": "DATA_SCIENCE",
    },
    "scikit-learn": {
        "aliases": ["scikit-learn", "sklearn", "scikit learn"],
        "category": "MACHINE_LEARNING",
    },
    "TensorFlow": {
        "aliases": ["tensorflow", "tf"],
        "category": "MACHINE_LEARNING",
    },
    "Keras": {
        "aliases": ["keras"],
        "category": "MACHINE_LEARNING",
    },
    "PyTorch": {
        "aliases": ["pytorch"],
        "category": "MACHINE_LEARNING",
    },
    "XGBoost": {
        "aliases": ["xgboost"],
        "category": "MACHINE_LEARNING",
    },
    "spaCy": {
        "aliases": ["spacy"],
        "category": "LIBRARY",
    },
    "OpenCV": {
        "aliases": ["opencv", "open-cv"],
        "category": "LIBRARY",
    },
    "LightGBM": {
        "aliases": ["lightgbm"],
        "category": "MACHINE_LEARNING",
    },
    "Machine Learning": {
        "aliases": ["machine learning", "ml"],
        "category": "MACHINE_LEARNING",
    },
    "Deep Learning": {
        "aliases": ["deep learning", "dl"],
        "category": "MACHINE_LEARNING",
    },
    "Computer Vision": {
        "aliases": ["computer vision", "cv"],
        "category": "MACHINE_LEARNING",
    },
    "Natural Language Processing": {
        "aliases": ["natural language processing", "nlp"],
        "category": "MACHINE_LEARNING",
    },

    # -----------------------------------------------------------------------
    # AI & GENERATIVE AI
    # -----------------------------------------------------------------------
    "Artificial Intelligence": {
        "aliases": ["artificial intelligence", "ai"],
        "category": "AI",
        "is_short_ambiguous": True,
    },
    "Generative AI": {
        "aliases": ["generative ai", "genai", "gen ai"],
        "category": "AI",
    },
    "Large Language Models": {
        "aliases": ["large language models", "llm", "llms"],
        "category": "AI",
    },
    "GPT": {
        "aliases": ["gpt", "gpt-3.5", "gpt-4", "chatgpt"],
        "category": "AI",
    },
    "OpenAI": {
        "aliases": ["openai"],
        "category": "AI",
    },
    "Gemini": {
        "aliases": ["gemini", "google gemini"],
        "category": "AI",
    },
    "Hugging Face": {
        "aliases": ["hugging face", "huggingface"],
        "category": "AI",
    },
    "Transformers": {
        "aliases": ["transformers"],
        "category": "AI",
    },

    # -----------------------------------------------------------------------
    # TESTING
    # -----------------------------------------------------------------------
    "Pytest": {
        "aliases": ["pytest"],
        "category": "TESTING",
    },
    "JUnit": {
        "aliases": ["junit"],
        "category": "TESTING",
    },
    "Jest": {
        "aliases": ["jest"],
        "category": "TESTING",
    },
    "Cypress": {
        "aliases": ["cypress"],
        "category": "TESTING",
    },
    "Selenium": {
        "aliases": ["selenium"],
        "category": "TESTING",
    },
    "Playwright": {
        "aliases": ["playwright"],
        "category": "TESTING",
    },

    # -----------------------------------------------------------------------
    # WEB & SECURITY
    # -----------------------------------------------------------------------
    "REST API": {
        "aliases": ["rest api", "restful api", "rest", "restful"],
        "category": "WEB",
    },
    "GraphQL": {
        "aliases": ["graphql"],
        "category": "WEB",
    },
    "WebSockets": {
        "aliases": ["websockets", "websocket"],
        "category": "WEB",
    },
    "OAuth 2.0": {
        "aliases": ["oauth", "oauth2", "oauth 2.0"],
        "category": "SECURITY",
    },
    "JWT": {
        "aliases": ["jwt", "json web token"],
        "category": "SECURITY",
    },
    "HTTPS / SSL / TLS": {
        "aliases": ["https", "ssl", "tls"],
        "category": "SECURITY",
    },

    # -----------------------------------------------------------------------
    # TOOLS
    # -----------------------------------------------------------------------
    "VS Code": {
        "aliases": ["vs code", "vscode", "visual studio code"],
        "category": "TOOLS",
    },
    "Postman": {
        "aliases": ["postman"],
        "category": "TOOLS",
    },
    "Figma": {
        "aliases": ["figma"],
        "category": "TOOLS",
    },
    "Bash": {
        "aliases": ["bash", "shell scripting", "zsh"],
        "category": "TOOLS",
    },
}

# Reverse lookup: lowercase_alias -> (canonical_name, category)
ALIAS_MAP: Dict[str, Tuple[str, str]] = {}
SHORT_AMBIGUOUS_ALIASES: Set[str] = set()


def validate_skill_dictionary() -> List[str]:
    """Validate skill dictionary taxonomy, categories, aliases, and collision prevention.

    Returns:
        List of warning/error messages if any dictionary validation issues are found.

    Raises:
        ValueError: If a fatal taxonomy violation (missing category, invalid category) occurs.
    """
    valid_categories = set(SKILL_CATEGORIES)
    alias_to_canonical: Dict[str, str] = {}
    errors: List[str] = []

    for canonical, info in SKILL_DICTIONARY.items():
        if not isinstance(canonical, str) or not canonical.strip():
            errors.append(f"Invalid canonical skill name: '{canonical}'")
            continue

        cat = info.get("category")
        if not cat or cat not in valid_categories:
            errors.append(f"Skill '{canonical}' has invalid category '{cat}'. Must be one of {SKILL_CATEGORIES}")

        aliases = info.get("aliases", [])
        all_terms = [canonical] + list(aliases)

        for term in all_terms:
            if not isinstance(term, str) or not term.strip():
                errors.append(f"Skill '{canonical}' contains an invalid/empty alias: '{term}'")
                continue

            term_clean = term.strip().lower()
            if term_clean in alias_to_canonical and alias_to_canonical[term_clean] != canonical:
                existing_canonical = alias_to_canonical[term_clean]
                errors.append(
                    f"Alias collision detected: '{term_clean}' maps to both '{existing_canonical}' and '{canonical}'"
                )
            else:
                alias_to_canonical[term_clean] = canonical

    if errors:
        import logging
        logger = logging.getLogger("talentai.resume_processing.skill_dictionary")
        for err in errors:
            logger.warning("Skill Dictionary Validation Warning: %s", err)
        if any("invalid category" in e for e in errors):
            raise ValueError(f"Skill dictionary validation failed with {len(errors)} error(s): {errors[0]}")

    return errors


# Build reverse lookup map
for canonical, info in SKILL_DICTIONARY.items():
    cat = info["category"]
    # Register canonical name itself as alias
    ALIAS_MAP[canonical.lower()] = (canonical, cat)
    if info.get("is_short_ambiguous"):
        SHORT_AMBIGUOUS_ALIASES.add(canonical.lower())

    for alias in info.get("aliases", []):
        alias_clean = alias.strip().lower()
        if alias_clean:
            ALIAS_MAP[alias_clean] = (canonical, cat)
            if info.get("is_short_ambiguous"):
                SHORT_AMBIGUOUS_ALIASES.add(alias_clean)

# Run dictionary validation upon import
validate_skill_dictionary()

