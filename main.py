import os
from discord.ext import commands

import requests

client = commands.Bot(command_prefix="!")


@client.event
async def on_ready():
    print(f"You have logged in as {client.user}")


@client.command()
async def price(ctx, symbol):
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd"
    data = requests.get(url).json()
    not_found = True

    for crypto in data:
        if symbol.lower() == crypto["symbol"]:
            not_found = False
            current_price = crypto["current_price"]
            print("Current price of {} is {:,}".format(symbol.upper(), current_price))
            await ctx.send(
                "Current price of {} is {:,}".format(symbol.uppper(), current_price)
            )
    if not_found:
        await ctx.send("Either you sent wrong symbol or currency is not in top 100")
