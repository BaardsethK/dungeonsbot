import discord

from discord.ext import commands
from discord.ext.commands import bot

import os
from os.path import join
from os.path import dirname

import random
import json
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

TOKEN = os.getenv('DISCORD_TOKEN')
BOT_PREFIX = ('!dn ')

description = ''' - Python-based discord bot for quick-generation of DnD-characters.'''
bot = commands.Bot(command_prefix = BOT_PREFIX, description=description)

racePath = './races.json'
classPath = './classes.json'

async def getRace():
    with open(racePath) as races_file:
        races_dict = json.load(races_file)
        races = races_dict['playersHandbook']
        raceInfo = list(races.items())[random.randint(0,len(races)-1)]
        print(raceInfo)
        race = raceInfo[0]
        raceAttributes = raceInfo[1]
        print(race)
        maxAge = raceAttributes['maxAge']
        avgHeight = raceAttributes['height']
        avgWeight = raceAttributes['weight']
        subrace = ""
        if "subrace" in raceAttributes:
            
            subrace = raceAttributes['subrace'][random.randint(0,len(raceAttributes['subrace'])-1)]

        age = random.randint(10, maxAge)
        height = avgHeight * (1 + random.uniform(-0.1, 0.1))
        weightHeightRatio = avgWeight * (height / avgHeight)
        weight = weightHeightRatio * (1 + random.uniform(-0.1, 0.1))
        character = {
            "Race" : race,
            "Age" : age,
            "Height" : height,
            "Weight" : weight,
        }
        if len(subrace) > 0:
            character["Subrace"] = subrace
        return character

async def getClass():
    pass

async def getAbilityScores():
    abilities = ['strength',
        'dexterity',
        'intelligence',
        'wisdom',
        'charisma',
        'constitution']
    scores = {}
    for ability in abilities:
        dice = []
        for i in range(4):
            dice.append(random.randint(1,6))
        dice.remove(min(dice))
        scores[ability] =  sum(dice)
    return scores

async def chooseSkills():
    pass

@bot.command(name='create', description='', pass_context=True)
async def create(ctx):
    character = await getRace()
    print(character)
    msg = "Character:"
    for name, value in character.items():
        msg += f"\n\t{name}: {value}"
    await ctx.send(msg)

@bot.event
async def on_message(message):
    await bot.process_commands(message)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name=''))
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

bot.run(TOKEN)