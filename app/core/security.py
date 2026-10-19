from datetime import datetime, timedelta, timezone
from pwdlib import PasswordHash
from fastapi import HTTPException, status
import jwt

from app.database.session import settings

password_hash = PasswordHash.recommended()

def hash_pass(password:str)->str:
    return password_hash.hash(password)

def verify_pass(password:str, hashed_pass:str)->bool:
    return password_hash.verify(password, hashed_pass)

def create_access_token(subject:str, role:str)->str:
    expires_at=datetime.now(timezone.utc)+timedelta(minutes=60)
    payload= {
        "sub":subject,
        "role":role,
        "exp":expires_at
    }

    token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    return token

def decode_access_token(token:str)->dict:
    try:
        return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except jwt.ExpiredSignatureError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
