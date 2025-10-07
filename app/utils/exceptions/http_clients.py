"""Модуль содержит исключения HTTP клиента."""

from typing import Any, Dict

from fastapi import status

from app.utils.exceptions.base import BaseApplicationError
from app.utils import messages


class HTTPClientError(BaseApplicationError):
    """Базовое исключение для ошибок HTTP клиента."""

    def __init__(
        self,
        message: str = messages.HTTP_CLIENT_ERROR,
        detail: Dict[str, Any] | None = None,
        status_code: int = status.HTTP_422_UNPROCESSABLE_ENTITY,
    ) -> None:
        """
        Инициализация исключения HTTP клиента.

        Args:
            message: Сообщение об ошибке.
            detail: Дополнительные детали ошибки.
            status_code: HTTP код статуса.
        """
        super().__init__(
            message=message,
            status_code=status_code,
            detail=detail,
        )


class HTTPClientTimeoutError(HTTPClientError):
    """Исключение для таймаутов."""

    def __init__(
        self,
        message: str = messages.HTTP_CLIENT_TIMEOUT_ERROR,
        detail: Dict[str, Any] | None = None,
    ) -> None:
        """
        Инициализация исключения таймаута.

        Args:
            message: Сообщение об ошибке.
            detail: Дополнительные детали ошибки.
        """
        super().__init__(
            message=message,
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail=detail,
        )


class HTTPClientConnectionError(HTTPClientError):
    """Исключение для ошибок соединения."""

    def __init__(
        self,
        message: str = messages.HTTP_CLIENT_CONNECTION_ERROR,
        detail: Dict[str, Any] | None = None,
    ) -> None:
        """
        Инициализация исключения соединения.

        Args:
            message: Сообщение об ошибке.
            detail: Дополнительные детали ошибки.
        """
        super().__init__(
            message=message,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=detail,
        )


class HTTPClientResponseError(HTTPClientError):
    """Исключение для ошибок ответа."""

    def __init__(
        self,
        message: str = messages.HTTP_CLIENT_RESPONSE_ERROR,
        detail: Dict[str, Any] | None = None,
        status_code: int = status.HTTP_422_UNPROCESSABLE_ENTITY,
    ) -> None:
        """
        Инициализация исключения ответа.

        Args:
            message: Сообщение об ошибке.
            detail: Дополнительные детали ошибки.
            status_code: HTTP код статуса.
        """
        super().__init__(
            message=message,
            status_code=status_code,
            detail=detail,
        )
