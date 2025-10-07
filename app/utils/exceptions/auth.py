"""Модуль содержит исключения авторизации/регистрации."""

from typing import Any, Dict

from fastapi import status

from app.utils import messages
from app.utils.exceptions.base import BaseApplicationError


class InviteCodeNotFoundException(BaseApplicationError):
    """Исключение для ошибок инвайт кода."""

    def __init__(
        self,
        message: str = messages.REF_CODE_NOT_FOUND,
        detail: Dict[str, Any] | None = None,
    ) -> None:
        """Инициализация исключения.
        Args:
            message: Сообщение об ошибке.
            detail: Дополнительные детали ошибки.
        """
        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            detail={'field': 'invite'},
        )


class AuthenticationFailedError(BaseApplicationError):
    """Исключение для ошибок аутентификации."""

    def __init__(
        self,
        message: str = messages.USER_NOT_FOUND,
        detail: Dict[str, Any] | None = None,
    ) -> None:
        """Инициализация исключения.

        Args:
            message: Сообщение об ошибке.
            detail: Дополнительные детали ошибки.
        """
        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
        )


class UserInactiveError(BaseApplicationError):
    """Исключение для ошибки, если пользователь не активен."""

    def __init__(
        self,
        message: str = messages.USER_IN_ACTIVE,
        detail: Dict[str, Any] | None = None,
    ) -> None:
        """Инициализация исключения.

        Args:
            message: Сообщение об ошибке.
            detail: Дополнительные детали ошибки.
        """
        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
        )


class ForbiddenServiceTokenError(BaseApplicationError):
    """Исключение, если сервисный токен не совпадает."""

    def __init__(
        self,
        message: str = messages.INVALID_SERVICE_TOKEN,
        detail: Dict[str, Any] | None = None,
    ) -> None:
        """Инициализация исключения.

        Args:
            message: Сообщение об ошибке.
            detail: Дополнительные детали ошибки.
        """
        super().__init__(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )


class PermissionDeniedError(BaseApplicationError):
    """Исключение, если у пользователя нет необходимых прав."""

    def __init__(
        self,
        message: str = messages.PERMISSION_DENIED_MESSAGE,
        detail: Dict[str, Any] | None = None,
    ) -> None:
        """
        Инициализация исключения прав доступа.

        Args:
            message: Сообщение об ошибке.
            detail: Дополнительные детали ошибки.
        """
        super().__init__(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )
