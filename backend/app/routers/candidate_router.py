from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.database import get_db
from app.database import crud
from app.schemas import response_schemas
from app.core.dependencies import get_current_user

router = APIRouter()

@router.get("/")
async def list_candidates(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    skip = (page - 1) * page_size
    user_id = current_user.get("user_id")
    items = crud.get_candidates(db, user_id=user_id, skip=skip, limit=page_size)
    total = crud.get_candidates_count(db, user_id=user_id)
    return {"items": items, "page": page, "page_size": page_size, "total": total}

@router.get("/top")
async def get_top_candidates(
    k: int = 10, 
    job_id: Optional[int] = None, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if job_id:
        results = crud.get_screening_results_for_job(db, job_id)
        valid_results = []
        user_id = current_user.get("user_id")
        for r in results:
            candidate = crud.get_candidate(db, r.candidate_id)
            if candidate and candidate.user_id == user_id:
                valid_results.append({"candidate_id": r.candidate_id, "score": r.score, "rank": r.rank})
                if len(valid_results) >= k:
                    break
        return valid_results
    
    # If no job_id is provided, just return paginated candidates (placeholder mock here)
    return []

@router.get("/{candidate_id}", response_model=response_schemas.CandidateResponse)
async def get_candidate(
    candidate_id: int, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    candidate = crud.get_candidate(db, candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    if candidate.user_id != current_user.get("user_id"):
        raise HTTPException(status_code=403, detail="Not authorized to access this candidate")
    return candidate

@router.delete("/{candidate_id}")
async def delete_candidate(candidate_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    candidate = crud.get_candidate(db, candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    if candidate.user_id != current_user.get("user_id"):
        raise HTTPException(status_code=403, detail="Not authorized to delete this candidate")
    crud.delete_candidate(db, candidate_id)
    return {"detail": "Candidate deleted successfully"}
