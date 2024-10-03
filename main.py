# This code is based on the following example:
# https://discordpy.readthedocs.io/en/stable/quickstart.html#a-minimal-bot

import os
import discord
import leg01boats, leg01oils, leg02seawall, leg07phosphate

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = discord.Client(intents=intents)

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

    # TODO: Fix this to become the team's gc
    #if ctx.channel.id in [1065231788580012102] and ctx.content.startswith('$'):
    #    result, embed = leg01boats.process_message(ctx)
    #    if embed != None:
    #        await ctx.channel.send(embed=result)
    #    else:
    #        await ctx.channel.send(result)

    # TODO: Fix this to become the team's gc
    #if ctx.channel.id in [1065231788580012102] and ctx.content.startswith('$'):
    #    await leg01oils.process_message(ctx)

    # TODO: Fix this to become the team's gc
    if ctx.channel.id in [1065231788580012102]:
        await leg02seawall.process_message(ctx)

    #if ctx.channel.id in [1065231788580012102]:
    #    await leg07phosphate.process_message(ctx)

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
