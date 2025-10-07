"""Модуль для кастомных декораторов для перехвата HTTP ошибок."""
import logging
from functools import wraps
from typing import Callable, ParamSpec, TypeVar, Awaitable

from httpx import HTTPStatusError, Response

from app.enums.common_enums import HTTPStatusRange

logger = logging.getLogger(__name__)


Params = ParamSpec('Params')
ReturnType = TypeVar('ReturnType')


def handle_client_errors(  # noqa: C901
    func: Callable[Params, Awaitable[ReturnType]],
) -> Callable[Params, Awaitable[ReturnType | Response]]:
    """
    Декоратор для перехвата HTTP ошибок клиента (статусы 4xx).

    Если вызываемая функция выбрасывает исключение `HTTPStatusError` с кодом 400–499,
    декоратор логирует предупреждение и возвращает полный `httpx.Response`,
    чтобы вызывающий код мог обработать его вручную.

    Идеально подходит для сценариев, где ошибки 4xx не должны триггерить retry/backoff-логику.

    Args:
        func (Callable): Оборачиваемая функция, совершающая HTTP-запрос через httpx.

    Returns:
        Response | Any: Ответ от сервера в случае 4xx ошибки, либо результат вызова функции.
    """
    @wraps(func)
    async def wrapper(*args: Params.args, **kwargs: Params.kwargs) -> ReturnType | Response:
        try:
            return await func(*args, **kwargs)

        except HTTPStatusError as exc:
            status_code = exc.response.status_code

            if HTTPStatusRange.client_error_min.value <= status_code < HTTPStatusRange.client_error_max.value:  # noqa: E501
                logger.warning(f'Client error {status_code}: {exc.response.text}')
                return exc.response

            raise

    return wrapper
