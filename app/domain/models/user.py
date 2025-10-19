# app/domain/models/user.py
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4


@dataclass
class User:
    id: UUID = field(default_factory=uuid4)
    email: str = field(default="")
    username: str = field(default="")
    hashed_password: str = field(default="")

    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    # Relación con posts (One To Many)
    posts: List["Post"] = field(default_factory=list)

    def add_post(self, post: "Post") -> None:
        """Asociar un nuevo post al usuario"""
        self.posts.append(post)
        self.updated_at = datetime.utcnow()

    def __repr__(self) -> str:
        return f"<User(username='{self.username}', email='{self.email}')>"
