# #!/usr/bin/env python
from __future__ import absolute_import

import os
from sanic import Blueprint, Sanic

# from sanic_motor import BaseModel
# from motor.motor_asyncio import AsyncIOMotorClient

# from .. import handlers
from . import websocket
from . import api
from dotenv import load_dotenv

load_dotenv()

app = Sanic("Accounts")
app.config.CORS_ORIGINS = "*"

from sanic import Request, Websocket

app.add_websocket_route(websocket.online, "/online")


# settings = dict(
#     # MOTOR_URI=os.environ["MONGODB_URL"],
#     MOTOR_URI="mongodb://root:example@localhost:27017/accounts",
#     LOGO=None,
# )
# app.config.update(settings)

# BaseModel.init_app(app)

# app.static("/", "./accounts-client/dist")


# @app.on_request
# async def run_before_handler(request):
#     request.ctx.client = AsyncIOMotorClient("mongodb://root:example@localhost:27017")


v1 = Blueprint("v1", version=1)
v1.add_route(api.webhook, "/webhook", methods=["POST"])

app.blueprint(v1)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="127.0.0.1", port=port, debug=True)
