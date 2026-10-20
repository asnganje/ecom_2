from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import status

from app.core.dependency import get_db, get_current_user
from app.modules.users.model import User
from app.modules.users.schema import UserRead, UserUpdate, UserRole
from app.modules.users.service import UserService

router = APIRouter(prefix="/users")

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[UserRead])
def list_users(current_user:User=Depends(get_current_user), db:Session=Depends(get_db)):
    if current_user.role != UserRole.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only admin can view those resources!"
        )
    service = UserService(db)
    users = service.list_users()
    return users

@router.get("/profile", status_code=status.HTTP_200_OK, response_model=UserRead)
def get_current_user_profile(current_user:User=Depends(get_current_user), db:Session=Depends(get_db)):
    u_service = UserService(db)
    user = u_service.get_current_user(current_user)
    return user

@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserRead)
def get_user(user_id:int, db:Session=Depends(get_db)):
    service = UserService(db)
    user = service.get_user(user_id)
    return user

@router.patch("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserRead)
def update_user(user_id:int, payload:UserUpdate, db:Session=Depends(get_db)):
    service = UserService(db)
    user = service.update_user(user_id, payload)
    return user

@router.delete("/{user_id}", status_code=status.HTTP_200_OK, response_model=dict)
def delete_user(user_id:int, db: Session=Depends(get_db)):
    service = UserService(db)
    service.delete_user(user_id)
    return {
        "msg":"user deleted successfully!"
    }

