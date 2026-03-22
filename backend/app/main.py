from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.routers import resume_router, job_router, screening_router, candidate_router, assistant_router, auth_router
from app.core.limiter import limiter
from app.database.database import get_db
from app.static_files import mount_frontend
import os
import logging
from logging.handlers import RotatingFileHandler

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

log_handlers = [logging.StreamHandler()]
if ENVIRONMENT == "development":
    os.makedirs("logs", exist_ok=True)
    log_handlers.append(
        RotatingFileHandler("logs/app.log", maxBytes=5_000_000, backupCount=3)
    )

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(module)s | %(message)s",
    handlers=log_handlers
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Resume Screening API",
    description="AI Resume Screening + HR Assistant — Datathon 2026",
    version="1.0.0",
    docs_url="/docs" if ENVIRONMENT == "development" else None,
    redoc_url="/redoc" if ENVIRONMENT == "development" else None,
)

# Configure CORS
raw_origins = os.getenv("FRONTEND_URL", "http://localhost:5173")
allowed_origins = [url.strip() for url in raw_origins.split(",")]
for dev_origin in ["http://localhost:5173", "http://localhost:8000"]:
    if dev_origin not in allowed_origins:
        allowed_origins.append(dev_origin)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.limiter = limiter

@app.on_event("startup")
async def validate_environment():
    required_vars = ["DATABASE_URL", "SECRET_KEY", "GEMINI_API_KEY"]
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        logger.error(f"STARTUP FAILED — missing env vars: {missing}")
        raise RuntimeError(f"Missing required environment variables: {missing}")
    logger.info("All required environment variables are present")
    logger.info("Application startup complete")

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

mount_frontend(app)

@app.get("/")
def read_root():
    return {"message": "Welcome to AI Resume Screening Backend!"}
