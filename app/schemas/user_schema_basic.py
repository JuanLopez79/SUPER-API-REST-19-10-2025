# app/schemas/user_schema_basic.py
from pydantic import BaseModel, EmailStr

class UserResponseBasic(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True  # Permite mapear desde SQLAlchemy ORM
