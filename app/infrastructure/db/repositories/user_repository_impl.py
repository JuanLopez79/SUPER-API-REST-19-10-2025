# app/infrastructure/repositories/user_repository_impl.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
from typing import Optional, List

from app.infrastructure.db.models.user_model import UserORM
from app.schemas.user_schema import UserCreate, UserUpdate, UserResponse
from app.core.security import hash_password

class UserRepositoryImpl:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_data: UserCreate) -> UserResponse:
        new_user = UserORM(
            email=user_data.email,
            username=user_data.username,
            hashed_password=user_data.password,
        )
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        # Carga posts de forma eager
        stmt = select(UserORM).options(selectinload(UserORM.posts)).where(UserORM.id == new_user.id)
        result = await self.session.execute(stmt)
        user_with_posts = result.scalar_one()
        return UserResponse.model_validate(user_with_posts)

    async def get_by_id(self, user_id: int) -> Optional[UserResponse]:
        stmt = select(UserORM).options(selectinload(UserORM.posts)).where(UserORM.id == user_id)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        if user:
            return UserResponse.model_validate(user)
        return None

    async def get_by_username(self, username: str) -> Optional[UserResponse]:
        stmt = select(UserORM).where(UserORM.username == username)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        return UserResponse.model_validate(user) if user else None

    async def list_all(self) -> List[UserResponse]:
        stmt = select(UserORM).options(selectinload(UserORM.posts))
        result = await self.session.execute(stmt)
        users = result.scalars().all()
        return [UserResponse.model_validate(user) for user in users]

    async def update(self, user_id: int, user_data: UserUpdate) -> Optional[UserResponse]:
        update_data = user_data.dict(exclude_unset=True)
        if "password" in update_data:
            # Hashea el password y cambia la clave
            update_data["hashed_password"] = hash_password(update_data.pop("password"))
        stmt = (
            update(UserORM)
            .where(UserORM.id == user_id)
            .values(**update_data)
            .execution_options(synchronize_session="fetch")
        )
        await self.session.execute(stmt)
        await self.session.commit()
        # Devuelve el usuario actualizado
        return await self.get_by_id(user_id)

    async def delete(self, user_id: int) -> bool:
        result = await self.session.execute(delete(UserORM).where(UserORM.id == user_id))
        await self.session.commit()
        return result.rowcount > 0
