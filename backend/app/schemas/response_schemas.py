from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class CandidateResponse(BaseModel):
    id: int
    name: str
    skills: List[str]
    experience_years: float
    education: Optional[str]
    projects: Optional[List[str]]
    created_at: datetime
    
    class Config:
        from_attributes = True

class CandidateRankingResponse(BaseModel):
    candidate_id: int
    name: str
    score: float
    matched_skills: List[str]
    missing_skills: List[str]
    rank: int

class JobResponse(BaseModel):
    id: int
    title: str
    description: str
    required_skills: List[str]
    created_at: datetime

    class Config:
        from_attributes = True

class AssistantResponse(BaseModel):
    response: str
