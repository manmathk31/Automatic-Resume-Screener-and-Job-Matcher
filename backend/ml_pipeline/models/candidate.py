"""
Candidate data model for the ML pipeline.

Defines the Candidate dataclass used throughout the pipeline
to carry per-candidate state from parsing through ranking.
"""

from dataclasses import dataclass, field
from typing import List, Optional

import numpy as np


@dataclass
class Candidate:
    """Represents a single candidate flowing through the screening pipeline.

    Attributes:
        name: Display name derived from the resume filename.
        resume_path: Absolute or relative path to the source PDF.
        cleaned_text: Pre-processed resume text (lowercase, no special chars).
        skills: Skills detected in the resume.
        embedding: Sentence-transformer vector for the cleaned text.
        semantic_score: Cosine similarity between resume and JD embeddings.
        skill_match_score: Fraction of required JD skills found in the resume.
        missing_skills: JD skills not found in the resume.
        final_score: Weighted combination of semantic and skill scores.
    """

    name: str = ""
    resume_path: str = ""
    cleaned_text: str = ""
    skills: List[str] = field(default_factory=list)
    embedding: Optional[np.ndarray] = None
    semantic_score: float = 0.0
    skill_match_score: float = 0.0
    missing_skills: List[str] = field(default_factory=list)
    final_score: float = 0.0

    def to_dict(self) -> dict:
        """Convert the candidate to a JSON-serialisable dictionary.

        The embedding is excluded because it is a large numpy array
        that is not useful in API responses.
        """
        return {
            "name": self.name,
            "resume_path": self.resume_path,
            "skills": self.skills,
            "semantic_score": round(self.semantic_score, 4),
            "skill_match_score": round(self.skill_match_score, 4),
            "missing_skills": self.missing_skills,
            "final_score": round(self.final_score, 4),
        }
