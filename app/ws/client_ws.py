import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException

from schemas.client_ws import IncomingMessageDTO

router = APIRouter()
logger = logging.getLogger(__name__)


@router.websocket("/ws/market-stream")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()

    try:
        while True:
            raw = await ws.receive_text()
            print(raw)

            ack = IncomingMessageDTO(
                request_id=123,
                status="ok",
                action="subscribe",
                user_id=318,
                tickers=["AAPL", "MSFT"],
            )
            await ws.send_text(ack.model_dump_json(separators=(",", ":")))
    except WebSocketDisconnect:
        logger.info("client disconnected")
