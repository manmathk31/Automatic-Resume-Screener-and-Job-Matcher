from sqlalchemy.orm import Session
from app.models import candidate_model, job_model, screening_model
from app.schemas import request_schemas
from app.models.user_model import User

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, email: str, name: str, hashed_password: str):
    db_user = User(email=email, name=name, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_candidate(db: Session, candidate_id: int):
    return db.query(candidate_model.Candidate).filter(candidate_model.Candidate.id == candidate_id).first()

def get_candidates_count(db: Session, user_id: int):
    return db.query(candidate_model.Candidate).filter(candidate_model.Candidate.user_id == user_id).count()

def get_candidates(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(candidate_model.Candidate).filter(candidate_model.Candidate.user_id == user_id).offset(skip).limit(limit).all()

def create_candidate(db: Session, candidate: request_schemas.CandidateCreate, user_id: int = None):
    db_candidate = candidate_model.Candidate(
        name=candidate.name,
        skills=candidate.skills,
        experience_years=candidate.experience_years,
        education=candidate.education,
        projects=candidate.projects,
        embedding=candidate.embedding,
        user_id=user_id
    )
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)
    return db_candidate

def get_jobs_count(db: Session, user_id: int):
    return db.query(job_model.Job).filter(job_model.Job.user_id == user_id).count()

def get_jobs(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(job_model.Job).filter(job_model.Job.user_id == user_id).offset(skip).limit(limit).all()

def create_job(db: Session, job: request_schemas.JobCreate, user_id: int = None, embedding: list = None):
    db_job = job_model.Job(
        title=job.title,
        description=job.description,
        required_skills=job.required_skills,
        embedding=embedding,
        user_id=user_id
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

def delete_screening_results_for_candidate(db: Session, candidate_id: int):
    db.query(screening_model.ScreeningResult).filter(screening_model.ScreeningResult.candidate_id == candidate_id).delete()
    db.commit()

def delete_candidate(db: Session, candidate_id: int):
    candidate = db.query(candidate_model.Candidate).filter(candidate_model.Candidate.id == candidate_id).first()
    if candidate:
        delete_screening_results_for_candidate(db, candidate_id)
        db.delete(candidate)
        db.commit()
        return True
    return False

def delete_screening_results_for_job(db: Session, job_id: int):
    db.query(screening_model.ScreeningResult).filter(screening_model.ScreeningResult.job_id == job_id).delete()
    db.commit()

def delete_job(db: Session, job_id: int):
    job = db.query(job_model.Job).filter(job_model.Job.id == job_id).first()
    if job:
        delete_screening_results_for_job(db, job_id)
        db.delete(job)
        db.commit()
        return True
    return False
