from typing import Annotated
from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.schemas.charity_project import (
    CharityProjectsDB, CharityProjectsCreate, CharityProjectsUpdate
)
from app.crud.charity_project import charity_projects_crud
from app.api.validators import (
    check_name_duplicate,
    check_charity_projects_exists,
    check_charity_project_is_closed,
    check_new_full_amount,
    check_project_before_delete
)
from app.models import Donation
from app.core.user import current_superuser


router = APIRouter()

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@router.get(
    '/',
    response_model=list[CharityProjectsDB],
)
async def get_all_charity_projects(session: SessionDep):
    """
    Показать список всех целевых проектов
    Для всех пользователей
    """
    results = await charity_projects_crud.get_multi(session)
    return results


@router.post(
    '/',
    response_model=CharityProjectsDB,
    dependencies=[Depends(current_superuser)]
)
async def create_charity_project(
    charity_project: CharityProjectsCreate,
    session: SessionDep,
):
    """
    Создать целевой проект
    Только для суперюзеров
    """
    await check_name_duplicate(charity_project.name, session)
    new_project = await charity_projects_crud.create(
        charity_project, session, invest_model=Donation)
    return new_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectsDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_projects(
    project_id: int,
    obj_in: CharityProjectsUpdate,
    session: SessionDep,
):
    """
    Редактировать целевой проект.
    Закрытый проект нельзя редактировать;
    нельзя установить требуемую сумму меньше уже вложенной
    Только для суперюзеров
    """
    project = await check_charity_projects_exists(project_id, session)
    await check_charity_project_is_closed(project)

    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)

    await check_new_full_amount(project, obj_in.full_amount)

    if obj_in.full_amount == project.invested_amount:
        project.fully_invested = True
        project.close_date = datetime.now()

    project = await charity_projects_crud.update(project, obj_in, session)
    return project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectsDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_projects(
    project_id: int,
    session: SessionDep
):
    """
    Удалить целевой проект.
    Нельзя удалить проект, в который уже были инвестированы средства
    Только для суперюзеров
    """
    project = await check_charity_projects_exists(project_id, session)
    await check_charity_project_is_closed(project)

    await check_project_before_delete(project)

    project = await charity_projects_crud.remove(project, session)
    return project
