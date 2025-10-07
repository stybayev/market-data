"""Основной модуль FastAPI приложения."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from async_fastapi_jwt_auth import AuthJWT
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis
from sqlalchemy.exc import SQLAlchemyError
import sentry_sdk

from app.api.v1.users import router as router_users
from app.api.v1.anketa import router as router_anketa
from app.api.v1.brokerage_account import router as router_brokerage_account
from app.api.v1.admin_panel import router as router_admin_panel
from app.core.config import settings
from app.core.jwt import JWTSettings
from app.db import redis
from app.dependencies.main import setup_dependencies
from app.utils.exceptions.base import BaseApplicationError
from app.utils.exceptions.error_handlers import (
    validation_exception_handler,
    application_error_handler,
    sqlalchemy_error_handler,
)
from app.utils.exceptions.validation import ValidationError


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Контекстный менеджер жизненного цикла приложения.

    Args:
        app: Экземпляр FastAPI приложения.

    Yields:
        None: Отдает управление приложению.
    """
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        send_default_pii=True,
    )

    AuthJWT.load_config(JWTSettings)
    redis.connection = Redis(host=settings.redis_host, port=settings.redis_port)

    yield

    await redis.connection.close()

app = FastAPI(
    title=settings.project_name,
    docs_url='/api/auth/openapi',
    openapi_url='/api/auth/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
    swagger_ui_oauth2_redirect_url='/api/v1/auth/users/login',
)

# Регистрация ендпойнтов
app.include_router(router_users, prefix='/api/v1/users')

# Регистрация обработчиков ошибок
app.add_exception_handler(BaseApplicationError, application_error_handler)  # type: ignore
app.add_exception_handler(ValidationError, validation_exception_handler)  # type: ignore
app.add_exception_handler(SQLAlchemyError, sqlalchemy_error_handler)  # type: ignore

# Регистрация зависимостей
setup_dependencies(app)
