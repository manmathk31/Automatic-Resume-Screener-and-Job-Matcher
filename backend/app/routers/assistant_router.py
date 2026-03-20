from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database import crud
from app.schemas import request_schemas, response_schemas
from app.services import assistant_service
from app.core.dependencies import get_current_user

router = APIRouter()

@router.post("/query", response_model=response_schemas.AssistantResponse)
async def query_assistant(req: request_schemas.AssistantQueryRequest, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    context_str = "No specific job context provided. Answer generally."
    
    if req.job_id:
        job = crud.get_job(db, req.job_id)
        if job and job.user_id == current_user.get("user_id"):
            results = crud.get_screening_results_for_job(db, job.id)
            top_10 = results[:10]
            
            context_parts = [f"Job Title: {job.title}", "Top 10 Candidates for this job:"]
            for res in top_10:
                cand = crud.get_candidate(db, res.candidate_id)
                cand_name = cand.name if cand else "Unknown Candidate"
                matched = ", ".join(res.matched_skills) if res.matched_skills else "None"
                missing = ", ".join(res.missing_skills) if res.missing_skills else "None"
                context_parts.append(
                    f"- {cand_name}: Score: {res.score}, Matched: [{matched}], Missing: [{missing}]"
                )
            context_str = "\n".join(context_parts)
            
    response_text = assistant_service.generate_assistant_response(req.query, context_str)
    
    return response_schemas.AssistantResponse(response=response_text)
