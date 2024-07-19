import os
import discord

from dotenv import load_dotenv
from constants import *
from components import MyBot

from argparse import ArgumentParser
from utils import utils

async def main():
    load_dotenv()

    bot = MyBot(command_prefix="$", activity_name="Blockchain", tree_cls=MyCommandTree)

    parser = ArgumentParser(
        usage="python3 main.py [-t | --test]",
        description="Discord bot for providing information about the cryptocurrencies",
        allow_abbrev=False,
    )

    parser.add_argument(
        "-t",
        "--test",
        action="stor_true",
        help="Providing console log instead of file log",
    )
    args = parser.parse_args()
    if args.test:
        discord.utils.setup_logging()
    else:
        utils.setup_file_logging()

    TOKEN = os.getenv("TOKEN")
    await bot.start(TOKEN)
