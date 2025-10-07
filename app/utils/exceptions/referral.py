"""Модуль содержит исключения для реферальной программы."""
from typing import Any

from fastapi import status

from app.utils.exceptions.base import BaseApplicationError


class PartnerValidationError(BaseApplicationError):
    """Исключение для ошибок связанные с партнерской программой."""

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        detail: dict[str, Any] | None = None,
    ) -> None:
        """
        Исключение для ошибок связанные с партнерской программой.

        Args:
            message: Сообщение об ошибке.
            status_code: HTTP код статуса.
            detail: Дополнительные детали ошибки.
        """
        super().__init__(
            message=message,
            status_code=status_code,
            detail=detail,
        )
