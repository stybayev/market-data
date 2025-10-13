"""Модуль для работы с Redis."""
import json
import os

from redis.asyncio import Redis

from app.core.config import Settings

connection: Redis | None = None  # type: ignore

PUBSUB_CHANNEL = os.getenv("PUBSUB_CHANNEL", "pubsub:subs:diff")


async def init_redis(settings: Settings) -> None:
    """
    Инициализирует соединение с Redis.
    """
    global connection
    connection = Redis(host=settings.redis_host, port=settings.redis_port, decode_responses=True)


async def close_redis() -> None:
    """
    Закрывает соединение с Redis.
    """
    if connection is not None:
        await connection.close()
        connection = None


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


async def publish_subs_command(action: str, user_id: int, tickers: list[str], **meta) -> None:
    """
    Публикует команду управления подписками в Redis Pub/Sub.
    """
    r = await get_redis()
    payload = {
        "op": action,  # "subscribe" | "unsubscribe" | "set"
        "user_id": user_id,
        "tickers": tickers,
    }
    if meta:
        payload.update(meta)

    await r.publish(PUBSUB_CHANNEL, json.dumps(payload, separators=(",", ":")))
