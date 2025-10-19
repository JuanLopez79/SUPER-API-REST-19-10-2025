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
