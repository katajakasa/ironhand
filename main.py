import json
import logging

from aiohttp import web

log = logging.getLogger(__name__)

async def webhook(request: web.Request) -> web.Response:
    try:
        body = await request.json()
    except json.decoder.JSONDecodeError:
        return web.Response(status=400)

    log.error("Received headers: %s", request.headers)
    log.error("Received message: %s", body)
    return web.Response(text="OK", status=200)


async def create_app() -> web.Application:
    logging.basicConfig(level=logging.INFO)
    app = web.Application()
    app.add_routes([web.post("/webhooks/civ6", webhook)])
    return app


def main() -> None:
    web.run_app(create_app())


if __name__ == "__main__":
    main()
