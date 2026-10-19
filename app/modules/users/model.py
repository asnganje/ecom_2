from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.database.session import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fullname:Mapped[str]=mapped_column(String(100), nullable=False)
    email:Mapped[str]=mapped_column(String(255), unique=True, nullable=False)
    password_hash:Mapped[str]=mapped_column(String(255), nullable=False)
    is_active:Mapped[bool]=mapped_column(Boolean, default=True, nullable=False)
    role:Mapped[str]=mapped_column(String(50), default="customer", nullable=False)
    
