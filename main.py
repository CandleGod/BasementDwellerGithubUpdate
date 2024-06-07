from discord.ext import commands
import discord
import os
from dotenv import load_dotenv
from commands import on_message, view_inventory

load_dotenv()
TOKEN = os.getenv('origTOKEN')

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
bot.add_listener(on_message, 'on_message')
bot.add_command(view_inventory)

@bot.event
async def on_ready():
    print(f'Currently goofing around as {bot.user}')

bot.run(TOKEN)
