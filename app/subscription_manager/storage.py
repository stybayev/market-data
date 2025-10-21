"""Адаптеры хранилищ подписок."""

from __future__ import annotations

from typing import Iterable

from redis.asyncio import Redis

from app.subscription_manager.service import SubscriptionStorage


class RedisSubscriptionStorage(SubscriptionStorage):
    """Хранит подписки пользователя в Redis как множества."""

    def __init__(self, redis: Redis, *, namespace: str = 'subs') -> None:
        self._redis = redis
        self._namespace = namespace

    async def add_tickers(self, user_id: int, tickers: list[str]) -> list[str]:
        if tickers:
            await self._redis.sadd(self._key(user_id), *tickers)
        return await self._fetch(user_id)

    async def remove_tickers(self, user_id: int, tickers: list[str]) -> list[str]:
        if tickers:
            await self._redis.srem(self._key(user_id), *tickers)
        return await self._fetch(user_id)

    async def set_tickers(self, user_id: int, tickers: list[str]) -> list[str]:
        key = self._key(user_id)
        if tickers:
            pipe = self._redis.pipeline()
            pipe.delete(key)
            pipe.sadd(key, *tickers)
            await pipe.execute()
        else:
            await self._redis.delete(key)
        return await self._fetch(user_id)

    async def _fetch(self, user_id: int) -> list[str]:
        members: Iterable[str] = await self._redis.smembers(self._key(user_id))
        return sorted(members)

    def _key(self, user_id: int) -> str:
        return f'{self._namespace}:{user_id}'

