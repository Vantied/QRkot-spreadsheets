from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.investment import process_investment


class CRUDBase:

    def __init__(self, model):
        self.model = model

    async def get_uninvested(
        self,
        model,
        session: AsyncSession
    ):
        db_objs = await session.execute(
            select(model)
            .where(model.fully_invested.is_(False))
            .order_by(model.create_date)
        )
        return db_objs.scalars().all()

    async def get(
        self,
        obj_id: int,
        session: AsyncSession,
    ):
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def get_multi(
        self,
        session: AsyncSession
    ):
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
        self,
        obj_in,
        session: AsyncSession,
        invest_model=None,
        user=None
    ):
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data)
        db_obj.invested_amount = 0

        if user is not None:
            db_obj.user_id = user.id

        session.add(db_obj)

        if invest_model is not None:
            uninvested_objects = await self.get_uninvested(
                invest_model, session
            )

            if uninvested_objects:
                db_obj, updated_objects = process_investment(
                    db_obj, uninvested_objects)
                session.add_all(updated_objects)

        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db_obj,
        obj_in,
        session: AsyncSession,
    ):
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.model_dump(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
        self,
        db_obj,
        session: AsyncSession,
    ):
        await session.delete(db_obj)
        await session.commit()
        return db_obj
