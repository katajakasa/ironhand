import argparse

import structlog
from aiohttp import web

from ironhand import create_app
from ironhand.access_log import AccessLogger
from ironhand.config import read_config

log = structlog.get_logger(__name__)


def get_args():
    parser = argparse.ArgumentParser(
        prog="ironhand", description="Civilization VI webhook server"
    )
    parser.add_argument(
        "-P", "--port", type=int, default=5089, help="Port to listen on"
    )
    parser.add_argument("-H", "--host", default="127.0.0.1", help="Host to listen on")
    return parser.parse_args()


def main() -> None:
    structlog.configure()
    config = read_config()
    args = get_args()
    app = create_app(config)
    log.info("Listening on %s:%d", args.host, args.port)
    web.run_app(
        app, host=args.host, port=args.port, access_log_class=AccessLogger, print=None
    )


if __name__ == "__main__":
    main()
