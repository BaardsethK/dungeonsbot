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
backgroundsPath = './backgrounds.json'
npcPath = './npc.json'

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
        height_inch, height_feet = math.modf(height)
        height_inch = height_inch / (1/12)
        weightHeightRatio = avgWeight * (height / avgHeight)
        weight = weightHeightRatio * (1 + random.uniform(-0.1, 0.1))
        character = {
            "Race" : race,
            "Age" : age,
            "Height" : f"{height_feet} ft, {math.floor(height_inch)} in",
            "Weight" : round(weight, 1),
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
            skill_nr = f'Skill {i+1}'
            classInfo[skill_nr] = chosen_skills[i] 
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

async def getBackground():
    with open(backgroundsPath) as backgrounds_file:
        background_dict = json.load(backgrounds_file)
        backgrounds = background_dict['playersHandbook']
        character_background = list(backgrounds.items())[random.randint(0, len(backgrounds)-1)]
        background_name = character_background[0]
        background_details = character_background[1]
        background_feats = {}
        background_feats['name'] = background_name
        
        if 'tools' in background_details:
            length = len(background_details['availableTools'])
            if background_details['tools'] == length:
                for i in range(background_details['tools']):
                    skill_name = f"Tool {i+1}"
                    background_feats[skill_name] = background_details['availableTools'][i]
            else:
                for i in range(background_details['tools']):
                    skill_name = f'Tool {i+1}'
                    background_feats[skill_name] = background_details['availableTools'][random.randint(1, length-1)]

        if 'languages' in background_details:
            length = len(background_details['availableLanguages'])
            if background_details['languages'] == length:
                for i in range(background_details['languages']):
                    skill_name = f"Language {i+1}"
                    background_feats[skill_name] = background_details['availableLanguages'][i]
            else:
                for i in range(background_details['languages']):
                    skill_name = f'Language {i+1}'
                    background_feats[skill_name] = background_details['availableLanguages'][random.randint(1, length-1)]
        
        if 'skills' in background_details:
            length = len(background_details['availableSkills'])
            if background_details['skills'] == length:
                for i in range(background_details['skills']):
                    skill_name = f"Skill {i+1}"
                    background_feats[skill_name] = background_details['availableSkills'][i]
            else:
                for i in range(background_details['skills']):
                    skill_name = f'Skill {i+1}'
                    background_feats[skill_name] = background_details['availableSkills'][random.randint(1, length-1)]
        return background_feats

@bot.command(name='create', description='', pass_context=True)
async def create(ctx):
    character = await getRace()
    classInfo = await getClass()
    abilityInfo = await getAbilityScores()
    backgroundInfo = await getBackground()
    msg = "Character:"
    for name, value in character.items():
        msg += f"\n\t{name}: {value}"
    msg += "\nClass:"
    for name, value in classInfo.items():
        msg += f"\n\t{name}: {value}"
    msg += "\nAbilities:"
    for name, value in abilityInfo[0].items():
        msg += f"\n\t{name}: {value} ({abilityInfo[1][name]})"
    msg += "\nBackground:"
    for name,value in backgroundInfo.items():
        msg += f"\n\t{name}: {value}"
    await ctx.send(msg)

@bot.command(name='npc', description='Generate NPC, either by input or randomly', pass_context=True)
async def npc(ctx):
    with open(npcPath) as file:
        npcs_dict = json.load(file)
        npc_types = npcs_dict['playersHandbook']
        msg = "placeholder"
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