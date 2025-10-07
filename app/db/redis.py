"""Модуль для работы с Redis."""

from redis.asyncio import Redis

connection: Redis | None = None  # type: ignore


async def get_redis() -> Redis:  # type: ignore
    """
    Возвращает экземпляр Redis.

    Returns:
        Redis: Экземпляр Redis

    Raises:
        ValueError: Если соединение Redis не инициализировано
    """
    if not connection:
        raise ValueError('Соединение Redis не инициализировано')
    return connection
