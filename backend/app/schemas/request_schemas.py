from pydantic import BaseModel
from typing import List, Optional

class CandidateCreate(BaseModel):
    name: str
    skills: List[str]
    experience_years: float = 0.0
    education: Optional[str] = None
    projects: Optional[List[str]] = None
    embedding: Optional[List[float]] = None

class JobCreate(BaseModel):
    title: str
    description: str
    required_skills: List[str]

class ScreeningRunRequest(BaseModel):
    job_id: int

class AssistantQueryRequest(BaseModel):
    query: str
