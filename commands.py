import discord
from discord.ext import commands
from inventory import create_inventory_embed, get_user_inventory
from genshin_pull import handle_genshin_pull, handle_sell_3_stars

GENSHIN_PULL_CHANNEL_ID = [1248361818716377138, 1248509798841057350]

async def on_message(message, bot):
    if message.author.bot:
        return

    if message.channel.id in GENSHIN_PULL_CHANNEL_ID:
        if message.content.lower() == '!bdgpull':
            await handle_genshin_pull(message, bot)
        elif message.content.lower() == '!bdghelp':
            await message.channel.send('\nCurrent Functions\n1. Message Logger - Takes deleted messages and shows them in specific channels\n\nCurrent Commands\n1. !bdgpull - pulls for genshin characters and weapons (use in bot channel only)\n2. !bdginventory - view your pulled characters')

    await bot.process_commands(message)

@commands.command(name='bdginventory')
async def view_inventory(ctx):
    user_id = str(ctx.author.id)
    inventory_list = get_user_inventory(user_id)
    if len(inventory_list) == 0:
        await ctx.send("Your inventory is empty.")
        return

    pages = [inventory_list[i:i+25] for i in range(0, len(inventory_list), 25)]

    current_page = 0
    embed = create_inventory_embed(ctx.author.name, pages, current_page)
    message = await ctx.send(embed=embed)

    if len(pages) > 1:
        await message.add_reaction("⬅️")
        await message.add_reaction("➡️")
        await message.add_reaction("❌")
        await message.add_reaction("💰")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["⬅️", "➡️", "❌", "💰"]

        while True:
            try:
                reaction, user = await bot.wait_for("reaction_add", timeout=60, check=check)

                if str(reaction.emoji) == "➡️" and current_page < len(pages) - 1:
                    current_page += 1
                    await message.edit(embed=create_inventory_embed(ctx.author.name, pages, current_page))
                elif str(reaction.emoji) == "⬅️" and current_page > 0:
                    current_page -= 1
                    await message.edit(embed=create_inventory_embed(ctx.author.name, pages, current_page))
                elif str(reaction.emoji) == "❌":
                    await message.delete()
                    return
                elif str(reaction.emoji) == "💰":
                    await handle_sell_3_stars(ctx)

                await message.remove_reaction(reaction, user)
            except TimeoutError:
                break
