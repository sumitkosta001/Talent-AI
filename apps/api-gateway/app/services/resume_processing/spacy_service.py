"""Singleton spaCy NLP Service for Day 24 Resume Skills Extraction.

Provides lazy-loaded, thread-safe access to the configured spaCy language pipeline (en_core_web_sm).
Prevents reloading the model on every extraction call and handles missing model errors gracefully.
"""

import logging
from typing import Optional
import spacy
from spacy.language import Language

from app.config.settings import settings
from app.exceptions.resume import ResumeParsingError

logger = logging.getLogger("talentai.resume_processing.spacy_service")

_spacy_nlp_instance: Optional[Language] = None
_spacy_model_name: Optional[str] = None


def get_spacy_nlp(model_name: Optional[str] = None) -> Language:
    """Get or load the singleton spaCy Language pipeline model.

    Args:
        model_name: Optional model name override. Defaults to settings.nlp.spacy_model.

    Returns:
        Loaded spaCy Language pipeline object.

    Raises:
        ResumeParsingError: If spaCy model is not installed or fails to load.
    """
    global _spacy_nlp_instance, _spacy_model_name

    target_model = model_name or settings.nlp.spacy_model

    if _spacy_nlp_instance is not None and _spacy_model_name == target_model:
        return _spacy_nlp_instance

    try:
        logger.info("Loading spaCy NLP pipeline model: '%s'", target_model)
        nlp = spacy.load(target_model)
        _spacy_nlp_instance = nlp
        _spacy_model_name = target_model
        logger.info("Successfully loaded spaCy model '%s' (components: %s)", target_model, nlp.pipe_names)
        return nlp

    except Exception as exc:
        logger.error("Failed to load spaCy model '%s': %s", target_model, str(exc))
        raise ResumeParsingError(
            f"Failed to load spaCy NLP model '{target_model}'. Ensure 'python -m spacy download {target_model}' has been executed."
        ) from exc


def get_loaded_model_name() -> str:
    """Return the name of the currently loaded spaCy model."""
    return _spacy_model_name or settings.nlp.spacy_model


def reset_spacy_cache() -> None:
    """Reset cached spaCy instance (useful for testing or reloading)."""
    global _spacy_nlp_instance, _spacy_model_name
    _spacy_nlp_instance = None
    _spacy_model_name = None


def set_spacy_nlp(nlp: Language, model_name: Optional[str] = None) -> None:
    """Inject a pre-loaded spaCy instance (useful for unit tests/mocking)."""
    global _spacy_nlp_instance, _spacy_model_name
    _spacy_nlp_instance = nlp
    _spacy_model_name = model_name or getattr(nlp, "meta", {}).get("name", settings.nlp.spacy_model)

