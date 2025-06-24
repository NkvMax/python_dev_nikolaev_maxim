# Точка входа в приложение. Запуск FastAPI
# Создаем объект FastAPI(), подключаем роуты, поднимаем сервер uvicorn

from fastapi import FastAPI
from app.controllers import comments_controller, general_controller


def create_app() -> FastAPI:
    app = FastAPI(
        title="Аналитический сервис для агрегации пользовательской активности",
        version="1.0.0",
        description="MySQL (PyMySQL) подключение к db1 и db2"
    )

    # Подключаем routes
    app.include_router(comments_controller.router, prefix="/api/comments", tags=["comments"])
    app.include_router(general_controller.router, prefix="/api/general", tags=["general"])

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
