"""
Единый Settings-класс, совместимый c Pydantic 1.x и 2.x
без дополнительных зависимостей.
"""

# пытаемся сначала импортировать "старую" реализацию из подпакета v1
try:
    from pydantic.v1 import BaseSettings, Field  # Pydantic ≥ 2.0
except (ImportError, ModuleNotFoundError):
    from pydantic import BaseSettings, Field  # Pydantic 1.x


# модель
class Settings(BaseSettings):
    db1_url: str = Field(..., env="DATABASE_URL1")
    db2_url: str = Field(..., env="DATABASE_URL2")

    class Config:  # работает и в v1, и в v2
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
