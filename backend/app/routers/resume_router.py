import os
import logging
from typing import List
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.services import candidate_service
from app.schemas import response_schemas
from app.core.dependencies import get_current_user

from ml_pipeline.resume_parser.pdf_extractor import extract_resume_text
from ml_pipeline.resume_parser.text_cleaner import clean_resume_text
from ml_pipeline.skill_extraction.skill_detector import extract_skills
from ml_pipeline.embeddings.embedding_generator import generate_embedding

logger = logging.getLogger(__name__)

router = APIRouter()

def process_single_resume(file_path: str, filename: str, db: Session, user_id: int = None):
    try:
        raw_text = extract_resume_text(file_path)
        cleaned_text = clean_resume_text(raw_text)
        skills = extract_skills(cleaned_text)
        embedding_arr = generate_embedding(cleaned_text)
        embedding_list = embedding_arr.tolist() if embedding_arr is not None else []
        
        name = filename.lower()
        if name.endswith(".pdf"):
            name = name[:-4]
        name = name.replace("_", " ").replace("-", " ").title()
        
        extracted_data = {
            "name": name,
            "skills": skills
        }
        
        db_candidate = candidate_service.add_candidate(db, extracted_data, embedding_list)
        if user_id is not None:
            db_candidate.user_id = user_id
            db.commit()
            db.refresh(db_candidate)
        return db_candidate
    except Exception as e:
        logger.error(f"Failed to process {filename}: {e}")
        return None

@router.post("/upload", response_model=response_schemas.CandidateResponse)
async def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    contents = await file.read()
    if not contents.startswith(b"%PDF"):
        raise HTTPException(status_code=400, detail="Invalid file format. Magic bytes do not match %PDF.")
        
    temp_path = f"/tmp/{file.filename}"
    try:
        # Create /tmp directory if it doesn't exist (e.g. on Windows)
        os.makedirs("/tmp", exist_ok=True)
        with open(temp_path, "wb") as f:
            f.write(contents)
            
        db_candidate = process_single_resume(temp_path, file.filename, db, user_id=current_user.get("user_id"))
        if db_candidate is None:
            raise Exception("Failed to process resume")
        return db_candidate
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@router.post("/upload-batch", response_model=List[response_schemas.CandidateResponse])
async def upload_resume_batch(files: List[UploadFile] = File(...), db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    created_candidates = []
    # Create /tmp directory if it doesn't exist (e.g. on Windows)
    os.makedirs("/tmp", exist_ok=True)
    for file in files:
        if not file.filename.lower().endswith(".pdf"):
            logger.warning(f"File {file.filename} skipped: Not a .pdf extension")
            continue
        contents = await file.read()
        if not contents.startswith(b"%PDF"):
            logger.warning(f"File {file.filename} skipped: Magic bytes do not match %PDF")
            continue
            
        temp_path = f"/tmp/{file.filename}"
        try:
            with open(temp_path, "wb") as f:
                f.write(contents)
                
            db_candidate = process_single_resume(temp_path, file.filename, db, user_id=current_user.get("user_id"))
            if db_candidate:
                created_candidates.append(db_candidate)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
    return created_candidates
