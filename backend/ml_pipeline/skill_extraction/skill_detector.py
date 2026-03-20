"""
Skill detection module.

Extracts technical and professional skills from text using
keyword matching against a predefined, extensible skill list.
This module is used for both resume and job-description skill extraction.
"""

import logging
import re
from typing import Dict, List

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Predefined skill list (extensible)
# ---------------------------------------------------------------------------
SKILL_LIST: List[str] = [
    "Python",
    "Java",
    "C++",
    "C",
    "JavaScript",
    "TypeScript",
    "Go",
    "Rust",
    "SQL",
    "NoSQL",
    "MongoDB",
    "PostgreSQL",
    "MySQL",
    "Machine Learning",
    "Deep Learning",
    "NLP",
    "Natural Language Processing",
    "Computer Vision",
    "Data Analysis",
    "Data Science",
    "Data Engineering",
    "TensorFlow",
    "PyTorch",
    "Keras",
    "Scikit-learn",
    "Pandas",
    "NumPy",
    "OpenCV",
    "Docker",
    "Kubernetes",
    "AWS",
    "Azure",
    "GCP",
    "Git",
    "Linux",
    "REST API",
    "FastAPI",
    "Flask",
    "Django",
    "React",
    "Node.js",
    "HTML",
    "CSS",
    "Power BI",
    "Tableau",
    "Excel",
    "Spark",
    "Hadoop",
    "ETL",
    "CI/CD",
    "Agile",
    "Scrum",
]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def extract_skills(text: str) -> List[str]:
    """Extract skills from text using case-insensitive keyword matching.

    Each skill in the predefined list is searched for as a whole-word
    match inside the provided text. This function works for both
    resume text and job description text.

    Args:
        text: Cleaned text (resume or job description).

    Returns:
        Sorted list of unique detected skills (original casing from SKILL_LIST).
    """
    if not text:
        logger.warning("Received empty text for skill extraction.")
        return []

    logger.info("Extracting skills from text (%d characters).", len(text))
    text_lower = text.lower()

    detected: List[str] = []
    for skill in SKILL_LIST:
        escaped = re.escape(skill.lower())

        # For skills with non-word characters (e.g. "c++", "ci/cd", "node.js"),
        # \b won't work at those boundaries, so use look-behind/look-ahead
        # that assert a non-alphanumeric char (or start/end of string).
        if not skill[0].isalnum():
            left = r"(?<![a-z0-9])"
        else:
            left = r"\b"

        if not skill[-1].isalnum():
            right = r"(?![a-z0-9])"
        else:
            right = r"\b"

        pattern = left + escaped + right
        if re.search(pattern, text_lower):
            detected.append(skill)

    detected = sorted(set(detected))
    logger.info("Detected %d skills: %s", len(detected), detected)
    return detected


def detect_missing_skills(
    candidate_skills: List[str],
    required_skills: List[str],
) -> List[str]:
    """Identify required skills that the candidate does not possess.

    Args:
        candidate_skills: Skills extracted from the candidate's resume.
        required_skills: Skills extracted from the job description.

    Returns:
        List of skills present in *required_skills* but absent from
        *candidate_skills*.
    """
    candidate_set = {s.lower() for s in candidate_skills}
    missing = [s for s in required_skills if s.lower() not in candidate_set]
    logger.info("Missing skills: %s", missing)
    return missing


def compute_skill_match_score(
    candidate_skills: List[str],
    required_skills: List[str],
) -> float:
    """Compute the fraction of required skills matched by the candidate.

    Formula:
        skill_match_score = matched_skills / total_required_skills

    Args:
        candidate_skills: Skills extracted from the candidate's resume.
        required_skills: Skills extracted from the job description.

    Returns:
        Score between 0.0 and 1.0.  Returns 0.0 if there are no
        required skills (avoids division by zero).
    """
    if not required_skills:
        logger.warning("No required skills provided; returning 0.0.")
        return 0.0

    candidate_set = {s.lower() for s in candidate_skills}
    matched = sum(1 for s in required_skills if s.lower() in candidate_set)
    score = matched / len(required_skills)

    logger.info(
        "Skill match: %d / %d = %.4f",
        matched,
        len(required_skills),
        score,
    )
    return score


def compare_candidates_skills(
    candidates_data: List[Dict],
) -> Dict:
    """Compare skills across multiple candidates.

    Args:
        candidates_data: List of dicts, each with keys ``"name"`` and
            ``"skills"`` (a list of skill strings).

    Returns:
        Dictionary with:
            - ``"common_skills"``: skills shared by *all* candidates.
            - ``"unique_skills"``: mapping of candidate name to skills
              unique to that candidate.
            - ``"all_skills"``: union of every candidate's skills.
    """
    if not candidates_data:
        return {"common_skills": [], "unique_skills": {}, "all_skills": []}

    # Build per-candidate skill sets
    skill_sets: Dict[str, set[str]] = {
        c["name"]: set(c["skills"]) for c in candidates_data
    }

    all_skills: set[str] = set()
    for s in skill_sets.values():
        all_skills.update(s)

    # Common skills (intersection)
    common: set[str] = set()
    if skill_sets:
        skill_sets_iter = iter(skill_sets.values())
        common = next(skill_sets_iter).copy()
        for s in skill_sets_iter:
            common &= s

    # Unique skills per candidate
    unique: Dict[str, List[str]] = {}
    for name, skills in skill_sets.items():
        others: set[str] = set()
        for other_name, other_skills in skill_sets.items():
            if other_name != name:
                others.update(other_skills)
        unique[name] = sorted(skills.difference(others))

    result = {
        "common_skills": sorted(common),
        "unique_skills": unique,
        "all_skills": sorted(all_skills),
    }
    logger.info("Candidate skill comparison complete.")
    return result
