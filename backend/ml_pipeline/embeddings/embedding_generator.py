"""
Embedding generation module.

Uses the ``sentence-transformers`` library to convert text into dense
vector embeddings suitable for semantic similarity computation.

Model: ``all-MiniLM-L6-v2`` (384-dimensional vectors).
"""

import logging
from typing import List, Optional

import numpy as np

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Lazy-loaded singleton model instance
# ---------------------------------------------------------------------------
_model = None


def _get_model():
    """Return the shared SentenceTransformer model, loading it on first call."""
    global _model
    if _model is None:
        logger.info("Loading sentence-transformer model (all-MiniLM-L6-v2)…")
        from sentence_transformers import SentenceTransformer

        _model = SentenceTransformer("all-MiniLM-L6-v2")
        logger.info("Model loaded successfully.")
    return _model


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def generate_embedding(text: str) -> Optional[np.ndarray]:
    """Generate a 384-dim embedding vector for a single text string.

    Args:
        text: Input text (resume or job description).

    Returns:
        A numpy array of shape ``(384,)``, or ``None`` if the input
        text is empty.
    """
    if not text or not text.strip():
        logger.warning("Empty text provided; returning None.")
        return None

    logger.info("Generating embedding for text (%d chars).", len(text))
    model = _get_model()
    embedding = model.encode(text, convert_to_numpy=True)
    logger.info("Embedding generated — shape: %s", embedding.shape)
    return embedding


def generate_embeddings_batch(texts: List[str]) -> List[Optional[np.ndarray]]:
    """Generate embeddings for a list of texts in a single batch call.

    This is significantly faster than calling ``generate_embedding``
    in a loop because the model can parallelise computation internally.

    Args:
        texts: List of input strings.

    Returns:
        List of numpy arrays (one per input text).  An entry is ``None``
        if the corresponding input text was empty.
    """
    if not texts:
        logger.warning("Empty text list provided; returning empty list.")
        return []

    logger.info("Generating batch embeddings for %d texts.", len(texts))

    # Separate valid (non-empty) texts from empty ones
    indices_valid: List[int] = []
    valid_texts: List[str] = []
    for idx, t in enumerate(texts):
        if t and t.strip():
            indices_valid.append(idx)
            valid_texts.append(t)

    # Encode all valid texts at once
    model = _get_model()
    valid_embeddings = model.encode(valid_texts, convert_to_numpy=True, show_progress_bar=False)

    # Reconstruct the result list, putting None for empty inputs
    results: List[Optional[np.ndarray]] = [None] * len(texts)
    for i, idx in enumerate(indices_valid):
        results[idx] = valid_embeddings[i]

    logger.info("Batch embedding complete — %d / %d texts embedded.", len(valid_texts), len(texts))
    return results
