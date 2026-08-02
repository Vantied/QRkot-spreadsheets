from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.schemas.donation import DonationDB, DonationCreate, DonationFullInfoDB
from app.crud.donation import donations_crud
from app.models import CharityProject, User
from app.core.user import current_user, current_superuser


router = APIRouter()

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@router.get(
    '/',
    response_model=list[DonationFullInfoDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(session: SessionDep):
    """
    Показать список всех пожертвований
    Только для суперюзеров
    """
    results = await donations_crud.get_multi(session)
    return results


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True
)
async def create_donation(
    donation: DonationCreate,
    session: SessionDep,
    user: Annotated[User, Depends(current_user)],
):
    """
    Создать пожертвование
    Только для зарегистрированных пользователей
    """
    new_donation = await donations_crud.create(
        donation, session, invest_model=CharityProject, user=user)
    return new_donation


@router.get(
    '/my',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
)
async def get_user_donations(
    session: SessionDep,
    user: Annotated[User, Depends(current_user)],
):
    """
    Показать список пожертвований пользователя, выполняющего запрос.
    Только для зарегистрированных пользователей
    """
    donations = await donations_crud.get_donations_user(session, user)
    return donations