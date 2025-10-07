"""Модуль содержит исключения БД."""

from typing import Any, Dict

from fastapi import status

from app.utils.exceptions.base import BaseApplicationError


class UniqueConstraintError(BaseApplicationError):
    """Исключение ограничения уникальности."""

    def __init__(
        self,
        message: str = 'Ошибка уникальности данных',
        detail: Dict[str, Any] | None = None,
    ) -> None:
        """Инициализация исключения уникальности.

        Args:
            message: Сообщение об ошибке.
            detail: Дополнительные детали ошибки.
        """
        super().__init__(
            message=message,
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
        )


class ObjectNotFoundError(BaseApplicationError):
    """Исключение объектов которых нет в базе."""

    def __init__(
        self,
        message: str,
        detail: Dict[str, Any] | None = None,
    ) -> None:
        """Инициализация исключения уникальности.

        Args:
            message: Сообщение об ошибке.
            detail: Дополнительные детали ошибки.
        """
        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )
