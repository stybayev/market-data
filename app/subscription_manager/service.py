"""Сервис, управляющий подписками пользователей."""

from __future__ import annotations

from typing import Iterable

from app.enums import Action


class SubscriptionManager:
    """Применяет команды подписок к хранилищу.

    Менеджер принимает команды из очереди и обновляет состояние подписок
    в хранилище. Логику доступа к данным предоставляет адаптер хранилища,
    удовлетворяющий интерфейсу, описанному в этом модуле.
    """

    def __init__(self, storage: "SubscriptionStorage", max_subs_per_user: int) -> None:
        self._storage = storage
        self._max_subs_per_user = max_subs_per_user

    async def handle(self, *, action: Action, user_id: int, tickers: Iterable[str]) -> list[str]:
        """Применяет команду подписки и возвращает новое состояние.

        Raises:
            ValueError: Если после применения команды нарушен лимит по количеству тикеров.
            ValueError: Если передана неподдерживаемая операция.
        """
        tickers_list = list(tickers)

        match action:
            case Action.SUBSCRIBE:
                new_state = await self._storage.add_tickers(user_id, tickers_list)
            case Action.UNSUBSCRIBE:
                new_state = await self._storage.remove_tickers(user_id, tickers_list)
            case Action.SET:
                new_state = await self._storage.set_tickers(user_id, tickers_list)
            case _:
                raise ValueError(f'unsupported action: {action}')

        if len(new_state) > self._max_subs_per_user:
            raise ValueError(
                f'user {user_id} has too many tickers: {len(new_state)} > {self._max_subs_per_user}'
            )

        return new_state


class SubscriptionStorage:
    """Интерфейс хранилища подписок."""

    async def add_tickers(self, user_id: int, tickers: list[str]) -> list[str]:
        raise NotImplementedError

    async def remove_tickers(self, user_id: int, tickers: list[str]) -> list[str]:
        raise NotImplementedError

    async def set_tickers(self, user_id: int, tickers: list[str]) -> list[str]:
        raise NotImplementedError

