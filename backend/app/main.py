from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import resume_router, job_router, screening_router, candidate_router, assistant_router

app = FastAPI(
    title="AI Resume Screening API",
    description="Backend API for Datathon 2026 AI Resume Screening + HR Assistant",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(resume_router.router, prefix="/resume", tags=["Resume"])
app.include_router(job_router.router, prefix="/jobs", tags=["Jobs"])
app.include_router(screening_router.router, prefix="/screening", tags=["Screening"])
app.include_router(candidate_router.router, prefix="/candidates", tags=["Candidates"])
app.include_router(assistant_router.router, prefix="/assistant", tags=["Assistant"])

@app.get("/")
def read_root():
    return {"message": "Welcome to AI Resume Screening Backend!"}
