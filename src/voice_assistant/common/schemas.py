from orjson import orjson
from pydantic import BaseModel


def orjson_dumps(value, *, default):
    return orjson.dumps(value, default=default).decode()


class BaseOrjsonSchema(BaseModel):
    """Базовая модель Pydantic с использованием orjson."""

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
