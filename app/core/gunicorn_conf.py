"""
Конфигурационный модуль Gunicorn.

Этот модуль предоставляет настройки для запуска Gunicorn с использованием
переменных окружения и динамического определения параметров.
"""

import json
import logging
import multiprocessing

from pydantic.v1 import BaseSettings


class GunicornSettings(BaseSettings):
    """
    Класс для управления настройками Gunicorn.

    Атрибуты:
        workers_per_core (float): Количество воркеров на одно ядро.
        web_concurrency (int): Пользовательское количество воркеров.
        host (str): Хост, на котором запускается приложение.
        port (int): Порт для запуска приложения.
        bind (str): Полный адрес привязки.
        log_level (str): Уровень логирования.
        keepalive (int): Время поддержания соединения (в секундах).
        errorlog (str): Лог ошибок.
    """

    workers_per_core: float = 1.0
    web_concurrency: int | None = None
    host: str = '0.0.0.0'  # noqa: S104
    port: int = 8080
    bind: str | None = None
    log_level: str = 'info'
    keepalive: int = 120
    errorlog: str = '-'

    class Config:
        """Конфигурация для Pydantic."""

        env_file = '.env'
        env_prefix = 'AUTH_API_GUNICORN_'

    @property
    def bind_address(self) -> str:
        """
        Получение адреса привязки.

        Returns:
            str: Адрес в формате host:port.
        """
        if self.bind:
            return self.bind
        return f'{self.host}:{self.port}'  # noqa: WPS305

    @property
    def worker_count(self) -> int:
        """
        Расчёт количества воркеров.

        Returns:
            int: Количество воркеров, определённое динамически или заданное пользователем.
        """
        cores = multiprocessing.cpu_count()
        default_web_concurrency = self.workers_per_core * cores
        if self.web_concurrency:
            return max(self.web_concurrency, 1)
        return max(int(default_web_concurrency), 2)


# Создаём экземпляр класса GunicornSettings
gunicorn_settings = GunicornSettings()

# Конфигурационные переменные Gunicorn
loglevel = gunicorn_settings.log_level
workers = gunicorn_settings.worker_count
bind = gunicorn_settings.bind_address
keepalive = gunicorn_settings.keepalive
errorlog = gunicorn_settings.errorlog

# Для логирования и отладки
log_data = {
    'loglevel': loglevel,
    'workers': workers,
    'bind': bind,
    'workers_per_core': gunicorn_settings.workers_per_core,
    'host': gunicorn_settings.host,
    'port': gunicorn_settings.port,
}
logging.info(json.dumps(log_data))
