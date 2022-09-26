from typing import Any, Iterator
from zoneinfo import ZoneInfo

TZ_MOSCOW = ZoneInfo("Europe/Moscow")

sentinel: Any = object()


def resolve_callables(mapping: dict) -> Iterator[tuple[Any, Any]]:
    """Генерация пар ключ-значение из `mapping`, где значения могут быть callable объектами."""
    for key, value in mapping.items():
        yield key, value() if callable(value) else value
