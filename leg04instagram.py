import discord
import utils
import json
from datetime import datetime
import pytz
from replit import db

# Timezone for Manila
MANILA_TZ = pytz.timezone('Asia/Manila')

# List of Teams
TEAMS = {
  'JUTS_AVAIL',
  'JUTS_BUKO_JUTS',
  'JUTS_JUTATAYS',
  'JUTS_JUTS_GIVE_ME_A_REASON',
  'JUTS_KHAO_KHEOW_STARS',
  'JUTS_NEW_KIDS_ON_THE_BLOCK',
  'JUTS_NUMBERS',
  'JUTS_SIMPLE_LIFE',
  'JUTS_ANNYEONG_JUTSEYO',
  'JUTS_TEAM_1',
  'JUTS_TEAM_2'
}

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

with open('official-roles.json') as f:
  officialRoles = json.load(f)

with open('official-threads.json') as f:
  officialThreads = json.load(f)

# Manually set codes and corresponding URLs for each image
PLACEHOLDER_URLS = [
    {"code": "20231029", "url": "https://i.ibb.co/0smvZkX/pirelli.png"},
    {"code": "20230114", "url": "https://i.ibb.co/1JgHyLB/kotse.png"},
    {"code": "20231230", "url": "https://i.ibb.co/Y8r2BDF/jersey.png"},
    {"code": "20230720", "url": "https://i.ibb.co/94xY0d4/number.png"},
    {"code": "20231001", "url": "https://i.ibb.co/dg9VKk5/hubad.png"},
    {"code": "20230830", "url": "https://i.ibb.co/ZKcyqCG/fan.png"},
    {"code": "20231115", "url": "https://i.ibb.co/4Wxm7Tx/art.png"},
    {"code": "20231219", "url": "https://i.ibb.co/Fhg1WsG/bahay.png"},
    {"code": "901234", "url": "https://example.com/random9.png"},
    {"code": "012345", "url": "https://example.com/random10.png"},
    {"code": "112233", "url": "https://example.com/random11.png"},
    {"code": "223344", "url": "https://example.com/random12.png"},
    {"code": "334455", "url": "https://example.com/random13.png"},
    {"code": "445566", "url": "https://example.com/random14.png"},
    {"code": "556677", "url": "https://example.com/random15.png"},
    {"code": "667788", "url": "https://example.com/random16.png"},
    {"code": "778899", "url": "https://example.com/random17.png"},
    {"code": "889900", "url": "https://example.com/random18.png"},
    {"code": "990011", "url": "https://example.com/random19.png"},
    {"code": "101010", "url": "https://example.com/random20.png"},
    {"code": "202020", "url": "https://example.com/random21.png"},
    {"code": "303030", "url": "https://example.com/random22.png"},
    {"code": "404040", "url": "https://example.com/random23.png"},
    {"code": "505050", "url": "https://example.com/random24.png"},
    {"code": "606060", "url": "https://example.com/random25.png"},
    {"code": "707070", "url": "https://example.com/random26.png"},
    {"code": "808080", "url": "https://example.com/random27.png"},
    {"code": "909090", "url": "https://example.com/random28.png"},
    {"code": "010101", "url": "https://example.com/random29.png"},
    {"code": "111111", "url": "https://example.com/random30.png"},
]

# Image sets for each level
LEVEL_1_IMAGES = PLACEHOLDER_URLS[:8]  # 8 images for Level 1
LEVEL_2_IMAGES = PLACEHOLDER_URLS[8:20]  # 12 images for Level 2
LEVEL_3_IMAGES = PLACEHOLDER_URLS[20:30]  # 10 images for Level 3

# Function to get team ID based on user roles
def get_team_id(member):
    for role in member.roles:
        if role.name in TEAMS:
            return role.name
    return None

# Function to get team ID based on user roles
def get_team_role(member):
    for role in member.roles:
        if role.name in TEAMS:
            return role
    return None

