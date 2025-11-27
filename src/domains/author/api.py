import uuid
from typing import List

from fastapi import APIRouter, Depends, Path, Query, status

from src.domains.author.schema import (
    AuthorCreateSchema,
    AuthorMappers,
    AuthorResponseSchema,
)
from src.domains.author.services import AuthorService, get_author_service

router = APIRouter()


@router.get(
    "/",
    response_model=List[AuthorResponseSchema],
    summary="Получить список авторов",
)
async def get_all(
    skip: int = Query(0, description="Смещение относительно первого элемента в списке"),
    limit: int = Query(100, description="Сколько элементов загружать в список"),
    with_genre: bool = Query(False, description="Загружать ли жанры"),
    service: AuthorService = Depends(get_author_service),
):
    authors = await service.get_all(skip=skip, limit=limit, with_genre=with_genre)
    return AuthorMappers.entity_to_response_list(authors)


@router.get(
    "/{id}",
    response_model=AuthorResponseSchema,
    summary="Получить автора по id",
)
async def get_by_id(
    id: uuid.UUID = Path(..., description="ID автора"),
    with_genre: bool = Query(False, description="Загружать ли жанры"),
    service: AuthorService = Depends(get_author_service),
):
    author = await service.get_by_id(author_id=id, with_genre=with_genre)
    return AuthorMappers.entity_to_response(author)


@router.post(
    "/",
    response_model=AuthorResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Создать автора",
)
async def create(
    author_data: AuthorCreateSchema,
    service: AuthorService = Depends(get_author_service),
):
    author = AuthorMappers.dto_to_entity_create(author_data)
    created_author = await service.create(author)
    return AuthorMappers.entity_to_response(created_author)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить автора по id",
)
async def delete(
    id: uuid.UUID = Path(..., description="ID автора"),
    service: AuthorService = Depends(get_author_service),
):
    return await service.delete(id)
