
from fastapi import FastAPI
from polygon import WebSocketClient
from polygon.websocket.models import WebSocketMessage, Feed, Market
import asyncio
from aiokafka import AIOKafkaProducer
import asyncio


app = FastAPI()

# client = WebSocketClient(
#     api_key="fmZjlZmcRcp77Y8JMyDnTwapp6ycTh5B",
#     feed=Feed.Delayed,
#     market=Market.Stocks
# )
#
# client.subscribe("Q.AAPL")  # Пример подписки

bootstrap_servers = '3.78.215.40:9094,3.78.215.40:9095,3.78.215.40:9096'
async def send_one():
    producer = AIOKafkaProducer(bootstrap_servers=bootstrap_servers)
    await producer.start()
    try:
        # Produce message
        await producer.send_and_wait(topic="messages", value=b"OO sheshen", key=b'python-message')
    finally:
        # Wait for all pending messages to be delivered or expire.
        await producer.stop()

@app.on_event("startup")
async def start_ws():
    # asyncio.get_event_loop().create_task(client.connect(handle_msg))
    asyncio.get_event_loop().create_task(send_one())

