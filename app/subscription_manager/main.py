"""Точка входа для сервиса Subscription Manager."""

from __future__ import annotations

import asyncio
import logging

from app.core.config import settings
from app.db.redis import close_redis, get_redis, init_redis
from app.subscription_manager.service import SubscriptionManager
from app.subscription_manager.storage import RedisSubscriptionStorage
from app.subscription_manager.worker import SubscriptionManagerWorker

logger = logging.getLogger(__name__)


async def main() -> None:
    await init_redis(settings)

    redis = await get_redis()
    storage = RedisSubscriptionStorage(redis)
    manager = SubscriptionManager(storage, max_subs_per_user=settings.ws_max_subs_per_user)
    worker = SubscriptionManagerWorker(redis, manager, settings.redis_pubsub_channel or '')

    try:
        await worker.run()
    finally:
        await close_redis()


def run() -> None:
    """Запускает главный цикл сервиса."""
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info('subscription-manager interrupted by user')


if __name__ == '__main__':
    run()

