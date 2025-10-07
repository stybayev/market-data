"""Модуль для настройки зависимостей FastAPI приложения.

Предоставляет функционал для регистрации зависимостей в приложении FastAPI,
используя контейнер зависимостей или пользовательский маппер.
"""

import logging
from typing import Any, Callable

from fastapi import FastAPI

from app.dependencies.registrator import dependencies_container


def setup_dependencies(app: FastAPI, mapper: dict[Any, Callable] | None = None) -> None:  # type: ignore  # noqa: E501, WPS210
    """Настраивает зависимости для FastAPI приложения.

    Args:
        app: Экземпляр FastAPI приложения
        mapper: Словарь с маппингом зависимостей. Если не указан,
               используется стандартный контейнер зависимостей
    """
    dependency_mapper = mapper if mapper is not None else dependencies_container

    for interface_cls, dependency_impl in dependency_mapper.items():
        app.dependency_overrides[interface_cls] = dependency_impl

    pretty = {
        f'{iface.__module__}.{iface.__qualname__}':
            getattr(resolved, '__name__', repr(resolved))
        for iface, resolved in app.dependency_overrides.items()
    }
    logging.info('Dependencies mapping: %s', pretty)  # noqa: WPS323
