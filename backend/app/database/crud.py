from sqlalchemy.orm import Session
from app.models import candidate_model, job_model, screening_model
from app.schemas import request_schemas

def get_candidate(db: Session, candidate_id: int):
    return db.query(candidate_model.Candidate).filter(candidate_model.Candidate.id == candidate_id).first()

def get_candidates(db: Session, skip: int = 0, limit: int = 100):
    return db.query(candidate_model.Candidate).offset(skip).limit(limit).all()

def create_candidate(db: Session, candidate: request_schemas.CandidateCreate):
    db_candidate = candidate_model.Candidate(
        name=candidate.name,
        skills=candidate.skills,
        experience_years=candidate.experience_years,
        education=candidate.education,
        projects=candidate.projects,
        embedding=candidate.embedding
    )
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)
    return db_candidate

def create_job(db: Session, job: request_schemas.JobCreate, embedding: list = None):
    db_job = job_model.Job(
        title=job.title,
        description=job.description,
        required_skills=job.required_skills,
        embedding=embedding
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

def get_job(db: Session, job_id: int):
    return db.query(job_model.Job).filter(job_model.Job.id == job_id).first()

def create_screening_result(db: Session, job_id: int, candidate_id: int, score: float, matched: list, missing: list, rank: int):
    result = screening_model.ScreeningResult(
        job_id=job_id,
        candidate_id=candidate_id,
        score=score,
        matched_skills=matched,
        missing_skills=missing,
        rank=rank
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    return result

def get_screening_results_for_job(db: Session, job_id: int):
    return db.query(screening_model.ScreeningResult).filter(screening_model.ScreeningResult.job_id == job_id).order_by(screening_model.ScreeningResult.rank).all()
