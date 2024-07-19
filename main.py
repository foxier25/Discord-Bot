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


async def bought(ctx, symbol, bought_price):
    bought_price_real = bought_price.replace(",", ".")
    print(f"You bought {symbol} at price of {bought_price_real}")

    if float(bought_price_real) < 0:
        await ctx.send("The price is not correct, please send us correct price")
        return

    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd"
    data = requests.get(url).json()
    not_found = True

    for crypto in data:
        if symbol.lower() == crypto["symbol"]:
            not_found = False
            current_price = crypto["current_price"]
            percentage = ((float(current_price) / float(bought_price_real)) - 1) * 100

            if percentage > 0:
                print("You are currently {:.2f}% in profit".format(percentage))
                await ctx.send("You are currently {:.2f}% in profit".format(percentage))
            else:
                print("You are currently {:.2f}% in loss".format(percentage))
                await ctx.send("You are currently {:.2f}% in loss".format(percentage))

    if not_found:
        await ctx.send("Either you sent wrong symbol or currency is not in top 100")


@client.command()
async def daychange(ctx, symbol):
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd"
    data = requests.get(url).json()
    not_found = True

    for crypto in data:
        if symbol.lower() == crypto["symbol"]:
            not_found = False
            day_change = crypto["price_change_24h"]
            day_change_percentage = crypto["price_change_percentage_24h"]
            print(
                "24h change for {} is {}, which is {}%".format(
                    symbol, day_change, day_change_percentage
                )
            )
            await ctx.send(
                "24h change for {} is {}, which is {}%".format(
                    symbol, day_change, day_change_percentage
                )
            )

    if not_found:
        await ctx.send("Either you sent wrong symbol or currency is not in top 100")


TOKEN = os.environ["TOKEN_SECRET"]

client.run(TOKEN)
