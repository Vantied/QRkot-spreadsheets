from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class DonationBase(BaseModel):
    full_amount: int = Field(gt=0)
    comment: str | None = None


class DonationCreate(DonationBase):
    pass


class DonationDB(DonationBase):
    id: int
    create_date: datetime

    model_config = ConfigDict(from_attributes=True)


class DonationFullInfoDB(DonationDB):
    invested_amount: int
    fully_invested: bool
    close_date: datetime | None
    user_id: int
