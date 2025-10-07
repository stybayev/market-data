"""Модуль реализации HTTP клиента для выполнения API запросов."""

from contextlib import asynccontextmanager
from typing import Any, Dict, AsyncGenerator

import httpx

from app.core.clients.base_http_client import BaseHTTPClient
from app.utils.exceptions.http_clients import (
    HTTPClientTimeoutError,
    HTTPClientResponseError,
    HTTPClientConnectionError,
    HTTPClientError,
)

ERROR_KEY = 'error'


class HTTPClient(BaseHTTPClient):
    """Базовый HTTP клиент с общей функциональностью."""

    def __init__(
        self,
        base_url: str,
        api_key: str | None = None,
        timeout: int = 10,
    ) -> None:
        """
        Инициализация HTTP клиента.

        Args:
            base_url: Базовый URL
            api_key: Ключ API
            timeout: Время ожидания запроса
        """
        self.base_url = base_url
        self.timeout = timeout
        self.default_headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

    @asynccontextmanager
    async def get_httpx_client(self) -> AsyncGenerator[httpx.AsyncClient, None]:
        """
        Контекстный менеджер для получения httpx клиента.

        Yields:
            httpx.AsyncClient: Асинхронный HTTP клиент.
        """
        async with httpx.AsyncClient(
            base_url=self.base_url,
            headers=self.default_headers,
            timeout=self.timeout,
        ) as client:
            yield client

    async def post(  # noqa: C901, WPS238, WPS231
        self,
        url: str,
        json: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Выполнить POST запрос.

        Args:
            url: URL для запроса
            json: Данные для отправки в формате JSON

        Returns:
            Dict[str, Any]: Ответ от сервера

        Raises:
            HTTPClientError: При ошибках HTTP запроса
            HTTPClientConnectionError: При ошибке соединения
            HTTPClientResponseError: При ошибке ответа
            HTTPClientTimeoutError: При таймауте
        """
        async with self.get_httpx_client() as client:
            try:  # noqa: WPS225, WPS229
                response = await client.post(url, json=json)
                response.raise_for_status()

                if not response.content:
                    return {}

                return response.json()  # type: ignore

            except httpx.TimeoutException as error:
                raise HTTPClientTimeoutError(
                    detail={ERROR_KEY: str(error)},  # noqa: WPS204
                )
            except httpx.ConnectError as error:
                raise HTTPClientConnectionError(
                    detail={ERROR_KEY: str(error)},
                )
            except httpx.HTTPStatusError as error:
                raise HTTPClientResponseError(
                    message=f'Ошибка {error.response.status_code}',
                    status_code=error.response.status_code,
                    detail={
                        'error': str(error),
                        'response_json': error.response.json(),
                    },
                )
            except httpx.HTTPError as error:
                raise HTTPClientError(
                    message='Неизвестная HTTP ошибка',
                    detail={ERROR_KEY: str(error)},
                )

    async def get(self, url: str, **kwargs: Any) -> Dict[str, Any]:  # noqa: C901, WPS238
        """
        Выполнить GET запрос.

        Args:
            url: URL для запроса
            **kwargs: Дополнительные параметры запроса (например, params, headers и т.д.)

        Returns:
            Dict[str, Any]: Ответ от сервера в формате JSON

        Raises:
            HTTPClientTimeoutError: При таймауте
            HTTPClientConnectionError: При ошибке соединения
            HTTPClientResponseError: При ошибочном статусе ответа
            HTTPClientError: При других HTTP ошибках
        """
        async with self.get_httpx_client() as client:
            try:  # noqa: WPS225, WPS229
                response = await client.get(url, **kwargs)
                response.raise_for_status()
                return response.json()  # type: ignore
            except httpx.TimeoutException as error:
                raise HTTPClientTimeoutError(
                    detail={ERROR_KEY: str(error)},
                )
            except httpx.ConnectError as error:
                raise HTTPClientConnectionError(
                    detail={ERROR_KEY: str(error)},
                )
            except httpx.HTTPStatusError as error:
                raise HTTPClientResponseError(
                    message=f'Ошибка {error.response.status_code}',
                    status_code=error.response.status_code,
                    detail={
                        ERROR_KEY: str(error),
                        'response_json': error.response.json(),
                    },
                )
            except httpx.HTTPError as error:
                raise HTTPClientError(
                    message='Неизвестная HTTP ошибка',
                    detail={ERROR_KEY: str(error)},
                )
