from typing import List, Literal, Optional

from pydantic import BaseModel, field_validator

from app.enums import Action


class IncomingMessageDTO(BaseModel):
    """
    DTO для входящих сообщений от клиента.
    """
    request_id: int
    action: Action
    tickers: str
    user_id: int

    @field_validator('tickers')
    @classmethod
    def non_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('tickers must be a non-empty comma-separated string')
        return v


class OutgoingAckDTO(BaseModel):
    """
    DTO для ответов клиенту.
    """
    request_id: int
    status: Literal['ok', 'error']
    action: Action
    user_id: int
    tickers: List[str]
    error: Optional[str] = None
