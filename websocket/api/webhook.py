from sanic import json, Request


async def webhook(request: Request):
    request.json
    return json({})
