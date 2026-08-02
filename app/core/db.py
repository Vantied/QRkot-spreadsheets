from datetime import datetime

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import Integer, Boolean, DateTime, CheckConstraint
from sqlalchemy.orm import (
    DeclarativeBase, Mapped, mapped_column, declared_attr
)

from app.core.config import settings


class Base(DeclarativeBase):  # noqa: PIE793
    pass


class CommonMixin:  # noqa: PIE793
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class FinancialMixin:  # noqa: PIE793
    @declared_attr
    def __table_args__(cls):
        return (
            CheckConstraint(
                'full_amount > 0',
                name='check_full_amount_positive'
            ),
            CheckConstraint(
                'invested_amount <= full_amount',
                name='check_invested_amount_less_than_full'
            ),
        )

    full_amount: Mapped[int] = mapped_column(Integer)
    invested_amount: Mapped[int] = mapped_column(Integer, default=0)
    fully_invested: Mapped[bool] = mapped_column(Boolean, default=False)
    create_date: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now)
    close_date: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True)


engine = create_async_engine(settings.database_url)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session():
    async with AsyncSessionLocal() as async_session:
        yield async_session
