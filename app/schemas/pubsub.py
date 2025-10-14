from pydantic import BaseModel, ConfigDict, field_validator

from app.enums import Action


class SubscriptionCommandDTO(BaseModel):
    """DTO для команды управления подписками, отправляемой в Redis Pub/Sub."""

    model_config = ConfigDict(extra='allow')

    op: Action
    user_id: int
    tickers: list[str]

    @field_validator('tickers')
    @classmethod
    def ensure_non_empty(cls, value: list[str]) -> list[str]:
        if not value:
            raise ValueError('tickers must be a non-empty list')
        if any(not ticker for ticker in value):
            raise ValueError('tickers must not contain empty strings')
        return value
