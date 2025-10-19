# app/infrastructure/db/models/user_model.py
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean, DateTime, Index
from app.infrastructure.db.db_session import Base
from datetime import datetime, timezone

class UserORM(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    # Relación One-to-Many con Post
    posts: Mapped[list["PostORM"]] = relationship(
        "PostORM",
        back_populates="author",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    # Índices
    __table_args__ = (
        Index('idx_users_username', 'username'),
        Index('idx_users_created_at', 'created_at'),
        Index('idx_users_created_username', 'created_at', 'username'),
    )

    def __repr__(self) -> str:
        return f"<UserORM(id={self.id}, username='{self.username}')>"
