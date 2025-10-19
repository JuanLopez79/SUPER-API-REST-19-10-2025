# app/application/services/user_service.py
from typing import List, Optional
from uuid import UUID
import logging

from app.domain.models.user import User as DomainUser
from app.schemas.user_schema import UserCreate, UserUpdate, UserResponse
from app.interfaces.repositories.user_repository import IUserRepository
from app.core.security import hash_password, verify_password

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, repository: IUserRepository):
        self.repository = repository

    # ==========================================================
    # 🔹 Crear usuario
    # ==========================================================
    async def create_user(self, user_data: UserCreate) -> UserResponse:
        try:
            hashed_pw = hash_password(user_data.password)
            user_data_hashed = UserCreate(
                email=user_data.email,
                username=user_data.username,
                password=hashed_pw,
            )
            created_user = await self.repository.create(user_data_hashed)
            return created_user  # Ya es UserResponse
        except ValueError as e:
            logger.warning(f"Error al crear usuario: {e}")
            raise

    # ==========================================================
    # 🔹 Obtener usuario por ID
    # ==========================================================
    async def get_user_by_id(self, user_id: int) -> Optional[UserResponse]:
        user = await self.repository.get_by_id(user_id)
        return user  # Ya es UserResponse o None

    # ==========================================================
    # 🔹 Listar todos los usuarios
    # ==========================================================
    async def list_all_users(self) -> List[UserResponse]:
        users = await self.repository.list_all()
        return users  # Ya es List[UserResponse]

    # ==========================================================
    # 🔹 Actualizar usuario
    # ==========================================================
    async def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[UserResponse]:
        updated_user = await self.repository.update(user_id, user_data)
        return updated_user  # Ya es UserResponse o None

    # ==========================================================
    # 🔹 Eliminar usuario
    # ==========================================================
    async def delete_user(self, user_id: int) -> bool:
        return await self.repository.delete(user_id)
