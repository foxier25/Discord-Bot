import os;
from discord.ext import commands
import requests

client = commands.Bot(command_prefix='!')

@client.event

async def on_ready():
    print(f'You have logged in as {client.user}')

