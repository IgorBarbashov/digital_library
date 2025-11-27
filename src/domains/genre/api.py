from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db import get_async_session
from src.domains.genre.models import Genre
from src.domains.genre.schema import GenreReadSchema

router = APIRouter()


@router.get(
    "/",
    response_model=List[GenreReadSchema],
    summary="Получить список жанров",
)
async def get_all(
    session: AsyncSession = Depends(get_async_session),
) -> List[GenreReadSchema]:
    stmt = select(Genre).order_by(Genre.create_at.asc())
    result = await session.execute(stmt)
    genres = result.scalars().all()

    return [GenreReadSchema.model_validate(genre) for genre in genres]
