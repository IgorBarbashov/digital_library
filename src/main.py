# src/main.py
import uvicorn
from fastapi import FastAPI

#  импортируем список роутеров
from src.api.routers import routers


def create_app() -> FastAPI:
    """
    Создаёт приложение FastAPI.
    Подключает все роутеры из списка (пункт 3).
    """
    app = FastAPI(
        title="Электронная библиотека",
        description="Бэкенд для поиска и чтения книг",
        version="0.0.1"
    )

    #  подключаем каждый роутер
    for router in routers:
        app.include_router(router)

    return app


# Создаём приложение
app = create_app()


#  запуск через uvicorn
if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )