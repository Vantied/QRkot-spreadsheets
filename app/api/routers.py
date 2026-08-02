from fastapi import APIRouter

from app.api.endpoints import (
    charity_projects_router,
    donations_router,
    user_router,
    yandex_router,
)

main_router = APIRouter()
main_router.include_router(
    charity_projects_router,
    prefix='/charity_project',
    tags=['charity_project']
)
main_router.include_router(
    donations_router, prefix='/donation', tags=['donation']
)
main_router.include_router(
    yandex_router,
    prefix='/yandex',
    tags=['Yandex Disk']
)
main_router.include_router(user_router)
