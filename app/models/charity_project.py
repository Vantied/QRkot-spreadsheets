from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base, CommonMixin, FinancialMixin
from app.core.constants import NAME_MAX_LENGTH


class CharityProject(CommonMixin, FinancialMixin, Base):
    name: Mapped[str] = mapped_column(String(NAME_MAX_LENGTH), unique=True)
    description: Mapped[str] = mapped_column(Text)
