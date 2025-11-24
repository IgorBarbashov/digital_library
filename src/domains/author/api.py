import uuid
from typing import List, Union

from fastapi import APIRouter, Depends, Path, Query, status

from src.domains.author.schema import AuthorSchema, AuthorWithGenreSchema
from src.domains.author.services import AuthorService, get_author_service

router = APIRouter()


@router.get(
    "/",
    response_model=Union[List[AuthorSchema], List[AuthorWithGenreSchema]],
    summary="Получить список авторов",
)
async def get_all(
    service: AuthorService = Depends(get_author_service),
    skip: int = Query(0, description="Смещение относительно первого элемента в списке"),
    limit: int = Query(100, description="Сколько элементов загружать в список"),
    with_genre: bool = Query(False, description="Загружать ли жанры"),
):
    return await service.get_all(skip=skip, limit=limit, with_genre=with_genre)


@router.get(
    "/{id}",
    response_model=Union[AuthorSchema, AuthorWithGenreSchema],
    summary="Получить автора по id",
)
async def get_by_id(
    service: AuthorService = Depends(get_author_service),
    id: uuid.UUID = Path(..., description="ID автора"),
    with_genre: bool = Query(False, description="Загружать ли жанры"),
):
    return await service.get_by_id(author_id=id, with_genre=with_genre)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить автора по id",
)
async def delete(
    service: AuthorService = Depends(get_author_service),
    id: uuid.UUID = Path(..., description="ID автора"),
):
    return await service.delete(id)
