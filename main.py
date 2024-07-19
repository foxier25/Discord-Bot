import os
from discord.ext import commands, tasks
import discord
import requests
from keep_alive import keep_alive
from replit import db

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix="!", intents=intents)


@client.event
async def on_ready():
    print(f"You have logged in as {client.user}")


@tasks.loop(minutes=60)
async def update_database():
    await client.wait_until_ready()  # without this it won't work
    print("price-check-1h")

    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd"
    data = requests.get(url).json()
    symbols = []

    text_positive = "Next cryptocurrencies are up at least 10% in past hour:\n"
    positive = False

    text_negative = "Next cryptocurrencies are down at least 10% in past hour:\n"
    negative = False

    channel = client.get_channel(901822736693870623)  # channel price-alerts

    for i in range(len(data)):
        current_price = data[i]["current_price"]
        symbol = data[i]["symbol"]

        if symbol not in db.keys():
            price_1h_ago = current_price
            percentage = 0
        else:
            price_1h_ago = db[symbol]
            percentage = ((float(current_price) / float(price_1h_ago)) - 1) * 100

        db[symbol] = current_price
        symbols.append(symbol)

        if percentage > 10:
            positive = True
            text_positive += symbol + " +" + str(round(percentage, 2)) + "%\n"

        if percentage < -10:
            negative = True
            text_negative += symbol + " " + str(round(percentage, 2)) + "%\n"

    if positive:
        print(text_positive)
        await channel.send(text_positive)

    if negative:
        print(text_negative)
        await channel.send(text_negative)

    for key in db.keys():
        if key not in symbols:
            del db[key]


update_database.start()


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


@client.command()
async def ath(ctx, symbol):
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd"
    data = requests.get(url).json()
    not_found = True

    for crypto in data:
        if symbol.lower() == crypto["symbol"]:
            not_found = False
            ath = crypto["ath"]
            ath_date = crypto["ath_date"]
            day = ath_date[8] + ath_date[9]
            month = ath_date[5] + ath_date[6]
            year = ath_date[0] + ath_date[1] + ath_date[2] + ath_date[3]
            ath_percentage_down = crypto["ath_change_percentage"]
            print(
                "ATH for {} is at {:,}, on {}.{}.{}, which is {:.2f}% down".format(
                    symbol.upper(), ath, day, month, year, ath_percentage_down
                )
            )
            await ctx.send(
                "ATH for {} is at {:,}, on {}.{}.{}, which is {:.2f}% down".format(
                    symbol.upper(), ath, day, month, year, ath_percentage_down
                )
            )
    if not_found:
        await ctx.send("Either you sent wrong symbol or currency is not in top 100")


@client.command()
async def top(ctx, *args):
    if len(args) != 1:
        await ctx.send("Command !top is not used properly. (!top n)")
        return
    n = int(args[0])
    if n < 1 or n > 50:
        await ctx.send("Number of coins must be between 1 and 50. (!top n, n ∈ [0,50])")
        return

    respond_symbols = ""
    respond_prices = ""
    respond_market_cap = ""

    data = requests.get(COINGECKO_COINS_URL).json()

    i = 0
    for crypto in data:
        if i == n:
            break
        respond_symbols += str(crypto["symbol"]).upper() + "\n"
        respond_prices += "{:,}".format(crypto["current_price"]) + "\n"
        respond_market_cap += "{:,}".format(crypto["market_cap"]) + "\n"
        i += 1

    today = date.today()
    d2 = today.strftime("%B/%d/%Y")
    now = datetime.now()
    time_now = now.strftime("%H:%M:%S")
    date_now = d2 + " at " + time_now

    my_embed = discord.Embed(
        title="More info",
        url="https://www.coingecko.com/en",
        colour=discord.Colour.purple(),
    )
    my_embed.set_author(
        name="Top" + str(n) + " coins",
        url="",
        icon_url="https://png.pngtree.com/png-clipart/20210310/original/pngtree-3d-trophy-with-first-second-third-winner-png-image_5931060.jpg",
    )
    my_embed.add_field(name="Symbol", value=respond_symbols, inline=True)
    my_embed.add_field(name="Price", value=respond_prices, inline=True)
    my_embed.add_field(name="Market cap", value=respond_market_cap, inline=True)
    my_embed.add_field(name='Down(%)', value='{:,.2f}'.format(ath_percentage_down) + '%', inline=True)
    my_embed.set_footer(text="Source: coingecko.com ☛ " + date_now)

    await ctx.send(embed=my_embed)


# Help command for commands and tasks
@client.command()
async def botinfo(ctx, *args):
    if len(args) != 0:
        await ctx.send("Command !botinfo is not used properly. (!botinfo)")
        return

    commands = "!price symbol\n!bought symbol price\n!daychange symbol\n!ath symbol\n!info symbol\n!top n"
    examples = (
        "!price btc\n!bought btc 21000\n!daychange btc\n!ath btc\n!info btc\n!top 10"
    )

    today = date.today()
    d2 = today.strftime("%B/%d/%Y")
    now = datetime.now()
    time_now = now.strftime("%H:%M:%S")
    date_now = d2 + " at " + time_now

    my_embed = discord.Embed(colour=discord.Colour.purple())
    my_embed.set_author(
        name="Commands that i use",
        icon_url="https://e7.pngegg.com/pngimages/305/948/png-clipart-computer-icons-exclamation-mark-others-miscellaneous-angle-thumbnail.png",
    )
    my_embed.add_field(name="Command", value=commands, inline=True)
    my_embed.add_field(name="Example", value=examples, inline=True)
    my_embed.set_footer(text="Source: coingecko.com ☛ " + date_now)

    await ctx.send(embed=my_embed)


TOKEN = os.environ["TOKEN_SECRET"]

keep_alive()
client.run(TOKEN)
