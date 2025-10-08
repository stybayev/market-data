from typing import List, Literal, Optional

from pydantic import BaseModel, field_validator, ValidationError

Action = Literal["subscribe", "unsubscribe", "set"]


class IncomingMessageDTO(BaseModel):
    request_id: int
    action: Action
    tickers: str
    user_id: int

    @field_validator("tickers")
    @classmethod
    def non_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("tickers must be a non-empty comma-separated string")
        return v


class OutgoingAckDTO(BaseModel):
    request_id: int
    status: Literal["ok", "error"]
    action: Action
    user_id: int
    tickers: List[str]
    error: Optional[str] = None
