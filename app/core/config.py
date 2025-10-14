"""
Конфигурация приложения.

Этот модуль содержит классы и настройки для управления конфигурацией приложения.
"""

import os
from logging import config as logging_config

from pydantic.v1 import BaseSettings

from app.core.database import DataBaseSettings
from app.core.logger import LOGGING

ENV_FILE_PATH = '.env'


class Settings(BaseSettings):
    """
    Основные настройки приложения.

    Атрибуты:
        project_name: Название проекта.
        uvicorn_host: Хост для Uvicorn.
        uvicorn_port: Порт для Uvicorn.
        db: Настройки базы данных.
        log_sql_queries: Флаг для логирования SQL-запросов.
        redis_host: Хост Redis.
        redis_port: Порт Redis.
    """

    # App
    project_name: str

    # Postgres
    db: DataBaseSettings = DataBaseSettings()  # type: ignore
    log_sql_queries: bool = False

    # Redis
    redis_host: str
    redis_port: int
    redis_pubsub_channel: str = 'pubsub:subs:diff'

    # Logging
    sentry_dsn: str

    class Config:
        """Конфигурация для загрузки переменных окружения."""

        env_file = ENV_FILE_PATH
        env_prefix = 'MARKET_DATA_'


# Создаем экземпляр класса Settings для хранения настроек
settings = Settings()  # type: ignore

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # noqa: WPS221
