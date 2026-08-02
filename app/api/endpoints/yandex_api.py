from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.charity_project import charity_projects_crud
from app.core.user import current_superuser
from app.core.yandex_client import YandexDiskClient, get_yandex_client
from app.api.validators import any_closed_projects
from app.services.yandex_api import create_simple_report


router = APIRouter()

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@router.post(
    '/',
    response_model=str,
    dependencies=[Depends(current_superuser)]
)
async def get_report(
    session: SessionDep,
    yandex_client: YandexDiskClient = Depends(get_yandex_client)
):
    """
    Создать отчёт и получить ссылку на него
    Только для суперюзеров
    """
    closed_projects = await (
        charity_projects_crud
        .get_projects_by_completion_rate(session)
    )
    await any_closed_projects(closed_projects)

    try:
        url = await create_simple_report(closed_projects, yandex_client)
        return url
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f'Ошибка при создании отчёта: {str(e)}'
        )
