import asyncio
from typing import Any, Coroutine, Iterator
from zoneinfo import ZoneInfo

TZ_MOSCOW = ZoneInfo("Europe/Moscow")

sentinel: Any = object()


def delay_tasks(*tasks: Coroutine) -> None:
    """Вспомогательная функция для запуска задач в фоне.

    Для надежной работы нужно сохранять ссылку на функцию.
    https://docs.python.org/3/library/asyncio-task.html#creating-tasks
    """
    background_tasks = set()
    for _task in tasks:
        task = asyncio.create_task(_task)
        background_tasks.add(task)
        task.add_done_callback(background_tasks.discard)


def resolve_callables(mapping: dict) -> Iterator[tuple[Any, Any]]:
    """Генерация пар ключ-значение из `mapping`, где значения могут быть callable объектами."""
    for key, value in mapping.items():
        yield key, value() if callable(value) else value
