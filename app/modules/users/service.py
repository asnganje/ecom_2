from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.core.security import hash_pass
from app.database.session import settings
from app.modules.users.model import User
from app.modules.users.repository import UserRepository
from app.modules.users.schema import UserRead, UserUpdate, UserRole


class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)
    def _dump_user(self, user:User)->UserRead:
        return UserRead.model_validate(user)
    def list_users(self)->list[UserRead]:
        users = self.repository.get_all()
        result = [self._dump_user(user) for user in users]
        return result
    def get_user(self, user_id:int)->UserRead:
        user = self.repository.get_by_id(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return self._dump_user(user)
    def get_current_user(self, user:User)->UserRead:
        return self._dump_user(user)

    def update_user(self, user_id:int, payload:UserUpdate)->UserRead:
        user = self.repository.get_by_id(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        changes = payload.model_dump(exclude_unset=True)

        if "fullname" in changes:
            user.fullname = changes["fullname"]

        db_user = self.repository.update_user(user)
        return self._dump_user(db_user)

    def delete_user(self, user_id:int):
        user = self.repository.get_by_id(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        self.repository.delete_user(user)

    def ensure_admin_user(self)->None:
        admin_email = settings.admin_email
        admin_password = settings.admin_password

        existing_admin = self.repository.get_by_email(admin_email)
        if existing_admin is not None:
            return
        admin_user = User(
            fullname="Nganje Auf",
            email=admin_email,
            password_hash=hash_pass(admin_password),
            role=UserRole.ADMIN.value
        )

        self.repository.create_user(admin_user)


