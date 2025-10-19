# app/schemas/user_schema.py
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import List, Optional
from app.schemas.post_schema_basic import PostResponseBasic
from app.schemas.user_schema_basic import UserResponseBasic

class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    password: Optional[str] = Field(None, min_length=6)


class UserResponse(UserResponseBasic):
    created_at: datetime
    updated_at: datetime
    posts: List[PostResponseBasic] = []

    class Config:
        from_attributes = True
