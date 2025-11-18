from typing import List, Union

from fastapi import APIRouter, Depends, Query

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
