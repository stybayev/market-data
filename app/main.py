
from fastapi import FastAPI
from polygon import WebSocketClient
from polygon.websocket.models import WebSocketMessage, Feed, Market
import asyncio
from aiokafka import AIOKafkaProducer
import asyncio


app = FastAPI()

client = WebSocketClient(
    api_key="fmZjlZmcRcp77Y8JMyDnTwapp6ycTh5B",
    feed=Feed.Delayed,
    market=Market.Stocks
)

client.subscribe("Q.AAPL")  # Пример подписки


async def send_one():
    producer = AIOKafkaProducer(bootstrap_servers='localhost:9092')
    # Get cluster layout and initial topic/partition leadership information
    await producer.start()
    try:
        # Produce message
        await producer.send_and_wait("messages", b"Super message")
    finally:
        # Wait for all pending messages to be delivered or expire.
        await producer.stop()

@app.on_event("startup")
async def start_ws():
    # asyncio.get_event_loop().create_task(client.connect(handle_msg))
    asyncio.get_event_loop().create_task(send_one())

