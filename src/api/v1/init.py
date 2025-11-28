from fastapi import FastAPI

from src.domains.author.api import router as author_router
from src.domains.genre.api import router as genre_router

api_base_prefix = "/api/v1"

routers = {
    "author": ["/author", author_router],
    "genre": ["/genre", genre_router],
}


def init_routers(app: FastAPI):
    for tag, router_settings in routers.items():
        prefix, router = router_settings
        prefix = f"{api_base_prefix}{prefix}"
        app.include_router(router=router, prefix=prefix, tags=[tag])
