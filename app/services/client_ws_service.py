"""Сервисы для обработки сообщений клиентского вебсокета."""

from __future__ import annotations

import json
import re
from typing import Any, Awaitable, Callable

from app.enums import Action, AckStatus
from app.schemas.client_ws import IncomingMessageDTO, OutgoingAckDTO

PublishSubsCallable = Callable[[Action, int, list[str]], Awaitable[None]]

# 'A.TSLA', 'Q.TQQQ' и т.п.
_TICKER_RE = re.compile(r'^[A-Z]\.[A-Z0-9]+$', re.ASCII)


class ClientWebsocketService:
    """Инкапсулирует бизнес-логику обработки команд из вебсокета."""

    def __init__(self, publish_command: PublishSubsCallable, max_subs_per_user: int) -> None:
        self._publish_command = publish_command
        self._max_subs_per_user = max_subs_per_user

    async def process_raw_message(self, raw: str) -> OutgoingAckDTO:
        """Обрабатывает сырое сообщение из вебсокета и возвращает ack."""
        try:
            data = json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            return OutgoingAckDTO(
                request_id=0,
                status=AckStatus.ERROR,
                action=Action.SUBSCRIBE,
                user_id=0,
                tickers=[],
                error='invalid json',
            )

        try:
            msg = IncomingMessageDTO(**data)
            tickers = self._normalize_tickers(msg.tickers)
            self._ensure_limit(tickers)

            await self._publish_command(msg.action, msg.user_id, tickers)

            return OutgoingAckDTO(
                request_id=msg.request_id,
                status=AckStatus.OK,
                action=msg.action,
                user_id=msg.user_id,
                tickers=tickers,
            )
        except Exception as exc:  # noqa: BLE001 - нужно отдать клиенту текст ошибки
            request_id, action, user_id = self._extract_context(data)
            return OutgoingAckDTO(
                request_id=request_id,
                status=AckStatus.ERROR,
                action=action,
                user_id=user_id,
                tickers=[],
                error=str(exc),
            )

    @staticmethod
    def _normalize_tickers(raw: str) -> list[str]:
        items = [ticker.strip().upper() for ticker in raw.split(',')]
        items = [ticker for ticker in items if ticker]
        _validate_tickers(items)
        return list(dict.fromkeys(items))

    def _ensure_limit(self, tickers: list[str]) -> None:
        if len(tickers) > self._max_subs_per_user:
            raise ValueError(f'too many tickers: {len(tickers)} > {self._max_subs_per_user}')

    @staticmethod
    def _extract_context(data: Any) -> tuple[int, Action, int]:
        if not isinstance(data, dict):
            return 0, Action.SUBSCRIBE, 0

        request_raw = data.get('request_id', 0)
        action_raw = data.get('action', Action.SUBSCRIBE)
        user_raw = data.get('user_id', 0)

        try:
            request_id = int(request_raw)
        except Exception:  # noqa: BLE001 - возврат к дефолту
            request_id = 0

        try:
            action = Action(action_raw)
        except Exception:  # noqa: BLE001 - возврат к дефолту
            action = Action.SUBSCRIBE

        try:
            user_id = int(user_raw)
        except Exception:  # noqa: BLE001 - возврат к дефолту
            user_id = 0

        return request_id, action, user_id


def _validate_tickers(tickers: list[str]) -> None:
    bad = [ticker for ticker in tickers if not _TICKER_RE.match(ticker)]
    if bad:
        raise ValueError(f'invalid tickers: {", ".join(bad)}')
