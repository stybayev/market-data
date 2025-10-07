"""Модуль для работы с PostgreSQL базой данных."""

from typing import AsyncGenerator

import httpx
from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

Base = declarative_base()

engine = create_async_engine(
    settings.db.url,
    echo=settings.log_sql_queries,
    future=True,
)

async_session = sessionmaker(  # type: ignore
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def purge_database() -> None:
    """Очистка базы данных от всех таблиц."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Генератор сессий базы данных.

    Yields:
        AsyncSession: Асинхронная сессия SQLAlchemy.

    Raises:
        Exception: Если возникает ошибка при работе сессии.
    """
    async with async_session() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_http_client() -> AsyncGenerator[httpx.AsyncClient, None]:
    """Генератор HTTP клиентов.

    Yields:
        httpx.AsyncClient: Асинхронный HTTP клиент.
    """
    async with httpx.AsyncClient() as client:
        yield client


async def create_db_and_tables() -> None:
    """Создание базы данных и таблиц."""
    async with engine.begin() as conn:
        await conn.execute(text('CREATE SCHEMA IF NOT EXISTS auth'))
        await conn.run_sync(Base.metadata.create_all)


USER_DB_DEPENDENCY = Depends(get_db_session)


async def get_user_db(session: AsyncSession = USER_DB_DEPENDENCY) -> AsyncGenerator[SQLAlchemyUserDatabase, None]:  # type: ignore # noqa
    """Получение базы данных пользователей.

    Args:
        session: Асинхронная сессия SQLAlchemy.

    Yields:
        SQLAlchemyUserDatabase: База данных пользователей.
    """
    from app.models.users import User  # noqa: WPS433

    yield SQLAlchemyUserDatabase(session, User)
