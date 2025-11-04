# src/api/test_router.py
# ТЕСТОВЫЙ РОУТЕР
from fastapi import APIRouter, Depends
from src.api.dependencies import get_uow
from src.utils.unitofwork import DefaultUnitOfWork
from src.api.routers import routers

router = APIRouter(prefix="/test", tags=["test"])


@router.get("/db")
async def test_db(uow: DefaultUnitOfWork = Depends(get_uow)):
    result = await uow.session.execute("SELECT 1")
    return {"db_check": result.scalar()}


# Добавляем в список
routers.append(router)