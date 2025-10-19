# app/schemas/post_schema_basic.py
from pydantic import BaseModel

class PostResponseBasic(BaseModel):
    id: int
    title: str

    class Config:
        from_attributes = True
