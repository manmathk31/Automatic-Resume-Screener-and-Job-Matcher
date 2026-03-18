from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.database import get_db
from app.database import crud
from app.schemas import response_schemas

router = APIRouter()

@router.get("/top")
async def get_top_candidates(k: int = 10, job_id: Optional[int] = None, db: Session = Depends(get_db)):
    if job_id:
        results = crud.get_screening_results_for_job(db, job_id)
        return [{"candidate_id": r.candidate_id, "score": r.score, "rank": r.rank} for r in results[:k]]
    
    # If no job_id is provided, just return paginated candidates
    return crud.get_candidates(db, limit=k)

@router.get("/{candidate_id}", response_model=response_schemas.CandidateResponse)
async def get_candidate(candidate_id: int, db: Session = Depends(get_db)):
    candidate = crud.get_candidate(db, candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return candidate
