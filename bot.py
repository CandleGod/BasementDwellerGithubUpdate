import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import json

load_dotenv()
TOKEN = os.getenv('origTOKEN')

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Constants
deleted_messages_channel_id = 1248074093409079400

# Message logger for deleted messages
@bot.event
async def on_message_delete(message):
    if message.author.bot:
        return

    channel = message.channel
    content = message.clean_content
    author = message.author

    embed = discord.Embed(
        title=f"Deleted Message in #{channel.name}",
        description=content if content else "[No content]",
        color=0xff0000
    )
    embed.set_author(name=author.name, icon_url=author.avatar.url)
    embed.set_footer(text=f"Author ID: {author.id}")

    deleted_messages_channel = bot.get_channel(deleted_messages_channel_id)
    if deleted_messages_channel:
        await deleted_messages_channel.send(embed=embed)

bot.run(TOKEN)
