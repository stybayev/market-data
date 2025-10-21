"""Фоновый обработчик команд подписок."""

from __future__ import annotations

import asyncio
import json
import logging
from typing import Any

from redis.asyncio import Redis

from app.enums import Action
from app.schemas.pubsub import SubscriptionCommandDTO
from app.subscription_manager.service import SubscriptionManager

logger = logging.getLogger(__name__)


class SubscriptionManagerWorker:
    """Читает команды из Redis Pub/Sub и применяет их через менеджер."""

    def __init__(self, redis: Redis, manager: SubscriptionManager, channel: str) -> None:
        self._redis = redis
        self._manager = manager
        self._channel = channel
        self._stop_event = asyncio.Event()

    async def run(self) -> None:
        if not self._channel:
            raise ValueError('redis pubsub channel is not configured')

        logger.info('subscription-manager starting, channel=%s', self._channel)

        async with self._redis.pubsub() as pubsub:
            await pubsub.subscribe(self._channel)

            async for message in pubsub.listen():
                if self._stop_event.is_set():
                    break
                if not _is_data_message(message):
                    continue
                await self._process_message(message['data'])

        logger.info('subscription-manager stopped')

    async def stop(self) -> None:
        self._stop_event.set()
        await self._redis.publish(self._channel, '__stop__')

    async def _process_message(self, payload: Any) -> None:
        try:
            raw = payload.decode() if isinstance(payload, bytes) else str(payload)
            data = json.loads(raw)
            dto = SubscriptionCommandDTO(**data)
        except Exception as exc:  # noqa: BLE001 - нужно логировать и продолжать работу
            logger.exception('failed to decode subscription command: %s', exc)
            return

        try:
            new_state = await self._manager.handle(
                action=dto.op,
                user_id=dto.user_id,
                tickers=dto.tickers,
            )
        except Exception as exc:  # noqa: BLE001 - не прерываем воркер
            logger.exception(
                'failed to apply command action=%s user_id=%s tickers=%s: %s',
                dto.op,
                dto.user_id,
                dto.tickers,
                exc,
            )
            return

        logger.debug(
            'processed command action=%s user_id=%s tickers=%s new_state=%s',
            dto.op,
            dto.user_id,
            dto.tickers,
            new_state,
        )


def _is_data_message(message: dict[str, Any]) -> bool:
    if message.get('type') != 'message':
        return False
    data = message.get('data')
    if data in {1, b'1'}:  # redis subscribe confirmation
        return False
    if data == '__stop__':
        return False
    if data in {Action.SUBSCRIBE.value, Action.UNSUBSCRIBE.value, Action.SET.value}:  # noqa:SIM103
        # redis.publish с raw строкой (например, команда subscribe) — пропускаем
        return False
    return True
