import csv
import random
import time
import discord
from discord.ext import commands
from inventory import add_to_inventory, get_user_inventory, create_inventory_embed, remove_3_star_items

cooldowns = {}

async def handle_genshin_pull(message, bot):
    if message.author.id in cooldowns:
        if cooldowns[message.author.id] + 10 > time.time():
            await message.channel.send('You need to wait 10 seconds before pulling again!')
            return
        else:
            del cooldowns[message.author.id]

    with open('charwepwithidentifier.csv', 'r') as f:
        reader = csv.reader(f)
        characters = list(reader)

    # Separate characters by rarity
    characters_by_rarity = {
        '5-star': [],
        '4-star': [],
        '3-star': []
    }
    for character in characters:
        if character[1] == '5':
            characters_by_rarity['5-star'].append(character)
        elif character[1] == '4':
            characters_by_rarity['4-star'].append(character)
        else:
            characters_by_rarity['3-star'].append(character)

    # Define rarity probabilities
    rarity_probabilities = {
        '5-star': 0.01,
        '4-star': 0.10,
        '3-star': 0.89
    }

    # Choose rarity based on probabilities
    rarities = list(rarity_probabilities.keys())
    probabilities = list(rarity_probabilities.values())
    chosen_rarity = random.choices(rarities, probabilities)[0]

    # Choose a character from the chosen rarity
    character = random.choice(characters_by_rarity[chosen_rarity])

    # Update the user's inventory
    user_id = str(message.author.id)
    add_to_inventory(user_id, character)

    # Rarity color
    if chosen_rarity == '5-star':
        embed_color = 0xFFD700  # Gold
    elif chosen_rarity == '4-star':
        embed_color = 0x800080  # Purple
    else:
        embed_color = 0x00FFFF  # Cyan

    embed = discord.Embed(title=f'You pulled: {character[0]}!', color=embed_color)
    embed.set_image(url=character[3])
    embed.add_field(name='Star', value=character[1], inline=False)
    embed.add_field(name='Rarity', value=character[2], inline=False)

    await message.channel.send(embed=embed)

    cooldowns[message.author.id] = time.time()

async def handle_sell_3_stars(ctx):
    user_id = str(ctx.author.id)
    inventory_list = get_user_inventory(user_id)
    if len(inventory_list) == 0:
        await ctx.send("Your inventory is empty.")
        return

    sold_items = [item for item in inventory_list if item[2] == "3-star"]
    if not sold_items:
        await ctx.send("You have no 3-star items to sell.")
        return

    remove_3_star_items(user_id)

    await ctx.send(f"You have sold {len(sold_items)} 3-star item(s) from your inventory.")
