import os
import discord

from dotenv import load_dotenv
from constants import *
from components import MyBot

async def main():
    load_dotenv()

    bot = MyBot(command_prefix="$", activity_name="Blockchain", tree_cls=MyCommandTree)
