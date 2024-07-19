from discord import Interaction, Embed, Colour


async def coin_not_found(interaction: Interaction) -> None:
    my_embed = Embed(colour=Colour.red())

    my_embed.add_field(
        name="⛔Coin not found", value=f"Make sure to provide a correct coin symbol"
    )

    await interaction.followup.send(embed=my_embed)
