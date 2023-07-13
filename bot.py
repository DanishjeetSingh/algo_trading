"""
Purpose:
    This script will contain the discord bot, which can send me the logs directly to my discord server.
"""

from configparser import ConfigParser

import discord
from discord.ext import commands

config = ConfigParser(interpolation=None)
config.read('config.ini')
TOKEN = config['DISCORD']['bot_token']

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

# Create a new bot instance
bot = commands.Bot(command_prefix='!', intents=intents)


# Event that triggers when the bot is ready and connected to the server
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print('Bot is ready')


# Command that responds to "!hello"
@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')


# Command that responds to "!ping"
@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')


# Run the bot
bot.run(TOKEN)