# Reset game
async def monaco_reset(ctx):
    db["monaco-lap1-ranking"] = []
    db["monaco-lap2-ranking"] = []
    db["monaco-lap3-ranking"] = []
    db["leclerc1-start"] = False
    db["leclerc2-start"] = False
    db["leclerc3-start"] = False
    for team in TEAMS:
        db["monaco-"+team+"-lap"] = 0
    db["team_data"] = {team: {"level": 1, "claimed_images": []} for team in TEAMS}
    db["level1_images"] = LEVEL_1_IMAGES.copy()
    db["level2_images"] = LEVEL_2_IMAGES.copy()
    db["level3_images"] = LEVEL_3_IMAGES.copy()
    embed = discord.Embed(title="Game Reset", description="The game has been reset successfully.", color=discord.Color.green())
    await ctx.channel.send(embed=embed)
    
# Function to join the game
async def join_game(ctx, team, level):

    # Retrieve images
    images = db[f"level{level}_images"]
    available_codes = '\n'.join(img["url"] for img in images)
    displayMsg = f'**LEVEL {level} - Available Images**\n{available_codes}'
    await ctx.channel.send(displayMsg)

# Function to claim an image by 6-digit code
async def claim_image(ctx, level, code):
    team = get_team_id(ctx.author)

    if not team:
        embed = discord.Embed(title="Error", description="You are not part of any registered team.", color=discord.Color.red())
        await ctx.channel.send(embed=embed)
        return

    # Check if the team already claimed an image for the current level
    if level in db["team_data"][team]["claimed_images"]:
        embed = discord.Embed(title="Error", description=f"{team} has already claimed an image for Level {level}.", color=discord.Color.red())
        await ctx.channel.send(embed=embed)
        return

    # Determine image pool based on level and restrict available images
    images_key = f"level{level}_images"
    images = db[images_key]
    available_images = images[:4] if level == 2 else images[:2] if level == 3 else images

    # Check if the provided code matches an available image
    for img in available_images:
        if img["code"] == code:
            db["team_data"][team]["claimed_images"].append(level)
            images.remove(img)  # Remove the claimed image
            db[images_key] = images  # Update the database

            embed = discord.Embed(title="Success", description=f"Image {code} has been successfully claimed by {team}!", color=discord.Color.green())
            await ctx.channel.send(embed=embed)

            # Replace images based on the level
            if level == 2 and len(images) < 4:
                new_image = LEVEL_2_IMAGES.pop(0)
                images.append(new_image)
                await ctx.channel.send(embed=discord.Embed(description="A new image has been added to Level 2.", color=discord.Color.blue()))
            elif level == 3 and len(images) < (len(TEAMS) + 1):
                new_image = LEVEL_3_IMAGES.pop(0)
                images.append(new_image)
                await ctx.channel.send(embed=discord.Embed(description="A new image has been added to Level 3.", color=discord.Color.blue()))

            return

    embed = discord.Embed(title="Error", description="The code you provided is not valid for the current level.", color=discord.Color.red())
    await ctx.channel.send(embed=embed)

# Function to show all available images for a specific level
async def show_available_images(ctx, level):
    if level == 1:
        images = db.get("level1_images", [])
    elif level == 2:
        images = db.get("level2_images", [])[:4]  # Show first 4
    elif level == 3:
        images = db.get("level3_images", [])[:(len(TEAMS) + 1)]  # Show based on teams
    else:
        embed = discord.Embed(title="Error", description="Invalid level number.", color=discord.Color.red())
        await ctx.channel.send(embed=embed)
        return

    available_codes = ', '.join(img["code"] for img in images)
    embed = discord.Embed(title=f"Available Images for Level {level}", description=available_codes or "No available images.", color=discord.Color.blue())
    await ctx.channel.send(embed=embed)

