# app/infrastructure/db/models/__init__.py

# Permite importar fácilmente todos los modelos en Alembic.

from .user_model import UserORM
from .post_model import PostORM

__all__ = ["UserORM", "PostORM"]
