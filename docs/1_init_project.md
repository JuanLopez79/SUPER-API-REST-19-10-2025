# ARRANQUE DEL PROYECTO

## 1. Estructura de archivos y carpetas

```bash

project/
│── alembic/
│   ├── versions/
│   ├── env.py
│   ├── README
│   └── script.py.mako
│── app/
│   ├── api/ 
│   │   ├── v1/
│   │   │   ├── dependencies/
│   │   │   │   └── common.py
│   │   │   └── endpoints/
│   │   │       ├── post_router.py
│   │   │       └── user_router.py    
│   │   └── __init__.py           
│   ├── core/  
│   │   ├── config.py
│   │   ├── exceptions.py
│   │   ├── logging_config.py  
│   │   └── security.py
│   ├── domain/
│   │   └── models/
│   │       ├── post.py 
│   │       └── user.py
│   ├── infrastructure/
│   │   ├── db/
│   │   │   ├── models/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── post_model.py
│   │   │   │   └── user_model.py
│   │   │   ├── repositories/
│   │   │   │   ├── post_repository_impl.py
│   │   │   │   └── user_repository_impl.py
│   │   │   └── db_session.py 
│   │   └── services/
│   │       ├── cache_service.py      # OPCIONAL futuro
│   │       └── email_service.py      # OPCIONAL futuro
│   ├── interfaces/
│   │   └── repositories/
│   │       ├── post_repository.py
│   │       └── user_repository.py
│   ├── schemas/
│   │   ├── post_schema_basic.py
│   │   ├── post_schema.py
│   │   ├── user_schema_basic.py
│   │   └── user_schema.py     
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── test_posts.py
│   │   └── test_users.py
│   ├── use_cases/   
│   │   ├── post_service.py
│   │   └── user_service.py
│   └── main.py
│── docs/
│   ├── 1_init_project.md
│   ├── 2_alembic.md
│   ├── 3_backend.md
│── venv/
│── .env
│── .env.example
│── .gitignore
│── alembic.ini
│── docker-compose.override.yml
│── docker-compose.prod.yml       # produccion
│── docker-compose.yml       # desarrollo (se carga por defecto)
│── Dockerfile
│── README.md
└── requirements.txt

```

## 2. Enlistar las librerias necesarias en **requirements.txt**

```bash

fastapi[all]
sqlalchemy[asyncio]
asyncpg
uvicorn
alembic
pydantic
python-jose[cryptography]
passlib[bcrypt]
email-validator
python-dotenv
bcrypt==3.2.0
passlib==1.7.4

# # requirements.txt
# fastapi==0.115.0
# uvicorn[standard]==0.30.1
# sqlalchemy[asyncio]==2.0.30
# asyncpg==0.29.0
# alembic==1.13.2
# python-dotenv==1.0.1
# pydantic==2.7.4
# pydantic-settings==2.2.1
# passlib[bcrypt]==1.7.4
# python-jose[cryptography]==3.3.0

```

## 3. Crear entorno virtual e instalar dependencias

```bash

python -m venv venv

```

---

```bash

.\venv\Scripts\activate

```

---

```bash

pip install -r requirements.txt

```

## 4. Crear archivo .gitignore

```python

# ==================================================
# ENTORNOS VIRTUALES
# ==================================================
venv/
ve/
.env
# .env.*
__pypackages__/

# ==================================================
# PYTHON: compilados, caché y metadatos
# ==================================================
__pycache__/
*.py[cod]
*$py.class
*.pyo
*.pyd
*.pyt
*.pyz
*.pyc
*.pdb

# ==================================================
# TESTING, COBERTURA Y TIPO
# ==================================================
.pytest_cache/
.coverage
.tox/
.nox/
mypy_cache/
htmlcov/
*.cover
*.log
nosetests.xml
coverage.xml
*.prof
.prof
*.tmp

# ==================================================
# DOCS
# ==================================================
_site/
_build/
docs/_build/
docs/site/
*.pdf
*.html

# ==================================================
# DOCKER & BASES DE DATOS
# ==================================================
docker-compose.override.yml
*.env.docker
pg_data/
*.sqlite3
*.db
*.sql
*.bak
*.dump
*.tar
*.tar.gz
*.zip

# ==================================================
# IDEs Y EDITORES
# ==================================================
.vscode/
.idea/
*.sublime-project
*.sublime-workspace
*.code-workspace
*.sw?

# ==================================================
# SISTEMA OPERATIVO
# ==================================================
.DS_Store
Thumbs.db
desktop.ini
.Trashes
*.stackdump
ehthumbs.db

# ==================================================
# ARCHIVOS TEMPORALES / BACKUPS
# ==================================================
*.tmp
*.temp
*.bak
*.orig
*.old
*.save
*.swp
*.swo
*.~*

# ==================================================
# DISTRIBUCIÓN / BUILD / PACKAGE
# ==================================================
build/
dist/
*.egg-info/
*.egg
.eggs/
pip-wheel-metadata/
__pypackages__/
*.whl

# ==================================================
# ARCHIVOS DE CONFIGURACIÓN LOCAL
# ==================================================
*.local
*.cfg
*.config
.settings/

# ==================================================
# LOGS GENERALES
# ==================================================
*.log
*.out
*.err
*.traceback

# ==================================================
# OTROS ARCHIVOS TEMPORALES
# ==================================================
*.lock
*.pid
*.seed
*.coveragerc
*.pot
*.mo

```

