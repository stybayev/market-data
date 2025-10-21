import json
import logging

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from app.schemas.client_ws import OutgoingAckDTO
from app.db.redis import publish_subs_command
from app.core.config import settings
from app.dependencies.registrator import add_factory_to_mapper
from app.services import ClientWebsocketService

router = APIRouter()
logger = logging.getLogger(__name__)

WS_MAX_SUBS_PER_USER = settings.ws_max_subs_per_user

@add_factory_to_mapper(ClientWebsocketService)
def get_client_ws_service() -> ClientWebsocketService:
    return ClientWebsocketService(
        publish_command=publish_subs_command,
        max_subs_per_user=WS_MAX_SUBS_PER_USER,
    )


@router.websocket('/ws/market-stream')
async def websocket_endpoint(
    ws: WebSocket,
    service: ClientWebsocketService = Depends(ClientWebsocketService),
):
    """
    Подписка на тикеры, отписка, получение последних цен.
    """
    await ws.accept()
    try:
        while True:
            raw = await ws.receive_text()
            ack: OutgoingAckDTO = await service.process_raw_message(raw)
            await ws.send_text(
                json.dumps(
                    ack.model_dump(exclude_none=True),
                    separators=(',', ':'),
                    ensure_ascii=False,
                )
            )
    except WebSocketDisconnect:
        logger.info('client disconnected')
