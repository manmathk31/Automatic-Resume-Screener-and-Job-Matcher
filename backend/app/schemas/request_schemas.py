from pydantic import BaseModel, Field
from typing import List, Optional
try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated

class CandidateCreate(BaseModel):
    name: str
    skills: List[str]
    experience_years: float = 0.0
    education: Optional[str] = None
    projects: Optional[List[str]] = None
    embedding: Optional[List[float]] = None

class JobCreate(BaseModel):
    title: str = Field(..., max_length=200)
    description: str = Field(..., max_length=5000)
    required_skills: List[Annotated[str, Field(max_length=100)]] = Field(..., max_length=30)

class ScreeningRunRequest(BaseModel):
    job_id: int

class AssistantQueryRequest(BaseModel):
    query: str = Field(..., max_length=1000)
    job_id: Optional[int] = None
