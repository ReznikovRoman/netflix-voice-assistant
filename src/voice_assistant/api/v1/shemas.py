from pydantic import BaseModel


class Nlu(BaseModel):
    tokens: list
    intents: dict


class RequestField(BaseModel):
    command: str
    original_utterance: str
    nlu: Nlu


class AliceRequest(BaseModel):
    meta: dict
    request: RequestField
    session: dict
    version: str


class AliceResponse(BaseModel):
    meta: dict
    response: dict
    session: dict
    version: str
