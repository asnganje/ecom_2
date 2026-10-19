from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.core.security import hash_pass, create_access_token, verify_pass
from app.modules.auth.schema import RegisterRequest, LoginRequest
from app.modules.users.model import User
from app.modules.users.repository import UserRepository
from app.modules.users.schema import UserRole, UserRead


class AuthService:
    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)

    def _dump_user(self, user:User)->dict:
        return UserRead.model_validate(user).model_dump()

    def register(self, payload:RegisterRequest)->dict:
        existing_user = self.user_repository.get_by_email(payload.email)
        if existing_user is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists"
            )
        user = User(
            fullname=payload.fullname,
            email=payload.email,
            password_hash=hash_pass(payload.password),
            is_active=True,
            role=UserRole.CUSTOMER.value
        )
        db_user = self.user_repository.create_user(user)
        created_user = self._dump_user(db_user)
        access_token = create_access_token(str(db_user.id), db_user.role)
        return {
            "access_token":access_token,
            "user":created_user
        }
    def login(self, payload:LoginRequest):
        user = self.user_repository.get_by_email(payload.email)
        if user is None or not user.is_active or not verify_pass(payload.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Invalid email or password"
            )
        token = create_access_token(str(user.id), user.role)
        pydantic_user = self._dump_user(user)
        return {
            "msg":"login success",
            "token":token,
            "user":pydantic_user
        }




