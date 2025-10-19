# app/infrastructure/db/models/post_model.py
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Text, ForeignKey, DateTime, Index
from app.infrastructure.db.db_session import Base
from datetime import datetime, timezone

class PostORM(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    # Relación con User
    author: Mapped["UserORM"] = relationship("UserORM", back_populates="posts")

    # Índices
    __table_args__ = (
        Index('idx_posts_title', 'title'),
        Index('idx_posts_created_at', 'created_at'),
        Index('idx_posts_user_id_created_at', 'user_id', 'created_at'),
    )

    def __repr__(self) -> str:
        return f"<PostORM(id={self.id}, title='{self.title}')>"
