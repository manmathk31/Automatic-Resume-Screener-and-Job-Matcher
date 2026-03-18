from sqlalchemy import Column, Integer, String, Float, JSON, DateTime
from datetime import datetime
from app.database.database import Base

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    skills = Column(JSON)
    experience_years = Column(Float, default=0.0)
    education = Column(String, nullable=True)
    projects = Column(JSON, nullable=True)
    embedding = Column(JSON, nullable=True) # Storing embedding as JSON for SQLite, use vector DB later
    created_at = Column(DateTime, default=datetime.utcnow)
