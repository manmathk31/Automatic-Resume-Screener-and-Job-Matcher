from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database import crud
from app.schemas import request_schemas, response_schemas
from app.services import screening_service

router = APIRouter()

@router.post("/create", response_model=response_schemas.JobResponse)
async def create_job(job: request_schemas.JobCreate, db: Session = Depends(get_db)):
    text_repr = job.description + " " + " ".join(job.required_skills)
    embedding = screening_service.generate_embedding(text_repr)
    return crud.create_job(db=db, job=job, embedding=embedding)
