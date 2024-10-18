# This code is based on the following example:
# https://discordpy.readthedocs.io/en/stable/quickstart.html#a-minimal-bot

import os
import discord
import json
import leg01boats, leg01oils, leg02seawall, leg04instagram, leg06crates, leg07phosphate, utils

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = discord.Client(intents=intents)

with open('official-roles.json') as f:
  officialRoles = json.load(f)

with open('official-threads.json') as f:
  officialThreads = json.load(f)

TEAMCHANNELIDS = [
    1065231788580012102, #LAB ====
    1296050304768413757, #Avail
    1296050152565379083, #AnnyeongJutseyo
    1296050613544685610, #BukoJuts
    1296049983388258387, #Jutatays
    1296049893244272744, #JutsGiveMeAReason
    1296050524533166090, #KhaoKheowStars
    1296049799677874186, #NewKidsOnTheBlock
    1296050058483208254, #Numbers
    1296050222602129469 #SimpleLife
]

LAB = 1065231788580012102

###############################################
##                 TAR Juts                  ##
##             Friday Bot Codes              ##
###############################################

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(ctx):

    if ctx.author == client.user:
        return

    if ctx.content.startswith('$hello'):
        await ctx.channel.send('Hello!')

    # ======== LEG 01 ==========
    '''
    # -- Detour Roles
    if ctx.channel.id in TEAMCHANNELIDS and ctx.content == '$oligarchy-dt':
        await utils.add_role(ctx.guild, ctx.author, officialRoles['LEG01-DT-OLIGARCHY'])
        return
    elif ctx.channel.id in TEAMCHANNELIDS and ctx.content == '$dt-piracy':
        await utils.add_role(ctx.guild, ctx.author, officialRoles['LEG01-DT-PIRACY'])
        return

    # -- Kampongs
    if ctx.channel.id in TEAMCHANNELIDS and ctx.content.startswith('$kampong-'):
        await leg01boats.process_message(ctx)
        return

    # -- Oils
    if ctx.channel.id in [officialThreads["LEG01-DT-OLIGARCHY"], LAB] and ctx.content.startswith('$'):
        await leg01oils.process_message(ctx)
        return
    #'''

    # ======== LEG 02 ==========
    ''' 
    # -- Detour Roles
    if ctx.content.startswith('$against-sea'):
        await utils.add_role(ctx.guild, ctx.author, officialRoles['LEG02-DT-SEAWALL'])
        return

    # -- Seawall
    if ctx.channel.id in [officialThreads["LEG02-DT-SEAWALL"], LAB]:
        await leg02seawall.process_message(ctx)
    #'''

    # ======== LEG 04 ==========
    '''
    # -- Everything Leg 04 is here.
    if ctx.content.startswith('$'):
        await leg04instagram.process_message(ctx, client)
    #'''
    
    # ======== LEG 06 ==========
    #'''
    # -- Detour Roles
    if ctx.content.startswith('$banjul-port'):
        await utils.add_role(ctx.guild, ctx.author, officialRoles['LEG06-NEURALINK'])
        return
    if ctx.channel.id in [officialThreads["LEG06-NEURALINK"], LAB]:
        await leg06crates.process_message(ctx, client)
    #'''
    
    # ======== LEG 07 ==========
    '''
    if (ctx.channel.id in TEAMCHANNELIDS or ctx.channel.id == 1288522309149261914) and ctx.content.startswith('$'):
        await leg07phosphate.process_message(ctx)
    #'''

try:
  token = os.getenv("TOKEN") or ""
  if token == "":
    raise Exception("Please add your token to the Secrets pane.")
  client.run(token)
except discord.HTTPException as e:
    if e.status == 429:
        print(
            "The Discord servers denied the connection for making too many requests"
        )
        print(
            "Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests"
        )
    else:
        raise e
