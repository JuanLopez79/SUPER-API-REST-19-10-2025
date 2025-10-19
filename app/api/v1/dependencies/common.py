# app/api/v1/dependencies/common.py
from typing import AsyncGenerator
from fastapi import Depends
from app.infrastructure.db.db_session import AsyncSessionLocal, AsyncSession
from app.infrastructure.db.repositories.user_repository_impl import UserRepositoryImpl
from app.infrastructure.db.repositories.post_repository_impl import PostRepositoryImpl
from app.use_cases.user_service import UserService
from app.use_cases.post_service import PostService

# Generador de sesión DB (esto sí puede ser async generator)
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

# Repositorios
def get_user_repository(session: AsyncSession = Depends(get_db_session)) -> UserRepositoryImpl:
    return UserRepositoryImpl(session)

def get_post_repository(session: AsyncSession = Depends(get_db_session)) -> PostRepositoryImpl:
    return PostRepositoryImpl(session)

# Servicios
def get_user_service(user_repo: UserRepositoryImpl = Depends(get_user_repository)) -> UserService:
    return UserService(user_repo)

def get_post_service(post_repo: PostRepositoryImpl = Depends(get_post_repository)) -> PostService:
    return PostService(post_repo)
