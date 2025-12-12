from fastapi import FastAPI
from src.auth.api import router as auth_router
from src.domains.author.api import router as author_router
from src.domains.genre.api import router as genre_router
from src.domains.user.api import router as user_router
from src.domains.favorites.api import router as favorites_router
from src.domains.category.api import router as category_router
from src.domains.review.api import router as review_router

from src.setting import settings

routers = {
    "author": ["/author", author_router],
    "genre": ["/genre", genre_router],
    "category": ["/category", category_router],
    "favorites": ["/favorites", favorites_router],
    "review": ["/review", review_router],
    "user": ["/user", user_router],
    "auth": [settings.auth_prefix, auth_router],
}


def init_routers(app: FastAPI):
    for tag, router_settings in routers.items():
        prefix, router = router_settings
        prefix = f"{settings.api_base_prefix}{prefix}"
        app.include_router(router=router, prefix=prefix, tags=[tag])
