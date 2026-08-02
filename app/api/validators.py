from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_projects_crud
from app.models import CharityProject


async def check_name_duplicate(
        projects_name: str,
        session: AsyncSession
) -> None:
    """Проверяет есть ли такое name, если есть, то выкидывает ошибку"""
    id_project = await charity_projects_crud.get_projects_id_by_name(
        projects_name, session
    )
    if id_project is not None:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!'
        )


async def check_charity_projects_exists(
        project_id: int,
        session: AsyncSession
) -> CharityProject:
    """
    Проверяет, есть ли такой проект по id, если есть, то возвращает проект
    Если нет, выкидывает ошибку
    """
    charity_project = await charity_projects_crud.get(project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден!'
        )
    return charity_project


async def check_charity_project_is_closed(project: CharityProject) -> None:
    """Проверяет, закрыт ли проект. Если да выбрасывает ошибку 400"""
    if project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail='Нельзя закрыть или изменять закрытый проект'
        )


async def check_new_full_amount(
    project: CharityProject,
    new_full_amount: int | None
) -> None:
    """Проверяет, что новая требуемая сумма не меньше уже вложенной"""
    if (new_full_amount is not None and
            new_full_amount < project.invested_amount):
        raise HTTPException(
            status_code=400,
            detail='Нельзя установить значение'
            ' full_amount меньше уже вложенной суммы.'
        )


async def check_project_before_delete(project: CharityProject) -> None:
    """
    Проверяет, были ли уже внесены средства в проект.
    Если да — запрещает удаление.
    """
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!'
        )


async def any_closed_projects(projects: list):
    """
    Проверяет, есть ли закрытые проекты
    Если нет, то выкидывает ошибку
    """
    if not projects:
        raise HTTPException(
            status_code=404,
            detail='Нет закртытых проектов'
        )
