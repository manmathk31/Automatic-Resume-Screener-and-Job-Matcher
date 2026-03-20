"""
Pipeline orchestrator.

Connects all modules into a single ``run_screening`` function that
takes a list of resume file paths and a job description, then returns
ranked candidates.

Pipeline stages:
    1. Load and extract text from PDF resumes.
    2. Clean the extracted text.
    3. Extract skills from each resume.
    4. Rank candidates (embedding + similarity + skill matching).
"""

import logging
import os
from typing import Dict, List

from ml_pipeline.models.candidate import Candidate
from ml_pipeline.ranking.candidate_ranker import rank_candidates
from ml_pipeline.resume_parser.pdf_extractor import extract_resume_text
from ml_pipeline.resume_parser.text_cleaner import clean_resume_text
from ml_pipeline.skill_extraction.skill_detector import (
    compare_candidates_skills,
    extract_skills,
)

logger = logging.getLogger(__name__)


def _derive_candidate_name(file_path: str) -> str:
    """Derive a human-readable candidate name from the PDF filename.

    Example:
        ``"resumes/Alice_Smith.pdf"`` → ``"Alice Smith"``
    """
    base = os.path.splitext(os.path.basename(file_path))[0]
    # Replace underscores/hyphens with spaces and title-case
    return base.replace("_", " ").replace("-", " ").title()


def run_screening(
    resume_files: List[str],
    job_description: str,
) -> List[Dict]:
    """Execute the full resume-screening pipeline.

    Args:
        resume_files: List of file paths to PDF resumes.
        job_description: The job description text to match against.

    Returns:
        List of candidate dictionaries sorted by ``final_score``
        (descending).  Each dict contains: name, resume_path, skills,
        semantic_score, skill_match_score, missing_skills, final_score.
    """
    logger.info("=" * 60)
    logger.info("STARTING RESUME SCREENING PIPELINE")
    logger.info("Resumes: %d | JD length: %d chars", len(resume_files), len(job_description))
    logger.info("=" * 60)

    candidates: List[Candidate] = []

    for file_path in resume_files:
        name = _derive_candidate_name(file_path)
        logger.info("Processing candidate: %s", name)

        # --- Stage 1: Extract text ---
        try:
            raw_text = extract_resume_text(file_path)
        except (FileNotFoundError, RuntimeError) as exc:
            logger.error("Skipping '%s': %s", name, exc)
            continue

        # --- Stage 2: Clean text ---
        cleaned = clean_resume_text(raw_text)

        # --- Stage 3: Extract skills ---
        skills = extract_skills(cleaned)

        # Build Candidate object
        candidate = Candidate(
            name=name,
            resume_path=file_path,
            cleaned_text=cleaned,
            skills=skills,
        )
        candidates.append(candidate)

    if not candidates:
        logger.warning("No valid candidates after parsing. Returning empty list.")
        return []

    # --- Stage 4: Rank candidates ---
    logger.info("Ranking %d candidates against the job description.", len(candidates))
    ranked = rank_candidates(candidates, job_description)

    # --- Build comparison report ---
    candidates_data = [{"name": c.name, "skills": c.skills} for c in ranked]
    comparison = compare_candidates_skills(candidates_data)

    # --- Serialise results ---
    results = [c.to_dict() for c in ranked]

    logger.info("=" * 60)
    logger.info("SCREENING COMPLETE — Top candidate: %s (score %.4f)",
                results[0]["name"] if results else "N/A",
                results[0]["final_score"] if results else 0.0)
    logger.info("=" * 60)

    return {
        "ranked_candidates": results,
        "skill_comparison": comparison,
    }
