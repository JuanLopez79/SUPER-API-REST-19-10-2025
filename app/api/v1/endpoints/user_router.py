# app/api/v1/endpoints/user_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from app.use_cases.user_service import UserService
from app.api.v1.dependencies.common import get_user_service
from app.schemas.user_schema import UserCreate, UserUpdate, UserResponse

router = APIRouter()

# ==========================================================
# 🔹 Crear usuario
# ==========================================================
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    service = Depends(get_user_service)  # Elimina ": UserService"
):
    try:
        user = await service.create_user(user_data)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# ==========================================================
# 🔹 Obtener usuario por ID
# ==========================================================
@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(user_id: int, service = Depends(get_user_service)):
    user = await service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return user

# ==========================================================
# 🔹 Listar todos los usuarios
# ==========================================================
@router.get("/", response_model=List[UserResponse])
async def list_all_users(service = Depends(get_user_service)):
    users = await service.list_all_users()
    return users

# ==========================================================
# 🔹 Actualizar usuario
# ==========================================================
@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_data: UserUpdate, service = Depends(get_user_service)):
    user = await service.update_user(user_id, user_data)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return user

# ==========================================================
# 🔹 Eliminar usuario
# ==========================================================
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, service = Depends(get_user_service)):
    deleted = await service.delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

