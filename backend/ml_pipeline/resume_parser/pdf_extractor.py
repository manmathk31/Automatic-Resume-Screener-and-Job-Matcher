"""
PDF text extraction module.

Uses PyMuPDF (fitz) to extract raw text content from PDF resume files.
"""

import logging
from pathlib import Path

import fitz  # PyMuPDF

logger = logging.getLogger(__name__)


def extract_resume_text(file_path: str) -> str:
    """Extract all text from a PDF resume.

    Args:
        file_path: Path to the PDF file.

    Returns:
        Concatenated text from every page of the PDF.

    Raises:
        FileNotFoundError: If the PDF file does not exist.
        RuntimeError: If the PDF cannot be opened or read.
    """
    path = Path(file_path)

    # --- Validate file exists ---
    if not path.exists():
        logger.error("File not found: %s", file_path)
        raise FileNotFoundError(f"Resume file not found: {file_path}")

    if not path.suffix.lower() == ".pdf":
        logger.warning("File '%s' does not have a .pdf extension.", file_path)

    try:
        logger.info("Extracting text from resume: %s", path.name)
        doc = fitz.open(str(path))

        text_parts: list[str] = []
        for page_num, page in enumerate(doc, start=1):
            page_text = page.get_text()
            if page_text:
                text_parts.append(page_text)
            logger.debug("  Page %d: %d characters extracted.", page_num, len(page_text))

        doc.close()

        full_text = "\n".join(text_parts)
        logger.info(
            "Successfully extracted %d characters from '%s'.",
            len(full_text),
            path.name,
        )
        return full_text

    except Exception as exc:
        logger.error("Failed to read PDF '%s': %s", file_path, exc)
        raise RuntimeError(f"Error reading PDF '{file_path}': {exc}") from exc
