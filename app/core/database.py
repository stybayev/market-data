"""Модуль настроек подключения к базе данных PostgreSQL."""
from pydantic.v1 import BaseSettings

ENV_FILE_PATH = '.env'


class DataBaseSettings(BaseSettings):
    """
    Настройки подключения к базе данных PostgreSQL.

    Атрибуты:
        user: Имя пользователя для подключения.
        password: Пароль пользователя.
        db: Имя базы данных.
        host: Хост базы данных.
        port: Порт базы данных.
    """

    user: str
    password: str
    db: str
    host: str
    port: int

    class Config:
        """Конфигурация для загрузки переменных окружения."""

        env_file = ENV_FILE_PATH
        env_prefix = 'POSTGRES_'

    @property
    def url(self) -> str:
        """
        Генерация URL для подключения к базе данных.

        Returns:
            str: URL для подключения.
        """
        return f'postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}'  # noqa: E501
