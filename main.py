import argparse
import json
import logging
import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Final

from aiohttp import web

CONFIG_PATHS: Final[list[Path]] = [
    Path("./ironhand.toml").resolve(),
    Path("~/.local/share/ironhand/ironhand.toml").resolve(),
    Path("~/.ironhand/ironhand.toml").resolve(),
    Path("/etc/ironhand/ironhand.toml").resolve(),
]


@dataclass(frozen=True, slots=True)
class Config:
    user_mapping: dict[str, str] = field(default_factory=dict)


log = logging.getLogger(__name__)


async def webhook(request: web.Request) -> web.Response:
    try:
        body = await request.json()
    except json.decoder.JSONDecodeError:
        log.exception("Failed to decode JSON body")
        return web.Response(status=400)

    log.error("Received headers: %s", request.headers)
    log.error("Received message: %s", body)
    return web.Response(text="OK", status=200)


def read_config():
    for config_file in CONFIG_PATHS:
        if config_file.is_file():
            log.info("Found config file at %s", config_file)
            return Config(**tomllib.loads(config_file.read_text()))
    return Config()


async def create_app() -> web.Application:
    logging.basicConfig(level=logging.INFO)
    config = read_config()
    app = web.Application()
    app.add_routes([web.post("/webhooks/civ6", webhook)])
    return app


def get_args():
    parser = argparse.ArgumentParser(
        prog='ironhand',
        description='Civilization VI webhook server'
    )
    parser.add_argument("-P", "--port", type=int, default=5089, help="Port to listen on")
    parser.add_argument("-H", "--host", default="127.0.0.1", help="Host to listen on")
    return parser.parse_args()


def main() -> None:
    args = get_args()
    web.run_app(create_app(), host=args.host, port=args.port)


if __name__ == "__main__":
    main()
