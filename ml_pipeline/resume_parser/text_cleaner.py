"""
Text cleaning module.

Provides pre-processing utilities to normalise raw text extracted
from PDF resumes before downstream NLP tasks.
"""

import logging
import re

logger = logging.getLogger(__name__)


def clean_resume_text(text: str) -> str:
    """Clean and normalise raw resume text.

    Processing steps:
        1. Convert to lowercase.
        2. Remove URLs.
        3. Remove email addresses.
        4. Remove special characters (keep letters, digits, spaces).
        5. Collapse multiple whitespace characters into a single space.
        6. Strip leading and trailing whitespace.

    Args:
        text: Raw text extracted from a resume PDF.

    Returns:
        Cleaned and normalised text string.
    """
    if not text:
        logger.warning("Received empty text for cleaning.")
        return ""

    logger.info("Cleaning resume text (%d characters).", len(text))

    # Step 1 — lowercase
    text = text.lower()

    # Step 2 — remove URLs
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)

    # Step 3 — remove email addresses
    text = re.sub(r"\S+@\S+\.\S+", " ", text)

    # Step 4 — remove special characters (keep letters, digits, whitespace)
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # Step 5 — collapse whitespace
    text = re.sub(r"\s+", " ", text)

    # Step 6 — strip
    text = text.strip()

    logger.info("Cleaned text length: %d characters.", len(text))
    return text
