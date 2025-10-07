"""Модуль содержит исключения, возникающие при ошибках взаимодействия с монолитом."""
from typing import Any

from fastapi import status

from app.utils.exceptions.base import BaseApplicationError


class MonolithResponseError(BaseApplicationError):
    """Исключение для ошибок связанная с монолитом."""

    def __init__(
        self,
        message: str,
        detail: dict[str, Any] | None = None,
    ) -> None:
        """
        Инициализация исключения.

        Args:
            message: Сообщение об ошибке.
            detail: Дополнительные детали ошибки.
        """
        super().__init__(
            message=message,
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=detail,
        )
