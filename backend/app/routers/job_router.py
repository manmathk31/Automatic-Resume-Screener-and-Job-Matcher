from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database import crud
from app.schemas import request_schemas, response_schemas
from app.services.screening_service import generate_embedding_real
from app.core.dependencies import get_current_user

router = APIRouter()

@router.get("/")
async def list_jobs(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    skip = (page - 1) * page_size
    user_id = current_user.get("user_id")
    items = crud.get_jobs(db, user_id=user_id, skip=skip, limit=page_size)
    total = crud.get_jobs_count(db, user_id=user_id)
    return {"items": items, "page": page, "page_size": page_size, "total": total}

@router.post("/create", response_model=response_schemas.JobResponse)
async def create_job(job: request_schemas.JobCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    text_repr = job.description + " " + " ".join(job.required_skills)
    embedding = generate_embedding_real(text_repr)
    return crud.create_job(db=db, job=job, embedding=embedding, user_id=current_user.get("user_id"))

@router.delete("/{job_id}")
async def delete_job(job_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    job = crud.get_job(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.user_id != current_user.get("user_id"):
        raise HTTPException(status_code=403, detail="Not authorized to delete this job")
    crud.delete_job(db, job_id)
    return {"detail": "Job deleted successfully"}
