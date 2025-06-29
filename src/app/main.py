"""
Точка входа FastAPI-приложение:
   Читаем настройки (.env)
   Создаем движки init_engines()
   Только после этого импортируем контроллеры / use-cases
"""

from fastapi import FastAPI

from app.settings import settings
from app.db.engine import init_engines

# важно вызвать до остальных импортов
init_engines(settings.db1_url, settings.db2_url)

# Теперь можно тащить бизнес-код
from app.controllers import comments_controller, general_controller  # noqa: E402

def create_app() -> FastAPI:
    app = FastAPI(
        title="Analytics Service",
        version="1.0.0",
        description="FastAPI + PostgreSQL + SQLAlchemy",
    )

    app.include_router(comments_controller.router, prefix="/api/comments", tags=["comments"])
    app.include_router(general_controller.router, prefix="/api/general", tags=["general"])
    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
