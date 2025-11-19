from fastapi import FastAPI

from src.api.v1.author import router as author_router
from src.api.v1.root import router as root_router

api_base_prefix = "/api/v1"

routers = {
    "root": ["", root_router],
    "author": ["/author", author_router],
}


def init_routers(app: FastAPI):
    for tag, router_settings in routers.items():
        prefix, router = router_settings
        prefix = f"{api_base_prefix}{prefix}"
        app.include_router(router=router, prefix=prefix, tags=[tag])
