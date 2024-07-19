import logging
import logging.handlers
from typing import Dict, Union
from aiohttp import ClientSession
import json

from constants import *


def setup_logging() -> None:
    logger = logging.getLogger("")
    logger.setLevel(logging.INFO)

    handler = logging.handlers.RotatingFileHandler(
        filename="discord.log",
        encoding="utf-8",
        maxBytes=32 * 1024 * 1024,
        backupCount=5,
    )

    dt_fmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(
        "[{asctime}] [{levelname:<8}] {name}: {message}", dt_fmt, style="{"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)


async def fetch_url(session: ClientSession, url: str) -> Union[Dict, None]:
    async with session.get(url) as response:
        if response.status == 404:
            return None

        return await response.json()
