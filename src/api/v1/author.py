import uuid
from typing import List, Union

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status

from src.exceptions.entity import AuthorNotFound
from src.schemas.author import AuthorResponse, AuthorWithGenreResponse
from src.services.author import AuthorService, get_author_service

router = APIRouter()


@router.get(
    "/",
    response_model=Union[List[AuthorResponse], List[AuthorWithGenreResponse]],
    summary="Получить список авторов",
)
async def get_all(
    service: AuthorService = Depends(get_author_service),
    skip: int = Query(0, description="Смещение относительно первого элемента в списке"),
    limit: int = Query(100, description="Сколько элементов загружать в список"),
    with_genre: bool = Query(False, description="Загружать ли жанры"),
):
    authors = await service.get_all(skip=skip, limit=limit, with_genre=with_genre)

    return authors


@router.get(
    "/{id}",
    response_model=Union[AuthorResponse, AuthorWithGenreResponse],
    summary="Получить автора по id",
)
async def get_by_id(
    service: AuthorService = Depends(get_author_service),
    id: uuid.UUID = Path(..., description="ID автора"),
    with_genre: bool = Query(False, description="Загружать ли жанры"),
):
    try:
        author = await service.get_by_id(author_id=id, with_genre=with_genre)
        return author
    except AuthorNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.msg)
