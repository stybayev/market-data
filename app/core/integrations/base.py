"""Абстрактный клиент для взаимодействия с API брокера."""
from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID


class BaseIntegration(ABC):
    """Абстрактный базовый класс клиента для работы с брокерским API."""

    @abstractmethod
    async def close_account(self, broker_id: UUID, **kwargs: Any) -> None:
        """
        Закрытие брокерского аккаунта пользователя.

        Args:
            broker_id (UUID): ID брокерского аккаунта пользователя.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_account_by_id(self, broker_id: UUID) -> dict[str, Any] | None:
        """
        Возвращает данные брокерского аккаунта пользователя.

        Args:
            broker_id (UUID): ID брокерского аккаунта пользователя.
        """
        raise NotImplementedError
