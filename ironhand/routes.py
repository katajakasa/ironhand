import json
import structlog

from aiohttp import web

from ironhand.config import Config
from ironhand.error_handler import error_middleware

CONFIG_KEY = web.AppKey("config")


log = structlog.getLogger(__name__)


async def health(_: web.Request) -> web.Response:
    return web.Response(text="OK", status=200)


async def webhook(request: web.Request) -> web.Response:
    try:
        body = await request.json()
    except json.decoder.JSONDecodeError:
        log.exception("Failed to decode JSON body")
        return web.Response(status=400)

    log.error("Received headers: %s", request.headers)
    log.error("Received message: %s", body)
    return web.Response(text="OK", status=200)


def create_app(config: Config) -> web.Application:
    app = web.Application(middlewares=[error_middleware])
    app[CONFIG_KEY] = config
    app.add_routes([web.post(config.path, webhook)])
    app.add_routes([web.get(config.path, health)])
    return app
