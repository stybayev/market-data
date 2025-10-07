"""Модуль содержит обработчики ошибок для FastAPI приложения."""
import sentry_sdk
from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from starlette import status

from app.utils.exceptions.base import BaseApplicationError
from app.utils.exceptions.validation import ValidationError


async def validation_exception_handler(
    request: Request,
    exc: ValidationError,
) -> JSONResponse:
    """Обработчик ошибок валидации FastAPI.

    Args:
        request: Объект запроса.
        exc: Объект исключения.

    Returns:
        JSONResponse: Отформатированный ответ с ошибкой.
    """
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            'message': exc.message,
            'detail': exc.detail,
            'status_code': exc.status_code,
        },
    )


async def application_error_handler(
    request: Request,
    exc: BaseApplicationError,
) -> JSONResponse:
    """Обработчик кастомных ошибок приложения.

    Args:
        request: Объект запроса.
        exc: Объект исключения.

    Returns:
        JSONResponse: Отформатированный ответ с ошибкой.
    """
    with sentry_sdk.new_scope() as scope:
        scope.set_tag('handler', 'application_error_handler')
        scope.set_context('request', {'path': str(request.url), 'method': request.method})
        sentry_sdk.capture_exception(exc)

    return JSONResponse(
        status_code=exc.status_code,
        content={
            'message': exc.message,
            'detail': exc.detail,
            'status_code': exc.status_code,
        },
    )


async def sqlalchemy_error_handler(
    request: Request,
    exc: SQLAlchemyError,
) -> JSONResponse:
    """Обработчик ошибок SQLAlchemy.

    Args:
        request: Объект запроса.
        exc: Объект исключения.

    Returns:
        JSONResponse: Отформатированный ответ с ошибкой.
    """
    with sentry_sdk.new_scope() as scope:
        scope.set_tag('handler', 'sqlalchemy_error_handler')
        scope.set_context('request', {'path': str(request.url), 'method': request.method})
        sentry_sdk.capture_exception(exc)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            'message': 'Database error',
            'detail': str(exc),
            'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
        },
    )
