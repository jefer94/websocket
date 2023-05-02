import asyncio

# from sanic.exceptions import ConnectionClosed
from sanic import Request, Websocket
import websockets
from sanic.exceptions import WebsocketClosed

__all__ = ["example"]
connected = []


async def consumer_handler(ws: Websocket):
    while True:
        try:
            data = await ws.recv()
            print(data)

        except WebsocketClosed:
            break


async def producer_handler(ws: Websocket):
    while True:
        try:
            data = "hello!"
            await ws.send(data)
            await asyncio.sleep(1)

        except WebsocketClosed:
            break


async def example(request: Request, ws: Websocket):
    while True:
        consumer_task = asyncio.create_task(consumer_handler(ws))
        producer_task = asyncio.create_task(producer_handler(ws))

        done, pending = await asyncio.wait(
            [consumer_task, producer_task],
            return_when=asyncio.FIRST_COMPLETED,
        )

        for task in pending:
            task.cancel()
