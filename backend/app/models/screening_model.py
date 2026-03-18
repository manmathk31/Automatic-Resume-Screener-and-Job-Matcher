from sqlalchemy import Column, Integer, Float, JSON, ForeignKey
from app.database.database import Base

class ScreeningResult(Base):
    __tablename__ = "screening_results"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    score = Column(Float)
    matched_skills = Column(JSON)
    missing_skills = Column(JSON)
    rank = Column(Integer, nullable=True)
