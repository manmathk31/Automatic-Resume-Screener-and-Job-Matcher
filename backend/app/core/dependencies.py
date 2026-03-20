from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import decode_access_token

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    if not credentials:
        raise HTTPException(status_code=401, detail="Missing auth token")
    token = credentials.credentials
    payload = decode_access_token(token)
    user_id = payload.get("user_id")
    email = payload.get("email")
    if user_id is None or email is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    
    return {"user_id": user_id, "email": email}
