# CONSTRUCCION DEL BACKEND.

---

## 1. Preparando ORM (SQLAlchemy).

---

### 1.1 **app/infrastructure/db/db_session.py**:

Creamos motor de la base de datos.

```python

# app/infrastructure/db/db_session.py
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from app.core.config import get_settings

settings = get_settings()

# Engine Async
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=3600,
)

# Base declarativa
class Base(DeclarativeBase):
    pass

# Sessionmaker Async
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

async def dispose_db():
    """Cierra el engine de SQLAlchemy al apagar la aplicación"""
    await engine.dispose()

```

---

### 1.2 **app/infrastructure/db/models/post_model.py**:

```python

# app/infrastructure/db/models/post_model.py
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Text, ForeignKey, DateTime, Index
from app.infrastructure.db.db_session import Base
from datetime import datetime, timezone

class PostORM(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    # Relación con User
    author: Mapped["UserORM"] = relationship("UserORM", back_populates="posts")

    # Índices
    __table_args__ = (
        Index('idx_posts_title', 'title'),
        Index('idx_posts_created_at', 'created_at'),
        Index('idx_posts_user_id_created_at', 'user_id', 'created_at'),
    )

    def __repr__(self) -> str:
        return f"<PostORM(id={self.id}, title='{self.title}')>"

```

### 1.2 **app/infrastructure/db/models/user_model.py**:

```python

# app/infrastructure/db/models/user_model.py
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean, DateTime, Index
from app.infrastructure.db.db_session import Base
from datetime import datetime, timezone

class UserORM(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    # Relación One-to-Many con Post
    posts: Mapped[list["PostORM"]] = relationship(
        "PostORM",
        back_populates="author",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    # Índices
    __table_args__ = (
        Index('idx_users_username', 'username'),
        Index('idx_users_created_at', 'created_at'),
        Index('idx_users_created_username', 'created_at', 'username'),
    )

    def __repr__(self) -> str:
        return f"<UserORM(id={self.id}, username='{self.username}')>"

```

### 1.2 **app/infrastructure/db/models/__init__.py**:

```python

# app/infrastructure/db/models/__init__.py

# Permite importar fácilmente todos los modelos en Alembic.

from .user_model import UserORM
from .post_model import PostORM

__all__ = ["UserORM", "PostORM"]

```

---

## 2. Modelos de Dominio

### 2.1 **app/domain/models/post.py**

```python

# app/domain/models/post.py
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional


@dataclass
class Post:
    id: UUID = field(default_factory=uuid4)
    title: str = field(default="")
    content: str = field(default="")
    
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    # Relación con User
    author_id: Optional[UUID] = None

    def update_content(self, new_content: str) -> None:
        """Actualizar contenido del post"""
        self.content = new_content
        self.updated_at = datetime.utcnow()

    def __repr__(self) -> str:
        return f"<Post(title='{self.title}', author_id='{self.author_id}')>"

```

### 2.2 **app/domain/models/user.py**

```python

# app/domain/models/user.py
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4


@dataclass
class User:
    id: UUID = field(default_factory=uuid4)
    email: str = field(default="")
    username: str = field(default="")
    hashed_password: str = field(default="")

    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    # Relación con posts (One To Many)
    posts: List["Post"] = field(default_factory=list)

    def add_post(self, post: "Post") -> None:
        """Asociar un nuevo post al usuario"""
        self.posts.append(post)
        self.updated_at = datetime.utcnow()

    def __repr__(self) -> str:
        return f"<User(username='{self.username}', email='{self.email}')>"

```

---

## 3. Esquemas de validacion Pydantic

### 3.1 **app/schemas/post_schema_basic.py**

```python

# app/schemas/post_schema_basic.py
from pydantic import BaseModel

class PostResponseBasic(BaseModel):
    id: int
    title: str

    class Config:
        from_attributes = True

```

### 3.2 **app/schemas/post_schema.py**

```python

# app/schemas/post_schema.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.schemas.user_schema_basic import UserResponseBasic
from app.schemas.post_schema_basic import PostResponseBasic

class PostCreate(BaseModel):
    title: str
    content: str
    user_id: int  


class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    content: Optional[str] = None


class PostResponse(PostResponseBasic):
    content: str
    created_at: datetime
    updated_at: datetime
    author: Optional[UserResponseBasic] = None

    class Config:
        from_attributes = True

```

### 3.3 **app/schemas/user_schema_basic.py**

```python

# app/schemas/user_schema_basic.py
from pydantic import BaseModel, EmailStr

class UserResponseBasic(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True  # Permite mapear desde SQLAlchemy ORM

```

### 3.4 **app/schemas/user_schema.py**

```python

# app/schemas/user_schema.py
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import List, Optional
from app.schemas.post_schema_basic import PostResponseBasic
from app.schemas.user_schema_basic import UserResponseBasic

class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    password: Optional[str] = Field(None, min_length=6)


class UserResponse(UserResponseBasic):
    created_at: datetime
    updated_at: datetime
    posts: List[PostResponseBasic] = []

    class Config:
        from_attributes = True

```

---

## 4. Contratos

### 4.1 **app/interfaces/repositories/post_repository.py**

```python

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

```

### 4.1 **app/interfaces/repositories/user_repository.py**

```python

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

```

---

## 5. Repositorios

## 5.1 **app/core/security.py**

```python

# app/core/security.py
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

```

### 5.2 **app/infrastructure/db/repositories/post_repository_impl.py**:

```python

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

```

### 5.3 **app/infrastructure/db/repositories/user_repository_impl.py**:

```python

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

```

---

## 6. Servicios y Dependencias

### 6.1 **app/use_cases/post_service.py**:

```python

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

```

### 6.2 **app/use_cases/user_service.py**:

```python

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

```

### 6.3 **app/api/v1/dependencies/common.py**:

```python

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
        
```

---

## 7. Routers

### 7.1 **app/api/v1/endpoints/post_router.py**

```python

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

```

### 7.2 **app/api/v1/endpoints/user_router.py**

```python

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

```

### 7.3 app/main.py

```python

# app/main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.config import get_settings
import logging
from app.core.logging_config import setup_logging

from app.api.v1.endpoints import user_router, post_router  # Routers
from app.infrastructure.db.db_session import dispose_db     # Cierre DB

# Inicializar logging global
setup_logging()
logger = logging.getLogger(__name__)

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan de la aplicación: inicio y cierre de recursos.
    """
    logger.info("🚀 Aplicación iniciando...")
    yield
    logger.info("🛑 Aplicación cerrándose...")
    # Cerrar el engine de SQLAlchemy Async
    await dispose_db()

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        debug=settings.is_debug,
        lifespan=lifespan
    )

    # Routers
    app.include_router(user_router.router, prefix="/users", tags=["Users"])
    app.include_router(post_router.router, prefix="/posts", tags=["Posts"])
    # Si en un futuro agregamos auth_router:
    # from app.api.v1.endpoints import auth_router
    # app.include_router(auth_router.router, prefix="/auth", tags=["Auth"])

    return app

app = create_app()

```