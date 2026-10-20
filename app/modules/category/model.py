from sqlalchemy import Integer, String, ForeignKey, DateTime, func, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.database.session import Base


class Category(Base):
    __tablename__ = "categories"
    id:Mapped[int]=mapped_column(Integer, primary_key=True)
    name:Mapped[str]=mapped_column(String(100), nullable=False, unique=True)
    parent_id:Mapped[int|None] = mapped_column(ForeignKey("categories.id"), nullable=True, default=None)
    is_active:Mapped[bool]=mapped_column(Boolean, default=True, nullable=False)
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )