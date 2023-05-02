import asyncio
import os
import redis
import requests

# from sanic.exceptions import ConnectionClosed
from sanic import Request, Websocket
import websockets
from sanic.exceptions import WebsocketClosed
from ..tools import InMemory
from sanic.exceptions import WebsocketClosed

__all__ = ["online"]
connected = []

cache_key = "online:connected"


async def update_online():
    in_memory = InMemory()

    while True:
        connected = in_memory.get(cache_key)
        await asyncio.sleep(0.1)


# coroutine that will start another coroutine after a delay in seconds
async def delay(seconds):
    # suspend for a time limit in seconds
    await asyncio.sleep(seconds)
    # execute the other coroutine
    connected.append("hello!")


async def producer_handler(ws: Websocket):
    data = "hello!"
    in_memory = InMemory()

    # connected = in_memory.get(cache_key)
    prev_connected = set(connected)
    response = []

    # task = asyncio.create_task(delay(2))
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(delay(10))
    # loop.close()

    # n = 0

    while True:
        next_connected = set(connected)

        disconnected = prev_connected.difference(next_connected)
        for id in disconnected:
            response.append(
                {
                    "status": "disconected",
                    "id": id,
                }
            )

        connected = next_connected.difference(prev_connected)
        for id in connected:
            response.append(
                {
                    "status": "conected",
                    "id": id,
                }
            )

        if response:
            # in_memory.set(cache_key, next_connected)
            prev_connected = next_connected
            return response


def get_token_info(token):
    url = os.getenv("4GEEKS_URL")
    response = requests.get(
        f"{url}/v1/authenticate/token", headers={"Authorization": f"Bearer {token}"}
    )
    if response.status_code != 200:
        return None

    return response.json()


async def online(request: Request, ws: Websocket):
    get_token_info(request.token)
    while True:
        data = await producer_handler(ws)
        try:
            for datum in data:
                await ws.send(datum)

        except WebsocketClosed:
            break
