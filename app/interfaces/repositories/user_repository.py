# app/interfaces/repositories/user_repository.py
from typing import Protocol, List, Optional
from uuid import UUID
from app.domain.models.user import User as DomainUser


class IUserRepository(Protocol):
    async def create(self, user: DomainUser) -> DomainUser:
        ...

    async def get_by_id(self, user_id: int) -> Optional[DomainUser]:
        ...

    async def get_by_username(self, username: str) -> Optional[DomainUser]:
        ...

    async def list_all(self) -> List[DomainUser]:
        ...

    async def update(self, user_id: int, user_data) -> Optional[DomainUser]:
        ...

    async def delete(self, user_id: int) -> bool:
        ...
