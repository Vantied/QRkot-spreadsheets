from typing import Optional

from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_title: str = 'Благотворительный фонд поддержки котиков QRKot'
    description: str = 'Сервис для поддержки котиков'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None
    secret: str = 'NOT_SECRET'
    jwt_lifetime: int = 3600
    yandex_disk_token: Optional[str] = None
    report_format: str = "%Y/%m/%d %H:%M:%S"

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
