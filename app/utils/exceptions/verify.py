"""Модуль содержит исключения подтверждения почты или телефона."""
from typing import Any

from fastapi import status

from app.utils import messages
from app.utils.exceptions.base import BaseApplicationError


class VerifyCodeValidationError(BaseApplicationError):
    """Исключение для ошибок валидации кода подтверждения."""

    def __init__(
        self,
        field: str,
        message: str = messages.INCORRECT_VERIFY_CODE,
        detail: dict[str, Any] | None = None,
    ) -> None:
        """
        Инициализация исключения валидации кода подтверждения электронной почты.

        Args:
            field: Наименование передаваемого поля.
            message: Сообщение об ошибке.
            detail: Дополнительные детали ошибки.
        """
        super().__init__(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail or {'field': field},
        )


class EmailHasBeenVerifiedError(BaseApplicationError):
    """Исключение для ошибок если электронной почты уже верифицирована."""

    def __init__(
        self,
        message: str = messages.EMAIL_HAS_ALREADY_BEEN_VERIFIED,
        detail: dict[str, Any] | None = None,
    ) -> None:
        """
        Инициализация исключения если электронной почты уже верифицирована.

        Args:
            message: Сообщение об ошибке.
            detail: Дополнительные детали ошибки.
        """
        super().__init__(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )


class PhoneHasBeenVerifiedError(BaseApplicationError):
    """Исключение для ошибок если телефон уже верифицирован."""

    def __init__(
        self,
        message: str = messages.PHONE_HAS_ALREADY_BEEN_VERIFIED,
        detail: dict[str, Any] | None = None,
    ) -> None:
        """
        Инициализация исключения если телефон уже верифицирован.

        Args:
            message: Сообщение об ошибке.
            detail: Дополнительные детали ошибки.
        """
        super().__init__(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )
