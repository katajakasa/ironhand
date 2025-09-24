import structlog
from aiohttp import web

from .config import read_config
from .routes import create_app


async def app() -> web.Application:
    structlog.configure()
    return create_app(read_config())
