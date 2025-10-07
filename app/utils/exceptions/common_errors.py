"""Модуль содержит общие исключения."""

from typing import Any, Dict

from fastapi import status

from app.utils.exceptions.base import BaseApplicationError


class FieldAlreadyExistsError(BaseApplicationError):
    """Исключение для ошибок конфликтами полей."""

    def __init__(
        self,
        message: str,
        detail: Dict[str, Any] | None = None,
    ) -> None:
        """Инициализация исключения.

        Args:
            message: Сообщение об ошибке.
            detail: Дополнительные детали ошибки.
        """
        super().__init__(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )
