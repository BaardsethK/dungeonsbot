import discord

from discord.ext import commands
from discord.ext.commands import bot

import os
from os.path import join
from os.path import dirname

import random
import json
import math
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
        race = raceInfo[0]
        raceAttributes = raceInfo[1]
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
    with open(classPath) as classes_file:
        classes_dict = json.load(classes_file)
        classes = classes_dict['playersHandbook']
        characterClass = list(classes.items())[random.randint(0, len(classes)-1)]
        className = characterClass[0]
        characterClass = characterClass[1]
        base_hp = characterClass['hitPoints']
        skills = characterClass['skills']
        available_skills = characterClass['availableSkills']
        chosen_skills = []
        for i in range(skills):
            chosen_skills.append(available_skills.pop(random.randint(0,len(available_skills)-1)))
        classInfo = {
            'Class' : className,
            'Base HP' : base_hp,
        }
        for i in range(len(chosen_skills)):
            skill_nr = f'Skill {i}'
            classInfo[skill_nr] = chosen_skills[i] 
        print(classInfo)
        return classInfo

async def getAbilityScores():
    abilities = ['strength',
        'dexterity',
        'intelligence',
        'wisdom',
        'charisma',
        'constitution']
    scores = {}
    modifier = {}
    for ability in abilities:
        dice = []
        for i in range(4):
            dice.append(random.randint(1,6))
        dice.remove(min(dice))
        score = sum(dice)
        scores[ability] =  score
        modifier[ability] = math.floor((score - 10) / 2)
    ability_total = [scores, modifier]
    return ability_total

@bot.command(name='create', description='', pass_context=True)
async def create(ctx):
    character = await getRace()
    classInfo = await getClass()
    abilityInfo = await getAbilityScores()
    msg = "Character:"
    for name, value in character.items():
        msg += f"\n\t{name}: {value}"
    msg += "\nClass:"
    for name, value in classInfo.items():
        msg += f"\n\t{name}: {value}"
    msg += "\nAbilities:"
    for name, value in abilityInfo[0].items():
        msg += f"\n\t{name}: {value} ({abilityInfo[1][name]})"
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