from functools import cache

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


@cache
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        env_ignore_empty=True,
        extra='ignore',
    )

    database_drive: str
    database_host: str
    database_username: str
    database_password: str
    database_db: str
    database_port: int

    @computed_field
    @property
    def database_url(self) -> URL:
        return URL.create(
            drivername=self.database_drive,
            host=self.database_host,
            port=self.database_port,
            username=self.database_username,
            password=self.database_password,
            database=self.database_db,
        )
