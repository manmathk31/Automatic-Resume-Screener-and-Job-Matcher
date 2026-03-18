from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database import crud
from app.schemas import request_schemas, response_schemas
from app.services import assistant_service

router = APIRouter()

@router.post("/query", response_model=response_schemas.AssistantResponse)
async def query_assistant(req: request_schemas.AssistantQueryRequest, db: Session = Depends(get_db)):
    # Build simple context from DB
    candidates = crud.get_candidates(db, limit=5)
    context_str = ", ".join([f"{c.name} (Skills: {', '.join(c.skills)})" for c in candidates]) if candidates else "No candidates in DB."
    
    response_text = assistant_service.generate_assistant_response(req.query, context_str)
    return {"response": response_text}
