"""Реализация клиента для взаимодействия с API брокера Alpaca."""
import base64
import logging
from typing import Any
from uuid import UUID

from app.core.clients.base_http_client import BaseHTTPClient
from app.core.integrations.base import BaseIntegration
from app.enums.alpaca import AlpacaUrlsEnum
from app.utils import messages
from app.utils.backoff import backoff
from app.utils.exceptions.http_clients import HTTPClientConnectionError
from app.utils.http_error_handlers import handle_client_errors

logger = logging.getLogger(__name__)


class AlpacaIntegration(BaseIntegration):
    """Клиент для работы с API брокера Alpaca."""

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        client: BaseHTTPClient | None = None,
    ):
        """
        Инициализация клиента Alpaca.

        Args:
            api_key (str): Публичный API-ключ Alpaca.
            api_secret (str): Секретный ключ Alpaca.
            client (BaseHTTPClient | None): HTTP клиент
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.client = client

    # TODO(Alibek): Удалить этот метод после подключения мультисчетов.
    #       Логика закрытия брокерского счёта будет перенесена в монолит,
    #       так как теперь у пользователя может быть несколько брокерских счетов (мультисчета).
    @backoff(exceptions=(HTTPClientConnectionError,))
    @handle_client_errors
    async def close_account(self, broker_id: UUID, **kwargs: dict[str, Any]) -> None:
        """
        Закрывает брокерский аккаунт пользователя в Alpaca.

        Args:
            broker_id (UUID): ID брокерского аккаунта.
            kwargs: Дополнительные аргументы.

        Logs:
            - Ошибку, если HTTP-клиент не инициализирован.
        """
        if self.client is None:
            logger.error(messages.HTTP_CLIENT_NOT_INITIALIZED)
            return

        await self._get_auth_headers()

        url: str = AlpacaUrlsEnum.close_account.value.replace(':account_id', str(broker_id))
        await self.client.post(url=url, json={})

    @backoff(exceptions=(HTTPClientConnectionError,))
    @handle_client_errors
    async def get_account_by_id(self, broker_id: UUID) -> dict[str, Any] | None:
        """
        Возвращает данные брокерского аккаунта пользователя в Alpaca.

        Args:
            broker_id (UUID): ID брокерского аккаунта.

        Returns:
            dict[str, Any] | None: Данные аккаунта, если успешно получены,
            иначе None, если HTTP-клиент не инициализирован.
        """
        if self.client is None:
            logger.error(messages.HTTP_CLIENT_NOT_INITIALIZED)
            return None

        await self._get_auth_headers()

        url: str = AlpacaUrlsEnum.account_id.value.replace(':account_id', str(broker_id))
        return await self.client.get(url=url)

    async def _get_auth_headers(self) -> None:
        """
        Устанавливает заголовок Authorization для HTTP-клиента.

        Формирует строку авторизации из API-ключа и секретного ключа,
        кодирует её в Base64 и добавляет в заголовки клиента.
        """
        auth_string = f'{self.api_key}:{self.api_secret}'
        auth_string_encoded = base64.b64encode(str.encode(auth_string)).decode('utf-8')

        self.client.default_headers['Authorization'] = (  # type: ignore
            f'Basic {auth_string_encoded}'
        )
