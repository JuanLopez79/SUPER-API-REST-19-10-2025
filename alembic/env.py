from logging.config import fileConfig
import asyncio
import sys
import os
from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine

# --- Ajustar la ruta del proyecto ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importa la Base declarativa
from app.infrastructure.db.db_session import Base
from app.core.config import get_settings
from dotenv import load_dotenv
from app.infrastructure.db.models.post_model import PostORM
from app.infrastructure.db.models.user_model import UserORM

# Configuración de Alembic
config = context.config

# Configuración de logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Cargar variables de entorno y settings
load_dotenv()
settings = get_settings()

# URL de la base de datos (asegúrate que sea asyncpg)
# Ejemplo: postgresql+asyncpg://user:password@localhost:5432/mydb
config.set_main_option("sqlalchemy.url",
settings.DATABASE_URL)

# Metadata para autogenerar migraciones
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Ejecuta migraciones en modo offline (sin
    conexión a DB)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection):
    """Ejecuta las migraciones usando la conexión
    proporcionada."""
    context.configure(connection=connection,
        target_metadata=target_metadata)
    
    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online() -> None:
    """Ejecuta migraciones en modo online usando
    AsyncEngine."""
    connectable = create_async_engine(
        config.get_main_option("sqlalchemy.url"),
        poolclass=pool.NullPool,
    )
    
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
        await connectable.dispose()

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())