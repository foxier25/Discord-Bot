from aiohttp import ClientSession
from typing import List
import datetime as dt
from io import BytesIO
from plotly.graph_objects import Figure, Candlestick

from discord import app_commands
from discord import Interaction, Embed, Colour, File
from discord.ext.commands import Cog, Bot

from constants import *
from utils import utils
from utils import errors
    

class Info(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
    
    
    @app_commands.command(name='info', description='Basic information about the coin')
    @app_commands.describe(
        coin_symbol='Coin symbol'
    )