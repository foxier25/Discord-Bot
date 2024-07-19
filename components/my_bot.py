import logging
from pkgutil import iter_modules

from discord import Intents, Activity, ActivityType, Status
from discord.ext import commands
from discord.ext.commands import Context, CommandError
from discord.app_commands import CommandTree


class MyBot(commands.Bot):
    def __init__(
        self, command_prefix: str, activity_name: str, tree_cls: CommandTree
    ) -> None:
        intents = Intents.all()
        activity = Activity(name=activity_name, type=ActivityType.watching)
        super().__init__(
            command_prefix=command_prefix,
            tree_cls=tree_cls,
            intents=intents,
            activity=activity,
            status=Status.online,
        )
