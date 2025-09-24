from aiohttp import web
from aiohttp.typedefs import Handler
from aiohttp.web_middlewares import middleware
from aiohttp.web import Request, Response
import structlog

log = structlog.get_logger(__name__)


@middleware
async def error_middleware(request: Request, handler: Handler):
    try:
        return await handler(request)
    except web.HTTPException:
        raise
    except Exception as e:
        log.exception("Error while processing request: %s", e)
        return Response(
            text="Internal Server Error",
            status=500,
        )
