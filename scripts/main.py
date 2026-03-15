"""
Demo script — AI Resume Screening Pipeline.

Run from the project root:
    python -m scripts.main

Or directly:
    python scripts/main.py

Make sure the ``ml_pipeline`` package is importable (i.e. you are
running from the repository root).
"""

import json
import logging
import sys
import os

# Ensure the project root is on the Python path so that ``ml_pipeline``
# can be imported when running the script directly.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from ml_pipeline.pipeline import run_screening  # noqa: E402


def main():
    """Run a sample screening pipeline."""

    # ------------------------------------------------------------------
    # Configure logging — show INFO and above on the console
    # ------------------------------------------------------------------
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%H:%M:%S",
    )

    # ------------------------------------------------------------------
    # Sample inputs  (replace with real PDF paths on your machine)
    # ------------------------------------------------------------------
    resumes = [
        "resumes/resume1.pdf",
        "resumes/resume2.pdf",
        "resumes/resume3.pdf",
    ]

    job_description = (
        "Looking for a Machine Learning Engineer with strong experience in "
        "Python, NLP, Deep Learning, and TensorFlow. "
        "Experience with Docker and Kubernetes is a plus. "
        "Must have solid skills in Data Analysis and SQL."
    )

    # ------------------------------------------------------------------
    # Run the pipeline
    # ------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("   AI RESUME SCREENING & JOB MATCHER")
    print("=" * 60 + "\n")

    results = run_screening(resumes, job_description)

    # ------------------------------------------------------------------
    # Display results
    # ------------------------------------------------------------------
    if not results["ranked_candidates"]:
        print("No candidates could be processed. Check file paths and logs.")
        return

    print("\n" + "-" * 60)
    print("   RANKED CANDIDATES")
    print("-" * 60)
    for rank, candidate in enumerate(results["ranked_candidates"], start=1):
        print(f"\n  #{rank}  {candidate['name']}")
        print(f"       Final Score       : {candidate['final_score']:.4f}")
        print(f"       Semantic Score    : {candidate['semantic_score']:.4f}")
        print(f"       Skill Match Score : {candidate['skill_match_score']:.4f}")
        print(f"       Skills            : {', '.join(candidate['skills']) or 'None detected'}")
        print(f"       Missing Skills    : {', '.join(candidate['missing_skills']) or 'None'}")

    print("\n" + "-" * 60)
    print("   SKILL COMPARISON")
    print("-" * 60)
    print(json.dumps(results["skill_comparison"], indent=2))

    print("\n" + "=" * 60)
    print("   SCREENING COMPLETE")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
