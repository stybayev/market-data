import json
import logging
import re
from typing import List

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.schemas.client_ws import IncomingMessageDTO, OutgoingAckDTO
from app.db.redis import publish_subs_command
from app.enums import Action
from app.core.config import settings

router = APIRouter()
logger = logging.getLogger(__name__)

# 'A.TSLA', 'Q.TQQQ' и т.п.
TICKER_RE = re.compile(r'^[A-Z]\.[A-Z0-9]+$', re.ASCII)
WS_MAX_SUBS_PER_USER = settings.ws_max_subs_per_user


def normalize_tickers(raw: str) -> List[str]:
    """
    "A.TSLA, A.ARAV,A.NVDA" -> ['A.TSLA', 'A.ARAV', 'A.NVDA']
    + валидация и дедупликация.
    """

    items = [t.strip().upper() for t in raw.split(',')]
    items = [t for t in items if t]
    bad = [t for t in items if not TICKER_RE.match(t)]
    if bad:
        raise ValueError(f'invalid tickers: {", ".join(bad)}')
    return list(dict.fromkeys(items))  # дедуп с сохранением порядка


@router.websocket('/ws/market-stream')
async def websocket_endpoint(ws: WebSocket):
    """
    Подписка на тикеры, отписка, получение последних цен.
    """
    await ws.accept()
    try:
        while True:
            raw = await ws.receive_text()
            print(raw)
            try:
                data = None
                data = json.loads(raw)
                msg = IncomingMessageDTO(**data)
                tickers = normalize_tickers(msg.tickers)

                if len(tickers) > WS_MAX_SUBS_PER_USER:
                    raise ValueError(f'too many tickers: {len(tickers)} > {WS_MAX_SUBS_PER_USER}')

                await publish_subs_command(msg.action, msg.user_id, tickers)

                ack = OutgoingAckDTO(
                    request_id=msg.request_id,
                    status='ok',
                    action=msg.action,
                    user_id=msg.user_id,
                    tickers=tickers,
                )
                await ws.send_text(
                    json.dumps(
                        ack.model_dump(exclude_none=True),
                        separators=(',', ':'),
                        ensure_ascii=False,
                    )
                )

            except (json.JSONDecodeError, TypeError):
                await ws.send_text(json.dumps(
                    {
                        'request_id': 0,
                        'status': 'error',
                        'action': Action.SUBSCRIBE,
                        'user_id': 0,
                        'tickers': [],
                        'error': 'invalid json',
                    },
                    separators=(',', ':'),
                    ensure_ascii=False,
                ))
            except Exception as e:  # pydantic ValidationError или наш ValueError
                if isinstance(data, dict):
                    req_id_raw = data.get('request_id', 0)
                    action_raw = data.get('action', Action.SUBSCRIBE)
                    user_id_raw = data.get('user_id', 0)
                else:
                    req_id_raw, action_raw, user_id_raw = 0, Action.SUBSCRIBE, 0

                try:
                    req_id = int(req_id_raw)
                except Exception:
                    req_id = 0

                try:
                    action = Action(action_raw)
                except Exception:
                    action = Action.SUBSCRIBE

                try:
                    user_id = int(user_id_raw)
                except Exception:
                    user_id = 0

                err = OutgoingAckDTO(
                    request_id=req_id,
                    status='error',
                    action=action,
                    user_id=user_id,
                    tickers=[],
                    error=str(e),
                )
                await ws.send_text(
                    json.dumps(
                        err.model_dump(exclude_none=True),
                        separators=(',', ':'),
                        ensure_ascii=False,
                    )
                )
    except WebSocketDisconnect:
        logger.info('client disconnected')
