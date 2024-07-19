import logging
from aiohttp import client_exceptions

from discord import Interaction
from discord.app_commands import CommandTree, AppCommandError, CommandInvokeError


async def on_error(self, interaction: Interaction, error: AppCommandError) -> None:
    logging.exception(error)

    if isinstance(error, CommandInvokeError):
        error = error.original