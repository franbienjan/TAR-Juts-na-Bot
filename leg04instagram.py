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
    {"code": "20240914", "url": "https://i.ibb.co/TPzLSpH/azerbaijan.png"},
    {"code": "20240922", "url": "https://i.ibb.co/F4XQpDs/inchident.png"},
    {"code": "20240828", "url": "https://i.ibb.co/259z3Cp/shades.png"},
    {"code": "20240818", "url": "https://i.ibb.co/sV5sRZs/sink.png"},
    {"code": "20240806", "url": "https://i.ibb.co/Jsrqdk9/johhnie.png"},
    {"code": "20240729", "url": "https://i.ibb.co/8MDSZXC/shoes.png"},
    {"code": "20240711", "url": "https://i.ibb.co/ngCFSdx/pola.png"},
    {"code": "20240507", "url": "https://i.ibb.co/ZMVn3BB/leo.png"},
    {"code": "20240523", "url": "https://i.ibb.co/sJWCg4S/emo.png"},
    {"code": "20240329", "url": "https://i.ibb.co/Fh4Bwjr/indra.png"},
    {"code": "20240213", "url": "https://i.ibb.co/N1yFGr2/oldguy.png"},
    {"code": "20240125", "url": "https://i.ibb.co/MhL6Sgh/super.png"},
    {"code": "20170803", "url": "https://i.ibb.co/sRZ7csV/forgotten.png"},
    {"code": "20181013", "url": "https://i.ibb.co/prKJWFr/trolley.png"},
    {"code": "20190903", "url": "https://i.ibb.co/JRS1QW0/banner.png"},
    {"code": "20220713", "url": "https://i.ibb.co/Js6FwXN/abs.png"},
    {"code": "20221215", "url": "https://i.ibb.co/8sNxW72/painting.png"},
    {"code": "20220113", "url": "https://i.ibb.co/D5n0rFF/scan.png"},
    {"code": "20191202", "url": "https://i.ibb.co/dgKXZPv/dive.png"},
    {"code": "20190706", "url": "https://i.ibb.co/kSqFXKF/water.png"},
    {"code": "20190319", "url": "https://i.ibb.co/jZS8KQs/plate.png"},
    {"code": "20180328", "url": "https://i.ibb.co/6DV3Vhn/tribute.png"},
    {"code": "20180203", "url": "https://i.ibb.co/4VNB0bj/license.png"},
    {"code": "20171007", "url": "https://i.ibb.co/yVVKWHr/fia.png"},
    {"code": "20170516", "url": "https://i.ibb.co/n8vJ4b9/flag.png"},
    {"code": "20160910", "url": "https://i.ibb.co/qYRRzWV/watch.png"},
    {"code": "20130121", "url": "https://i.ibb.co/PNyrMPd/first.png"}
]

# Image sets for each level
LEVEL_1_IMAGES = PLACEHOLDER_URLS[:8]  # 8 images for Level 1
LEVEL_2_IMAGES = PLACEHOLDER_URLS[8:20]  # 12 images for Level 2
LEVEL_3_IMAGES = PLACEHOLDER_URLS[20:35]  # 15 images for Level 3

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
    db["monaco-lap3-ig"] = 0
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

# Function to claim an image by 6-digit code
async def claim_image(ctx, level, code):
    team = get_team_id(ctx.author)

    # Check if the team already claimed an image for the current level
    if level in db["team_data"][team]["claimed_images"]:
        embed = discord.Embed(title="Error", description=f"{team} has already claimed an image for Level {level}.", color=discord.Color.red())
        await ctx.channel.send(embed=embed)
        return

    # Determine image pool based on level and restrict available images
    images_key = f"level{level}_images"
    images = db[images_key]
    available_images = images[:4] if level == 2 else images[:(db["monaco-lap3-ig"] + 1)] if level == 3 else images

    # Check if the provided code matches an available image
    for img in available_images:
        if img["code"] == code:
            db["team_data"][team]["claimed_images"].append(level)
            images.remove(img)  # Remove the claimed image
            db[images_key] = images  # Update the database

            embed = discord.Embed(title="Success", description=f"Image {code} has been successfully claimed by {team}!", color=discord.Color.green())
            await ctx.channel.send(embed=embed)
            await ctx.author.send("THIS IS THE CLUE")

            # Replace images based on the level
            if level == 2 and len(images) < 4:
                print("pumapasok ba here")
                new_image = LEVEL_2_IMAGES.pop(0)
                images.append(new_image)
                await ctx.channel.send(embed=discord.Embed(description="A new image has been added to Level 2.", color=discord.Color.blue()))
            elif level == 3 and len(images) < (db["monaco-lap3-ig"] + 1):
                print("parang wala naman?")
                new_image = LEVEL_3_IMAGES.pop(0)
                images.append(new_image)
                await ctx.channel.send(embed=discord.Embed(description="A new image has been added to Level 3.", color=discord.Color.blue()))

            await show_available_images(ctx, level)
            return

