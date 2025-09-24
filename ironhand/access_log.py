import structlog
from aiohttp import web
from aiohttp.abc import AbstractAccessLogger

log = structlog.get_logger("aiohttp.access")


class AccessLogger(AbstractAccessLogger):
    def log(self, request: web.Request, response: web.Response, time):
        user_agent = request.headers.get("User-Agent", "unknown")
        log.info(
            f"{request.method} {request.path} in {round(time, 3)} {response.status} (%s)",
            user_agent,
        )
