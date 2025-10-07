"""Модуль содержит базовые исключения приложения."""

from typing import Any, Dict

from fastapi import status


class BaseApplicationError(Exception):
    """Базовый класс для всех кастомных исключений приложения."""

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail: Dict[str, Any] | None = None,
    ) -> None:
        """Инициализация базового исключения.

        Args:
            message: Сообщение об ошибке.
            status_code: HTTP код статуса.
            detail: Дополнительные детали ошибки.
        """
        self.message = message
        self.status_code = status_code
        self.detail = detail
        super().__init__(self.message)
