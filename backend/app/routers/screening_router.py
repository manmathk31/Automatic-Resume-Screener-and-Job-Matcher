from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database import crud
from app.schemas import request_schemas, response_schemas
from app.services import screening_service, explanation_service
from typing import List

router = APIRouter()

@router.post("/run", response_model=List[response_schemas.CandidateRankingResponse])
async def run_screening(request: request_schemas.ScreeningRunRequest, db: Session = Depends(get_db)):
    job = crud.get_job(db, request.job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    candidates = crud.get_candidates(db)
    if not candidates:
        return []

    # Prepare data for ranking
    job_embedding = job.embedding
    candidate_embeddings = {c.id: c.embedding for c in candidates}

    ranks = screening_service.rank_candidates(job_embedding, candidate_embeddings)
    
    results = []
    current_rank = 1
    for candidate_id, score in ranks.items():
        candidate = crud.get_candidate(db, candidate_id)
        
        # Calculate explanation (matched/missing skills)
        explanation = explanation_service.explain_score(candidate.skills, job.required_skills)
        matched_skills = explanation.get("matched_skills", [])
        missing_skills = explanation.get("missing_skills", [])
        
        # Save screening result
        crud.create_screening_result(
            db=db,
            job_id=job.id,
            candidate_id=candidate.id,
            score=score,
            matched=matched_skills,
            missing=missing_skills,
            rank=current_rank
        )
        
        results.append(response_schemas.CandidateRankingResponse(
            candidate_id=candidate.id,
            name=candidate.name,
            score=score,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            rank=current_rank
        ))
        current_rank += 1

    return results
