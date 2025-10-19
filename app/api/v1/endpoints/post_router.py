# app/api/v1/endpoints/post_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from app.api.v1.dependencies.common import get_post_service as PostService
from app.api.v1.dependencies.common import get_post_service
from app.schemas.post_schema import PostCreate, PostUpdate, PostResponse

router = APIRouter()

# ==========================================================
# 🔹 Crear post
# ==========================================================
@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(post_data: PostCreate, service = Depends(get_post_service)):
    try:
        post = await service.create_post(post_data)
        return post
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# ==========================================================
# 🔹 Obtener post por ID
# ==========================================================
@router.get("/{post_id}", response_model=PostResponse)
async def get_post_by_id(post_id: int, service = Depends(get_post_service)):
    post = await service.get_post(post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post no encontrado")
    return post

# ==========================================================
# 🔹 Listar todos los posts
# ==========================================================
@router.get("/", response_model=List[PostResponse])
async def list_all_posts(service = Depends(get_post_service)):
    posts = await service.list_posts()  # <-- usa el nombre correcto
    return posts

# ==========================================================
# 🔹 Actualizar post
# ==========================================================
@router.put("/{post_id}", response_model=PostResponse)
async def update_post(post_id: int, post_data: PostUpdate, service = Depends(get_post_service)):
    post = await service.update_post(post_id, post_data)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post no encontrado")
    return post

# ==========================================================
# 🔹 Eliminar post
# ==========================================================
@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, service = Depends(get_post_service)):
    deleted = await service.delete_post(post_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post no encontrado")
