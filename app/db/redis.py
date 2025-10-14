"""Модуль для работы с Redis."""
import json

from redis.asyncio import Redis

from app.core.config import Settings
from app.enums import Action
from app.schemas.pubsub import SubscriptionCommandDTO
from app.utils.exceptions.cache import RedisNotInitializedError

connection: Redis | None = None  # type: ignore
pubsub_channel: str | None = None


async def init_redis(settings: Settings) -> None:
    """
    Инициализирует соединение с Redis.
    """
    global connection
    global pubsub_channel
    connection = Redis(host=settings.redis_host, port=settings.redis_port, decode_responses=True)
    pubsub_channel = settings.redis_pubsub_channel


async def close_redis() -> None:
    """
    Закрывает соединение с Redis.
    """
    global connection
    global pubsub_channel
    if connection is not None:
        await connection.close()
        connection = None
    pubsub_channel = None


async def get_redis() -> Redis:  # type: ignore
    """
    Возвращает экземпляр Redis.

    Returns:
        Redis: Экземпляр Redis

    Raises:
        RedisNotInitializedError: Если соединение Redis не инициализировано
    """
    if not connection:
        raise RedisNotInitializedError()
    return connection


async def publish_subs_command(action: Action, user_id: int, tickers: list[str], **meta) -> None:
    """
    Публикует команду управления подписками в Redis Pub/Sub.
    """
    r = await get_redis()
    if pubsub_channel is None:
        raise RedisNotInitializedError()
    command = SubscriptionCommandDTO(op=action, user_id=user_id, tickers=tickers, **meta)
    await r.publish(
        pubsub_channel,
        json.dumps(command.model_dump(exclude_none=True), separators=(',', ':')),
    )
