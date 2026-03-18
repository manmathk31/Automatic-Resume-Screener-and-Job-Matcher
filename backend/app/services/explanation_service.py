from typing import List, Dict

def explain_score(candidate_skills: List[str], required_skills: List[str]) -> Dict[str, List[str]]:
    candidate_set = set(s.lower() for s in candidate_skills) if candidate_skills else set()
    required_set = set(s.lower() for s in required_skills) if required_skills else set()
    
    matched = list(candidate_set.intersection(required_set))
    missing = list(required_set.difference(candidate_set))
    
    # Optional logic to formulate a paragraph
    explanation_text = f"Candidate matches {len(matched)} of {len(required_set)} required skills. "
    if missing:
        explanation_text += f"Missing experience in: {', '.join(missing)}."
    else:
        explanation_text += "Strong match across all requirements."
        
    return {
        "matched_skills": [s.title() for s in matched],
        "missing_skills": [s.title() for s in missing],
        "explanation": explanation_text
    }
