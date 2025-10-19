# app/infrastructure/repositories/post_repository_impl.py
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload

from app.infrastructure.db.models.post_model import PostORM
from app.schemas.post_schema import PostCreate, PostUpdate, PostResponse

class PostRepositoryImpl:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, post_data: PostCreate) -> PostResponse:
        new_post = PostORM(
            title=post_data.title,
            content=post_data.content,
            user_id=post_data.user_id,
        )
        self.session.add(new_post)
        await self.session.flush()
        await self.session.commit()
        await self.session.refresh(new_post)
        # Recarga el post con la relación author
        stmt = select(PostORM).options(selectinload(PostORM.author)).where(PostORM.id == new_post.id)
        result = await self.session.execute(stmt)
        post_with_author = result.scalar_one()
        return PostResponse.model_validate(post_with_author)

    async def get_by_id(self, post_id: int) -> Optional[PostResponse]:
        stmt = (
            select(PostORM)
            .where(PostORM.id == post_id)
            .options(selectinload(PostORM.author))
        )
        result = await self.session.execute(stmt)
        post = result.scalar_one_or_none()
        return PostResponse.model_validate(post) if post else None

    async def list_posts(self) -> List[PostResponse]:
        stmt = select(PostORM).options(selectinload(PostORM.author))
        result = await self.session.execute(stmt)
        posts = result.scalars().all()
        return [PostResponse.model_validate(post) for post in posts]

    async def update(self, post_id: int, post_data: PostUpdate) -> Optional[PostResponse]:
        stmt = (
            update(PostORM)
            .where(PostORM.id == post_id)
            .values(**post_data.model_dump(exclude_unset=True))
        )
        await self.session.execute(stmt)
        await self.session.commit()
        return await self.get_by_id(post_id)

    async def delete(self, post_id: int) -> bool:
        result = await self.session.execute(delete(PostORM).where(PostORM.id == post_id))
        await self.session.commit()
        return result.rowcount > 0
