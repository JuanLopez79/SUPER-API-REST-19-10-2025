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
