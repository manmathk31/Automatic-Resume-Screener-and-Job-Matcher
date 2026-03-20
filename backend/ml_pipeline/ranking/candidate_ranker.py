"""
Candidate ranking module.

Combines semantic similarity and skill-match scores to produce a
final ranked list of candidates for a given job description.

Scoring formula:
    final_score = 0.7 * semantic_similarity + 0.3 * skill_match_score
"""

import logging
from typing import List

from ml_pipeline.embeddings.embedding_generator import (
    generate_embedding,
    generate_embeddings_batch,
)
from ml_pipeline.models.candidate import Candidate
from ml_pipeline.ranking.similarity_engine import compute_similarity
from ml_pipeline.skill_extraction.skill_detector import (
    compute_skill_match_score,
    detect_missing_skills,
    extract_skills,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Weights for the final score
# ---------------------------------------------------------------------------
SEMANTIC_WEIGHT: float = 0.7
SKILL_WEIGHT: float = 0.3


def rank_candidates(
    candidates: List[Candidate],
    job_description: str,
) -> List[Candidate]:
    """Rank a list of candidates against a job description.

    Steps performed:
        1. Extract required skills from the job description.
        2. Generate the job-description embedding.
        3. Generate resume embeddings in batch.
        4. For each candidate compute:
            a. Semantic similarity score.
            b. Skill match score & missing skills.
            c. Final weighted score.
        5. Sort candidates by ``final_score`` descending.

    Args:
        candidates: List of ``Candidate`` instances with ``cleaned_text``
            and ``skills`` already populated.
        job_description: Raw or cleaned job description string.

    Returns:
        The same list of ``Candidate`` objects, mutated with scores
        filled in and sorted from best to worst.
    """
    if not candidates:
        logger.warning("No candidates to rank.")
        return []

    # ---- 1. Extract required skills from the JD ----
    logger.info("Extracting required skills from job description.")
    required_skills = extract_skills(job_description.lower())
    logger.info("Required skills: %s", required_skills)

    # ---- 2. Job-description embedding ----
    logger.info("Generating job-description embedding.")
    jd_embedding = generate_embedding(job_description)
    if jd_embedding is None:
        logger.error("Could not generate JD embedding; aborting ranking.")
        return candidates

    # ---- 3. Batch-embed all resumes ----
    logger.info("Generating batch embeddings for %d resumes.", len(candidates))
    resume_texts = [c.cleaned_text for c in candidates]
    resume_embeddings = generate_embeddings_batch(resume_texts)

    # ---- 4. Score each candidate ----
    for idx, candidate in enumerate(candidates):
        emb = resume_embeddings[idx]
        candidate.embedding = emb

        # Semantic similarity
        if emb is not None:
            candidate.semantic_score = compute_similarity(emb, jd_embedding)
        else:
            candidate.semantic_score = 0.0
            logger.warning("No embedding for '%s'; semantic score = 0.", candidate.name)

        # Skill match
        candidate.skill_match_score = compute_skill_match_score(
            candidate.skills, required_skills
        )
        candidate.missing_skills = detect_missing_skills(
            candidate.skills, required_skills
        )

        # Final weighted score
        candidate.final_score = (
            SEMANTIC_WEIGHT * candidate.semantic_score
            + SKILL_WEIGHT * candidate.skill_match_score
        )

        logger.info(
            "Candidate '%s' — semantic=%.4f  skill=%.4f  final=%.4f",
            candidate.name,
            candidate.semantic_score,
            candidate.skill_match_score,
            candidate.final_score,
        )

    # ---- 5. Sort descending by final_score ----
    candidates.sort(key=lambda c: c.final_score, reverse=True)
    logger.info("Candidates ranked successfully.")
    return candidates
