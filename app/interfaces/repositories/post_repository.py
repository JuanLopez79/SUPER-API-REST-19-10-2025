# app/interfaces/repositories/post_repository.py
from typing import Protocol, List, Optional
from uuid import UUID
from app.domain.models.post import Post as DomainPost


class IPostRepository(Protocol):
    async def create(self, post: DomainPost) -> DomainPost:
        ...

    async def get_by_id(self, post_id: UUID) -> Optional[DomainPost]:
        ...

    async def list_all(self) -> List[DomainPost]:
        ...

    async def list_by_user(self, user_id: UUID) -> List[DomainPost]:
        ...

    async def update(self, post: DomainPost) -> Optional[DomainPost]:
        """Actualizar por objeto DomainPost (debe tener id)."""
        ...

    async def delete(self, post_id: UUID) -> bool:
        ...
