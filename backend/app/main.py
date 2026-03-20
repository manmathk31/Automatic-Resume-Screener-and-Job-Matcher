from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.routers import resume_router, job_router, screening_router, candidate_router, assistant_router, auth_router
from app.core.limiter import limiter
from app.database.database import get_db
import os
import logging
from logging.handlers import RotatingFileHandler

os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(module)s | %(message)s",
    handlers=[
        logging.StreamHandler(),
        RotatingFileHandler("logs/app.log", maxBytes=5_000_000, backupCount=3)
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Resume Screening API",
    description="Backend API for Datathon 2026 AI Resume Screening + HR Assistant",
    version="1.0.0"
)

# Configure CORS
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
async def ratelimit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many attempts, please wait."}
    )

@app.get("/health", tags=["Health"])
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "ok"}
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return {"status": "ok", "database": "unreachable"}

# Register routers
app.include_router(auth_router.router, prefix="/auth", tags=["Auth"])
app.include_router(resume_router.router, prefix="/resume", tags=["Resume"])
app.include_router(job_router.router, prefix="/jobs", tags=["Jobs"])
app.include_router(screening_router.router, prefix="/screening", tags=["Screening"])
app.include_router(candidate_router.router, prefix="/candidates", tags=["Candidates"])
app.include_router(assistant_router.router, prefix="/assistant", tags=["Assistant"])

@app.get("/")
def read_root():
    return {"message": "Welcome to AI Resume Screening Backend!"}
