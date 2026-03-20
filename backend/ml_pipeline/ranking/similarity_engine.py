"""
Similarity engine module.

Computes cosine similarity between embedding vectors
(e.g. resume vs. job-description embeddings).
"""

import logging

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)


def compute_similarity(
    resume_embedding: np.ndarray,
    job_embedding: np.ndarray,
) -> float:
    """Compute cosine similarity between two embedding vectors.

    Args:
        resume_embedding: 1-D numpy array (candidate embedding).
        job_embedding: 1-D numpy array (job-description embedding).

    Returns:
        Similarity score clipped to the range [0.0, 1.0].

    Raises:
        ValueError: If either embedding is ``None``.
    """
    if resume_embedding is None or job_embedding is None:
        logger.error("One or both embeddings are None.")
        raise ValueError("Embeddings must not be None.")

    # sklearn expects 2-D arrays → reshape
    score = cosine_similarity(
        resume_embedding.reshape(1, -1),
        job_embedding.reshape(1, -1),
    )[0][0]

    # Clip to [0, 1] (cosine similarity can occasionally be < 0)
    score = float(np.clip(score, 0.0, 1.0))

    logger.info("Cosine similarity: %.4f", score)
    return score
