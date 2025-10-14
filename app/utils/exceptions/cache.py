"""Исключения для кэширующих сервисов (Redis и т.п.)."""

from fastapi import status

from app.utils.exceptions.base import BaseApplicationError


class RedisNotInitializedError(BaseApplicationError):
    """Исключение для случаев, когда соединение с Redis не инициализировано."""

    def __init__(self) -> None:
        super().__init__(
            message='Соединение с Redis не инициализировано',
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        )
