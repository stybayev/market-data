"""Модуль содержит исключения для валидации входящих данных."""

from typing import Any, Dict

from fastapi import status

from app.utils import messages
from app.utils.exceptions.base import BaseApplicationError


class ValidationError(BaseApplicationError):
    """Исключение для ошибок валидации."""

    def __init__(
        self,
        message: str = 'Ошибка валидации',
        detail: Dict[str, Any] | None = None,
    ) -> None:
        """Инициализация исключения валидации.

        Args:
            message: Сообщение об ошибке.
            detail: Дополнительные детали ошибки.
        """
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
        )


class InvalidPhoneNumberError(ValidationError):
    """Исключение для недействительного номера телефона."""

    def __init__(
        self,
        message: str = messages.INVALID_PHONE,
        detail: Dict[str, Any] | None = None,
    ) -> None:
        """Инициализация исключения недействительного номера.

        Args:
            message: Сообщение об ошибке.
            detail: Дополнительные детали ошибки.
        """
        super().__init__(
            message=message,
            detail=detail,
        )


class EmailValidationError(ValidationError):
    """Исключение для ошибок валидации email."""

    def __init__(
        self,
        message: str = messages.INVALID_EMAIL,
        detail: Dict[str, Any] | None = None,
    ) -> None:
        """Инициализация исключения валидации email."""
        super().__init__(
            message=message,
            detail=detail or {'field': 'email'},
        )


class EmptyFieldError(ValidationError):
    """Исключение для пустых обязательных полей."""

    def __init__(
        self,
        field: str,
        message: str | None = None,
        detail: Dict[str, Any] | None = None,
    ) -> None:
        """Инициализация исключения пустого поля.

        Args:
            message: Сообщение об ошибке.
            detail: Дополнительные детали ошибки.
        """
        super().__init__(
            message=message or f'Поле {field} не должно быть пустым',
            detail=detail or {'field': field},
        )


class InvalidVerificationCodeError(ValidationError):
    """Исключение для ошибок если недопустимый код подтверждения."""

    def __init__(
        self,
        message: str = messages.VERIFY_CODE_ERROR,
        detail: Dict[str, Any] | None = None,
    ) -> None:
        """
        Инициализация исключения если недопустимый код для подтверждения почты или телефона.

        Args:
            message: Сообщение об ошибке.
            detail: Дополнительные детали ошибки.
        """
        super().__init__(
            message=message,
            detail=detail,
        )
