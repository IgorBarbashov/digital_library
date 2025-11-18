from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

# from src.exceptions.entity import AuthorNotFound
from src.schemas.author import AuthorResponse
from src.services.author import AuthorService, get_author_service

router = APIRouter()


@router.get(
    "/",
    response_model=List[AuthorResponse],
    summary="Получить список авторов",
)
async def get_all(
    service: AuthorService = Depends(get_author_service),
):
    skip: int = 0
    limit: int = 100
    authors = await service.get_all(skip=skip, limit=limit)

    print("!!!!!!!!!!!!!!!!", authors)

    return authors


# @router.get(
#     "/author",
#     response_model=List[AuthorResponse],
#     summary="Получить список авторов",
# )
# async def get_all(
#     service: AuthorService = Depends(get_author_service),
# ):
#     skip: int = 0
#     limit: int = 100

#     try:
#         authors = await service.get_all(skip=skip, limit=limit)
#     except AuthorNotFound as e:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.msg)

#     return
