"""Модуль для кастомных backoff-декораторов."""
import asyncio
import logging
import secrets
from functools import wraps
from typing import Callable, Any

logger = logging.getLogger(__name__)


def backoff(  # noqa: C901, WPS231
    start_sleep_time: float = 0.1,
    factor: float = 2,
    border_sleep_time: float = 10,
    max_retries: int = 5,
    jitter: bool = True,
    exceptions: tuple = (Exception,),  # type: ignore
    raise_on_fail: bool = True,
) -> Callable[..., Any]:
    """
    Кастомный backoff-декоратор с экспоненциальной задержкой и jitter'ом.

    Args:
        start_sleep_time: начальное время ожидания
        factor: во сколько раз увеличивать задержку
        border_sleep_time: максимальное время ожидания
        max_retries: сколько попыток максимум
        jitter: добавлять ли случайный разброс к задержке
        exceptions: кортеж исключений, на которые реагировать
        raise_on_fail: флаг, определяющий поведение при превышении лимита попыток

    Returns:
        Callable: Обернутая функция, которая будет повторно вызываться при указанных исключениях.

    Raises:
        RuntimeError: Если все попытки исчерпаны и `raise_on_fail=True`.  # noqa: DAR402
    """

    def func_wrapper(func: Callable[..., Any]) -> Any:  # noqa: WPS430, WPS231
        @wraps(func)
        async def inner(*args: Any, **kwargs: Any) -> Any:  # noqa: WPS430
            retries = 0
            delay = start_sleep_time

            while retries < max_retries:
                try:
                    return await func(*args, **kwargs)
                except exceptions as err:
                    retries += 1

                    # Расчёт времени с jitter
                    sleep_time = min(delay, border_sleep_time)
                    if jitter:
                        sleep_time = secrets.SystemRandom().uniform(  # noqa: WPS220
                            sleep_time / 2,
                            sleep_time,
                        )

                    logger.warning(
                        f'[backoff] Ошибка: {err}. Попытка {retries}/{max_retries}. '
                        f'Ждём {sleep_time:.2f} сек перед повтором...',
                    )

                    await asyncio.sleep(sleep_time)
                    delay *= factor  # Увеличиваем задержку экспоненциально

            logger.error(
                f'[backoff] Превышено число попыток ({max_retries}). Функция не выполнена.',
            )

            if raise_on_fail:
                raise RuntimeError(
                    f'Backoff: превышено максимальное количество повторных попыток ({max_retries})'
                )

            return None

        return inner

    return func_wrapper
