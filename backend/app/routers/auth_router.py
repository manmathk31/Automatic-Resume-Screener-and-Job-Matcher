from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from app.core.limiter import limiter
from app.database.database import get_db
from app.database import crud
from app.core import security

router = APIRouter()

class UserRegister(BaseModel):
    name: str = Field(..., max_length=100)
    email: str = Field(..., max_length=255)
    password: str = Field(..., min_length=8, max_length=100)

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/register")
@limiter.limit("5/minute")
async def register(request: Request, user: UserRegister, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = security.hash_password(user.password)
    new_user = crud.create_user(db, email=user.email, name=user.name, hashed_password=hashed_password)
    return {"id": new_user.id, "email": new_user.email, "name": new_user.name}

@router.post("/login", response_model=Token)
@limiter.limit("5/minute")
async def login(request: Request, user: UserLogin, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if not db_user or not security.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = security.create_access_token(data={"user_id": db_user.id, "email": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}
