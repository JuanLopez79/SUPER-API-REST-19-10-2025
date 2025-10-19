# app/domain/models/post.py
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional


@dataclass
class Post:
    id: UUID = field(default_factory=uuid4)
    title: str = field(default="")
    content: str = field(default="")
    
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    # Relación con User
    author_id: Optional[UUID] = None

    def update_content(self, new_content: str) -> None:
        """Actualizar contenido del post"""
        self.content = new_content
        self.updated_at = datetime.utcnow()

    def __repr__(self) -> str:
        return f"<Post(title='{self.title}', author_id='{self.author_id}')>"
