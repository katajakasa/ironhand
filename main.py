import logging

from aiohttp import web


async def webhook(request: web.Request) -> web.Response:
    print(await request.json())
    print(request.headers)
    return web.Response(text="OK", status=200)


async def create_app() -> web.Application:
    logging.basicConfig(level=logging.INFO)
    app = web.Application()
    app.add_routes([web.post("/webhook", webhook)])
    return app


def main() -> None:
    web.run_app(create_app())


if __name__ == "__main__":
    main()
