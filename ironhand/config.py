import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Final

import structlog

CONFIG_PATHS: Final[list[Path]] = [
    Path("./ironhand.toml").resolve(),
    Path("~/.local/share/ironhand/ironhand.toml").resolve(),
    Path("~/.ironhand/ironhand.toml").resolve(),
    Path("/etc/ironhand/ironhand.toml").resolve(),
]

log = structlog.get_logger(__name__)


@dataclass(frozen=True, slots=True)
class Config:
    path: str = "/webhooks/civ6"
    user_mapping: dict[str, str] = field(default_factory=dict)


def read_config():
    for config_file in CONFIG_PATHS:
        if config_file.is_file():
            log.info("Found config file at %s", config_file)
            return Config(**tomllib.loads(config_file.read_text()))
    return Config()