####################
## ENTRY FUNCTION ##
####################
# Function to process user messages
async def process_message(ctx, client):
    if ctx.author.bot:
        return

    # -- Get team
    team = get_team_id(ctx.author)
    teamRole = get_team_role(ctx.author)
    if not team:
        embed = discord.Embed(title="Error", description="You are not part of any registered team.", color=discord.Color.red())
        await ctx.channel.send(embed=embed)
        return

    # -- ADMIN COMMANDS
    if ctx.channel.id == LAB and ctx.content == '$monaco-reset':
        # This function resets the Lap #, and Position # of a team.
        await monaco_reset(ctx)
        return

    # -- PROMPTS IN TEAM GC ONLY:
    if ctx.channel.id in TEAMCHANNELIDS:
        if ctx.content == '$dock-at-monaco':
            await ctx.channel.send('https://i.ibb.co/zb10Mjn/0402-RB-Primer-Need-For-Speed.png')
            return
        elif ctx.content == '$enter-lap1-sector2':
            if db["monaco-"+team+"-lap"] == 0:
                await ctx.channel.send('ENTER LAP 1 SECTOR 2 SUCCESS') # TODO: Insert PNG here
                await utils.add_team_roles(ctx.guild, teamRole, officialRoles['LEG04-LECLERC-1'])
                await join_game(ctx, team, 1)
                db["monaco-"+team+"-lap"] = 1
            else:
                await ctx.channel.send('YOU HAVE ALREADY EXECUTED THIS!')
        elif ctx.content == '$enter-2ndlap-sector2':
            await ctx.channel.send('ENTER LAP 2 SECTOR 2 SUCCESS') # TODO: Insert PNG here
            await utils.add_team_roles(ctx.guild, teamRole, officialRoles['LEG04-LECLERC-2'])
                
            # TODO: dapat track the LEVEL of the person
        elif ctx.content == '$enter-finallap-sector2':
            await ctx.channel.send('ENTER LAP 78 SECTOR 2 SUCCESS') # TODO: Insert PNG here
            await utils.add_team_roles(ctx.guild, teamRole, officialRoles['LEG04-LECLERC-3'])
            # TODO: dapat track the LEVEL of the person
        elif ctx.content == '$finish-hunt-aliceguo':
            await ctx.channel.send('FINISH HUNT ALICE GUO')
            await utils.add_team_roles(ctx.guild, teamRole, officialRoles['LEG04-MONACO-HUNT'])
            # TODO: dapat track the LEVEL of the person
        elif ctx.content == '$finish-lap1-sector3':
            await ctx.channel.send('FINISH LAP 1 SECTOR 3 SUCCESS') # TODO: Insert PNG here
            mainLobby = client.get_channel(officialThreads['LAB'])
            timeNow = datetime.now().astimezone(MANILA_TZ).strftime(r"%I:%M:%S %p")
            await mainLobby.send(f'🏁 RACERS, START YOUR ENGINES...\n{timeNow}') #Update with correct update
            # TODO: dapat track the LEVEL of the person
        elif ctx.content == '$finish-2ndlap-sector3':
            await ctx.channel.send('FINISH LAP 2 SECTOR 3 SUCCESS') # TODO: Insert PNG here
            mainLobby = client.get_channel(officialThreads['LAB']) # TODO: Change to MAIN-LOBBY
            timeNow = datetime.now().astimezone(MANILA_TZ).strftime(r"%I:%M:%S %p")
            embed = discord.Embed(title=f":checkered_flag: **F1 RACE** ", description="", color=0xffffff)
            embed.add_field(name="Position", value="Currently 1st", inline=False)
            embed.add_field(name="Team", value=team, inline=False)
            embed.add_field(name="Lap", value="1", inline=True)
            embed.add_field(name="Time", value=f"{timeNow}", inline=True)
            embed.set_thumbnail(url="https://i.ibb.co/FsTLB5y/annyeongjutseyo.png")
            await mainLobby.send(embed=embed) #Update with correct update
            # TODO: dapat track the LEVEL of the person
            
    # -- INSTAGRAM TASK FOR CHARLES LECLERC
    if ctx.content.startswith("$charles-lap1 "):
        await claim_image(ctx, 1, ctx.content.split(" ")[1].upper())
    elif ctx.content.startswith("$charles-2ndlap "):
        await claim_image(ctx, 2, ctx.content.split(" ")[1].upper())
    elif ctx.content.startswith("$charles-finallap "):
        await claim_image(ctx, 3, ctx.content.split(" ")[1].upper())
    elif ctx.content.startswith("$charles-all "):
        await show_available_images(ctx, int(ctx.content.split(" ")[1]))
