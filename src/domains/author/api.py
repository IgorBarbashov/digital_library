import uuid
from typing import List

from fastapi import APIRouter, Depends, Path, Query, status

from src.domains.author.schema import (
    AuthorCreateSchema,
    AuthorMappers,
    AuthorResponseSchema,
    AuthorUpdateSchema,
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
    "/{author_id}",
    response_model=AuthorResponseSchema,
    summary="Получить автора по id",
)
async def get_by_id(
    author_id: uuid.UUID = Path(..., description="ID автора"),
    with_genre: bool = Query(False, description="Загружать ли жанры"),
    service: AuthorService = Depends(get_author_service),
):
    author = await service.get_by_id(author_id=author_id, with_genre=with_genre)
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
    author = AuthorMappers.create_dto_to_entity(author_data)
    created_author = await service.create(author)
    return AuthorMappers.entity_to_response(created_author)


@router.put(
    "/{author_id}",
    response_model=AuthorResponseSchema,
    summary="Обновить автора",
)
async def update(
    author_data: AuthorUpdateSchema,
    author_id: uuid.UUID = Path(..., description="ID автора"),
    service: AuthorService = Depends(get_author_service),
):
    updated_author = await service.update(
        author_id, author_data.model_dump(exclude_unset=True)
    )
    return AuthorMappers.entity_to_response(updated_author)


@router.delete(
    "/{author_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить автора по id",
)
async def delete(
    author_id: uuid.UUID = Path(..., description="ID автора"),
    service: AuthorService = Depends(get_author_service),
):
    return await service.delete(author_id)