## 5. Dockerizar proyecto creando en la jerarquia mas alta del proyecto. Crear **Dockerfile** y **docker_compose.yml**.

1️⃣ **Dockerfile** (único para desarrollo y producción):

```dockerfile

# Dockerfile

FROM python:3.12-slim

# Establece directorio de trabajo
WORKDIR /app

# Instala dependencias del sistema necesarias para compilar algunas librerías y PostgreSQL
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# Copia primero el archivo de requirements para usar cache de Docker
COPY requirements.txt .

# Instala dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el proyecto
COPY . .

# Expone puerto
EXPOSE 8000

# Comando por defecto (puede ser sobreescrito en docker-compose)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

```

---

2️⃣ **docker-compose.yml** (base):

```yaml

# docker-compose.yml

services: 
  db:
    image: postgres:15
    container_name: project_postgres
    restart: unless-stopped
    environment:
      POSTGRES_USER: ${POSTGRES_USER:-user}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-password}
      POSTGRES_DB: ${POSTGRES_DB:-project_db}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-user} -d ${POSTGRES_DB:-project_db}"]
      interval: 10s
      timeout: 5s
      retries: 5

  api:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: project_backend
    env_file: 
      - .env
    depends_on:
      db:
        condition: service_healthy

volumes:
  postgres_data:

```

---

3️⃣ **docker-compose.override.yml** (desarrollo, hot-reload):

```yaml

# docker-compose.override.yml

services:
  db:
    ports:
      - "5432:5432"

  api:
    ports:
      - "8000:8000"
    volumes:
      - .:/app
      - /app/__pycache__/
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

```

✅ Esto permite:

- Hot-reload cuando cambias código.

- Montaje del código local en el contenedor.

---

4️⃣ **docker-compose.prod.yml** (producción):

```yaml

# docker-compose.prod.yml

services:
  db:
    ports:
      - "5432:5432" # Solo si necesitas acceso remoto
    restart: always

  api:
    ports:
      - "8000:8000"
    restart: always
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

```

✅ Esto permite:

- Modo estable para producción.

- 4 workers para manejar más solicitudes.

- No hay hot-reload ni volúmenes locales.

---

## 6. Crear archivo **.env** y **.env.example** en la jerarquia mas alta del proyecto.

```bash

# .env.example

# --- PostgreSQL ---
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=your_database
POSTGRES_HOST=db
POSTGRES_PORT=5432
DATABASE_URL="postgresql+asyncpg://user:password@db:5432/project_db"

# --- App Config ---
APP_NAME=ProjectAPI
APP_ENV=development
APP_DEBUG=True # MODO DESARROLLO / FALSE PARA PRODUCCION
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

```

## 7. Inicializar backend.

1. En **app/main.py**:

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

    # Routers (Mas adelante se crearan)
    # app.include_router(user_router.router, prefix="/users", tags=["Users"])
    # app.include_router(post_router.router, prefix="/posts", tags=["Posts"])
    # Si en un futuro agregamos auth_router:
    # from app.api.v1.endpoints import auth_router
    # app.include_router(auth_router.router, prefix="/auth", tags=["Auth"])

    return app

app = create_app()

```

---

2. En **app/core/config.py**:

```python

# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    # Configuración general de la app
    APP_NAME: str = "ProjectAPI"
    APP_ENV: str = "development"  # Puede ser 'development', 'production', 'testing'
    DEBUG: bool = True

    # Configuración de base de datos
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    DATABASE_URL: str  # Puedes construirla dinámicamente si quieres

    # Configuración de JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    # Ajuste automático de DEBUG según APP_ENV
    @property
    def is_debug(self) -> bool:
        return self.APP_ENV.lower() != "production"

@lru_cache
def get_settings() -> Settings:
    return Settings()

```

---

3. En **app/core/logging_config.py**:

```python

# app/core/logging_config.py
import logging

# Nivel de logging
LOG_LEVEL = logging.INFO

# Formato
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

def setup_logging():
    logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)

```

## 8. Correr proyecto.

### DESARROLLO

```bash

docker compose up --build

```

- Hot-reload activo.

- Puertos: 8000 para FastAPI, 5432 para Postgres.

- Cambios en tu código se reflejan automáticamente.

### PRODUCCION

```bash

docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d

```

- Corre en segundo plano.

- 4 workers.

- Sin hot-reload.

- Contenedor estable para servidor real.