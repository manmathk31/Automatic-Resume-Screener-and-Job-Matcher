from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database import crud
from app.schemas import request_schemas, response_schemas
from app.services import screening_service, explanation_service
from typing import List
from app.core.dependencies import get_current_user

from ml_pipeline.skill_extraction.skill_detector import compute_skill_match_score

router = APIRouter()

@router.post("/run", response_model=List[response_schemas.CandidateRankingResponse])
async def run_screening(request: request_schemas.ScreeningRunRequest, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    job = crud.get_job(db, request.job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    candidates = crud.get_candidates(db, user_id=current_user.get("user_id"))
    if not candidates:
        return []

    # Prepare data for ranking
    job_embedding = job.embedding
    candidate_embeddings = {c.id: c.embedding for c in candidates}

    # Semantic similarity dict
    ranks_semantic = screening_service.rank_candidates_real(job_embedding, candidate_embeddings)
    
    candidates_data = []
    for candidate_id, semantic_score in ranks_semantic.items():
        candidate = crud.get_candidate(db, candidate_id)
        
        # Calculate Skill Match Score
        skill_score = compute_skill_match_score(candidate.skills, job.required_skills)
        
        # Calculate Final Score
        final_score = round(0.7 * semantic_score + 0.3 * skill_score, 4)
        
        # Explanation
        explanation = explanation_service.explain_score(candidate.skills, job.required_skills)
        matched_skills = explanation.get("matched_skills", [])
        missing_skills = explanation.get("missing_skills", [])
        
        candidates_data.append({
            "candidate": candidate,
            "final_score": final_score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills
        })

    # Sort candidates by final_score descending
    candidates_data.sort(key=lambda x: x["final_score"], reverse=True)

    results = []
    current_rank = 1
    for data in candidates_data:
        candidate = data["candidate"]
        
        # Save screening result
        crud.create_screening_result(
            db=db,
            job_id=job.id,
            candidate_id=candidate.id,
            score=data["final_score"],
            matched=data["matched_skills"],
            missing=data["missing_skills"],
            rank=current_rank
        )
        
        results.append(response_schemas.CandidateRankingResponse(
            candidate_id=candidate.id,
            name=candidate.name,
            score=data["final_score"],
            matched_skills=data["matched_skills"],
            missing_skills=data["missing_skills"],
            rank=current_rank
        ))
        current_rank += 1

    return results
