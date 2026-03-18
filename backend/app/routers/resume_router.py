from fastapi import APIRouter, File, UploadFile, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.services import pipeline_service, candidate_service, screening_service
from app.schemas import response_schemas

router = APIRouter()

@router.post("/upload", response_model=response_schemas.CandidateResponse)
async def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # In a real scenario, we save the file to a temp location and pass it to pipeline
    # For now, we mock the path
    temp_path = f"/tmp/{file.filename}"
    
    # 1. Extract text and structure
    extracted_data = pipeline_service.process_resume(temp_path)
    
    # 2. Generate embedding for candidate
    # Just combining skills as text representation mock
    text_repr = " ".join(extracted_data.get("skills", []))
    embedding = screening_service.generate_embedding(text_repr)
    
    # 3. Store candidate
    db_candidate = candidate_service.add_candidate(db, extracted_data, embedding)
    
    return db_candidate
