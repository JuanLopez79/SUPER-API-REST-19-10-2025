# app/schemas/post_schema.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.schemas.user_schema_basic import UserResponseBasic
from app.schemas.post_schema_basic import PostResponseBasic

class PostCreate(BaseModel):
    title: str
    content: str
    user_id: int  


class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    content: Optional[str] = None


class PostResponse(PostResponseBasic):
    content: str
    created_at: datetime
    updated_at: datetime
    author: Optional[UserResponseBasic] = None

    class Config:
        from_attributes = True
