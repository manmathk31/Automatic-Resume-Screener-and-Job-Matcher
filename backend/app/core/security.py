from datetime import datetime, timedelta
import os
from passlib.context import CryptContext
from jose import JWTError, jwt
try:
    from decouple import config
    SECRET_KEY = config("SECRET_KEY", default="supersecret")
except ImportError:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 24 * 60

import bcrypt

def hash_password(plain: str) -> str:
    # bcrypt limits passwords to 72 bytes. We safely truncate.
    pwd_bytes = plain.encode('utf-8')[:72]
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain: str, hashed: str) -> bool:
    pwd_bytes = plain.encode('utf-8')[:72]
    try:
        return bcrypt.checkpw(pwd_bytes, hashed.encode('utf-8'))
    except ValueError:
        return False

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> dict:
    from fastapi import HTTPException
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
