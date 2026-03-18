from sqlalchemy.orm import Session
from app.database import crud
from app.schemas import request_schemas

def add_candidate(db: Session, extracted_info: dict, embedding: list = None):
    candidate_in = request_schemas.CandidateCreate(
        name=extracted_info.get("name", "Unknown"),
        skills=extracted_info.get("skills", []),
        experience_years=extracted_info.get("experience_years", 0.0),
        education=extracted_info.get("education"),
        projects=extracted_info.get("projects"),
        embedding=embedding
    )
    return crud.create_candidate(db=db, candidate=candidate_in)
