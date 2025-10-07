"""Модуль реализации HTTP клиента для выполнения API запросов."""

from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseHTTPClient(ABC):
    """
    Абстрактный базовый класс для HTTP клиентов.
    Определяет общий интерфейс для всех HTTP клиентов в системе.
    """

    @abstractmethod
    async def get(self, url: str, **kwargs: Any) -> Dict[str, Any]:
        """
        Выполнить GET запрос.

        Args:
            url: URL для запроса

        Returns:
            Dict[str, Any]: Ответ от сервера

        Raises:
            HTTPClientError: При ошибках HTTP запроса
        """
        raise NotImplementedError

    @abstractmethod
    async def post(self, url: str, json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Выполнить POST запрос.

        Args:
            url: URL для запроса
            json: Данные для отправки в формате JSON

        Returns:
            Dict[str, Any]: Ответ от сервера

        Raises:
            NotImplementedError
        """
        raise NotImplementedError
