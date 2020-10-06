import discord

from discord.ext import commands
from discord.ext.commands import bot

import os
from os.path import join
from os.path import dirname

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

TOKEN = os.getenv('DISCORD_TOKEN')
BOT_PREFIX = ('!')

description = ''' - Python-based discord bot for quick-generation of DnD-characters.'''
bot = commands.Bot(command_prefix = BOT_PREFIX, description=description)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name=''))
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

bot.run(TOKEN)