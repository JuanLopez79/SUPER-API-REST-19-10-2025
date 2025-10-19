# app/services/post_service.py
from typing import List, Optional
from app.interfaces.repositories.post_repository import IPostRepository
from app.schemas.post_schema import (
    PostCreate, PostUpdate, PostResponse
)

class PostService:
    """Capa de aplicación que maneja la lógica de negocio de Posts."""

    def __init__(self, repository: IPostRepository):
        self.repository = repository

    async def create_post(self, post_data: PostCreate) -> PostResponse:
        if not post_data.title or not post_data.content:
            raise ValueError("El título y contenido no pueden estar vacíos.")
        return await self.repository.create(post_data)

    async def get_post(self, post_id: int) -> Optional[PostResponse]:
        return await self.repository.get_by_id(post_id)

    async def list_posts(self) -> List[PostResponse]:
        return await self.repository.list_posts()

    async def update_post(self, post_id: int, post_data: PostUpdate) -> Optional[PostResponse]:
        return await self.repository.update(post_id, post_data)

    async def delete_post(self, post_id: int) -> bool:
        return await self.repository.delete(post_id)
