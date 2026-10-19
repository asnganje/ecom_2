from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.modules.auth import service
from app.modules.auth.schema import RegisterRequest, LoginRequest
from app.modules.auth.service import AuthService

router = APIRouter(
    prefix="/auth"
)

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=dict)
def register(payload:RegisterRequest, db: Session= Depends(get_db))->dict:
    service = AuthService(db)
    response = service.register(payload)
    return response

@router.post("/login", status_code=status.HTTP_200_OK)
def login(payload:LoginRequest, db:Session = Depends(get_db)):
    l_service=AuthService(db)
    response = l_service.login(payload)
    return response