# Function to show all available images for a specific level
async def show_available_images(ctx, level):
    if level == 1:
        images = db.get("level1_images", [])
        command = "$charles-lap1 xxxxxxxx"
    elif level == 2:
        images = db.get("level2_images", [])[:4]  # Show first 4
        command = "$charles-2ndlap xxxxxxxx"
    elif level == 3:
        command = "$charles-finallap xxxxxxxx"
        images = db.get("level3_images", [])[:(db["monaco-lap3-ig"] + 1)]  # Show based on teams ON LEVEL 3
    else:
        embed = discord.Embed(title="Error", description="Invalid level number.", color=discord.Color.red())
        await ctx.channel.send(embed=embed)
        return

    available_codes = '\n'.join(img["url"] for img in images)
    embed = discord.Embed(title=f":camera_with_flash: LECLERC LAP {level}", description=f"Find these in Charles Leclerc's Instagram.\nUse the command `{command}` where xxxxxxxx is the date of the post in yyyymmdd format.", color=discord.Color.red())
    embed.add_field(name="Available Images", value=available_codes, inline=False)
    embed.add_field(name="List since", value=f"{datetime.now()}", inline=False)
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

    currentLap = db["monaco-"+team+"-lap"]

    # -- PROMPTS IN TEAM GC ONLY:
    if ctx.channel.id in TEAMCHANNELIDS:
        if ctx.content == '$dock-at-monaco':
            await ctx.channel.send('https://i.ibb.co/zb10Mjn/0402-RB-Primer-Need-For-Speed.png')
            return
        elif ctx.content == '$enter-lap1-sector2':
            if db["monaco-"+team+"-lap"] == 0:
                await ctx.channel.send('ENTER LAP 1 SECTOR 2 SUCCESS') # TODO: Insert PNG here
                await utils.add_team_roles(ctx.guild, teamRole, officialRoles['LEG04-LECLERC-1'])
                await show_available_images(ctx, 1)
                db["monaco-"+team+"-lap"] = 1
            return
        elif ctx.content == '$enter-2ndlap-sector2':
            print(db["monaco-"+team+"-lap"])
            if db["monaco-"+team+"-lap"] == 1:
                await ctx.channel.send('ENTER LAP 2 SECTOR 2 SUCCESS') # TODO: Insert PNG here
                await utils.add_team_roles(ctx.guild, teamRole, officialRoles['LEG04-LECLERC-2'])
                await show_available_images(ctx, 2)
                db["monaco-"+team+"-lap"] = 2
            return
        elif ctx.content == '$enter-finallap-sector2':
            if db["monaco-"+team+"-lap"] == 2:
                db["monaco-lap3-ig"] = db["monaco-lap3-ig"] + 1
                await ctx.channel.send('ENTER LAP 78 SECTOR 2 SUCCESS') # TODO: Insert PNG here
                await utils.add_team_roles(ctx.guild, teamRole, officialRoles['LEG04-LECLERC-3'])
                await show_available_images(ctx, 3)
                db["monaco-"+team+"-lap"] = 3
            return
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
    if ctx.channel.id == officialThreads['LEG04-LECLERC-1'] and ctx.content.startswith("$charles-lap1 ") and currentLap == 1:
        await claim_image(ctx, 1, ctx.content.split(" ")[1].upper())
    elif ctx.channel.id == officialThreads['LEG04-LECLERC-2'] and ctx.content.startswith("$charles-2ndlap ") and currentLap == 2:
        await claim_image(ctx, 2, ctx.content.split(" ")[1].upper())
    elif ctx.channel.id == officialThreads['LEG04-LECLERC-3'] and ctx.content.startswith("$charles-finallap ") and currentLap == 3:
        await claim_image(ctx, 3, ctx.content.split(" ")[1].upper())
    #elif ctx.content.startswith("$charles-all "):
    #    await show_available_images(ctx, int(ctx.content.split(" ")[1]))
