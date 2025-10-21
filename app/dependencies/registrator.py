"""Модуль предоставляет функционал для регистрации фабрик зависимостей.

Этот модуль содержит контейнер зависимостей и декоратор для регистрации
фабрик, используемых для создания экземпляров классов или вызова функций.
"""

from typing import Callable, Type

dependencies_container: dict[Type | Callable, Callable] = {}


def add_factory_to_mapper(class_: Type | Callable) -> Callable[[Callable], Callable]:
    """Регистрирует фабричную функцию для указанного класса или функции.

    Args:
        class_: Класс или функция, для которой регистрируется фабрика.

    Returns:
        Декоратор, который добавляет фабричную функцию в контейнер зависимостей.
    """
    def decorator(factory: Callable) -> Callable:
        dependencies_container[class_] = factory
        return factory
    return decorator
