import random
import discord
from replit import db
import re
from datetime import datetime, timedelta
import pytz

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

# Timezone for Manila
MANILA_TZ = pytz.timezone('Asia/Manila')

# Helper function to format wave times based on random wave measurements
def time_format(numbers):
    return [f"XX:X{num}" for num in numbers]

# Function to get wave data for the team
def get_wave_measure(team):
    return db.get(f"{team}_wave_measure")

# Function to reset the seawall progress and wave data for a team
def reset_seawall(team):
    db[f"{team}_seawall_section"] = 0
    db[f"{team}_wave_measure"] = None
    db[f"{team}_wave_player"] = None #holds ID of wave player
    db[f"{team}_build_player"] = None #holds ID of measure player

# $wave-measure command
async def wave_measure(ctx):
    rolePermitted = False
    team = ''
    for role in ctx.author.roles:
        if role.name in teams:
            rolePermitted = True
            team = role.name
            break
    if not rolePermitted:
        await ctx.channel.send("You need to be in a team to use this command.")
        return

    member = ctx.author
    if db[f"{team}_wave_measure"] != None:
        embed = discord.Embed(title="🌊 Wave Measurement 🌊", description=f":x: You already measured the waves! Start over!", color=0x808080)
        embed.set_thumbnail(url="https://i.ibb.co/pvjtG9y/wave.png")
        embed.add_field(name="Team", value=team, inline=True)
        await ctx.channel.send(embed=embed)
        reset_seawall(team)
        return
        
    if db[f"{team}_wave_player"] is None or db[f"{team}_wave_player"] == ctx.author.id:
        # Allow measuring waves any number of times
        wave_numbers = random.sample(range(10), 3)
        wave_times = time_format(wave_numbers)
        # Store in Replit DB
        db[f"{team}_wave_measure"] = wave_numbers
        db[f"{team}_wave_player"] = ctx.author.id

        embed = discord.Embed(title="🌊 Wave Measurement 🌊", description=f"Measurer **{member.mention}**, here are the wave times for {team}: {', '.join(wave_times)}", color=0xADD8E6)
        embed.add_field(name="Team", value=team, inline=True)
        embed.set_thumbnail(url="https://i.ibb.co/pvjtG9y/wave.png")
        await ctx.channel.send(embed=embed)
    else:
        embed = discord.Embed(title="🌊 Wave Measurement 🌊", description=f":x: You are the builder! You are not supposed to do this. Start over!", color=0x808080)
        embed.add_field(name="Team", value=team, inline=True)
        embed.set_thumbnail(url="https://i.ibb.co/pvjtG9y/wave.png")
        await ctx.channel.send(embed=embed)
        reset_seawall(team)

# $build-seawall X command
async def build_seawall(ctx, section: int):
    member = ctx.author
    rolePermitted = False
    team = ''
    for role in ctx.author.roles:
        if role.name in teams:
            rolePermitted = True
            team = role.name
            break
    if not rolePermitted:
        await ctx.channel.send("You need to be in a team to use this command.")
        return
    wave_measure = get_wave_measure(team)

    if not wave_measure:
        await ctx.channel.send(f":x: {member.mention}, your team hasn't measured the waves yet. Use `$wave-measure` first.")
        return

    if db[f"{team}_wave_player"] != ctx.author.id or db[f"{team}_build_player"] == ctx.author.id:
        db[f"{team}_build_player"] = ctx.author.id
        if ctx.created_at.minute % 10 not in get_wave_measure(team):
            embed = discord.Embed(title="🧱 Build Seawall 🧱", description=f":x: Builder **{member.mention}**, you posted at the wrong minute! Start over!", color=0x808080)
            embed.add_field(name="Team", value=team, inline=True)
            embed.set_thumbnail(url="https://i.ibb.co/5RVmv78/wall.png")
            reset_seawall(team)
            await ctx.channel.send(embed=embed)
            return
        
        prev_section = db.get(f"{team}_seawall_section", 0)

        if prev_section != section - 1:
            embed = discord.Embed(title="🧱 Build Seawall 🧱", description=f":x: Builder **{member.mention}**, you posted incorrectly! Start over!", color=0x808080)
            embed.add_field(name="Team", value=team, inline=True)
            embed.set_thumbnail(url="https://i.ibb.co/5RVmv78/wall.png")
            reset_seawall(team)
            await ctx.channel.send(embed=embed)
            return
        else:
            embed = discord.Embed(title="🧱 Build Seawall 🧱", description=f"🧱 Builder **{member.mention}**, you have successfully built a new section(s) of the seawall.", color=0x808080)
            embed.add_field(name="Team", value=team, inline=True)
            embed.add_field(name="Section/s", value=section, inline=True)
            embed.set_thumbnail(url="https://i.ibb.co/5RVmv78/wall.png")
            db[f"{team}_seawall_section"] = section
            db[f"{team}_wave_measure"] = None
            await ctx.channel.send(embed=embed)
            await check_seawall(ctx, team)
    else:
        embed = discord.Embed(title="🧱 Build Seawall 🧱", description=f":x: **{member.mention}**, you are the wave measurer! You are not supposed to do this. Start over!", color=0xAA4A44)
        embed.add_field(name="Team", value=team, inline=True)
        embed.set_thumbnail(url="https://i.ibb.co/5RVmv78/wall.png")
        await ctx.channel.send(embed=embed)
        reset_seawall(team)

# $check-seawall command
async def check_seawall(ctx, team: str):
    # Retrieve the tide time from the database
    tide_time_str = db['tide_time']
    tide_time = datetime.fromisoformat(tide_time_str).astimezone(MANILA_TZ)

    # Get the current time in Manila timezone
    manila_now = datetime.now(MANILA_TZ)

    # Calculate the time difference in minutes
    time_difference = manila_now - tide_time
    minutes_passed = int(time_difference.total_seconds() // 60)

    # Determine the target number of sections based on minutes passed
    if minutes_passed >= 35:
        target_sections = 5
    elif minutes_passed >= 25:
        target_sections = 6
    else:
        target_sections = 7

    # Retrieve the current seawall progress for the team
    seawall_progress_key = f"{team}_seawall_section"
    current_sections = db.get(seawall_progress_key, 0)  # Default to 0 if not found

    # Check if the number of sections built matches the target
    if current_sections >= target_sections:
        embed = discord.Embed(
            title="✨ Seawall Completed! ✨", 
            description=f"{team} has successfully built the seawall with the correct number of {target_sections} sections!",
            color=0xDAA520
        )
        embed.add_field(name="Team", value=team, inline=True)
        embed.set_thumbnail(url="https://i.ibb.co/5RVmv78/wall.png")

        await ctx.channel.send(embed=embed)

# $start-over command
async def start_over(ctx):
    rolePermitted = False
    team = ''
    for role in ctx.author.roles:
        if role.name in teams:
            rolePermitted = True
            team = role.name
            break
    if not rolePermitted:
        await ctx.channel.send("You need to be in a team to use this command.")
        return
    reset_seawall(team)

    embed = discord.Embed(title="🔄 Wall Reset 🔄", description=f"**{team}** has reset their seawall progress. Start building again!", color=0x0000ff)
    await ctx.channel.send(embed=embed)

async def seawall_set_tides(ctx, time_str: str):
    if not validate_time_format(time_str):
        await ctx.channel.send("Invalid time format. Please use 'HH:MM AM/PM'. Example: 05:00 PM")
        return

    # Get current date in Manila timezone
    manila_now = datetime.now(MANILA_TZ)

    # Parse the time_str
    tide_time = datetime.strptime(time_str, '%I:%M %p')

    # Combine today's date with the provided time
    tide_time_today = manila_now.replace(hour=tide_time.hour, minute=tide_time.minute, second=0, microsecond=0)

    # Save the tide time to the database
    db['tide_time'] = tide_time_today.isoformat()

    await ctx.channel.send(f"Tide time has been set to {time_str} for today.")

async def display_tide_time(ctx):
    if 'tide_time' not in db:
        await ctx.channel.send("Tide time has not been set yet. Use $seawall-set-tides to set the tide time.")
        return

    # Retrieve the saved tide time from the database
    tide_time_str = db['tide_time']
    tide_time = datetime.fromisoformat(tide_time_str).astimezone(MANILA_TZ)

    # Get the current time in Manila timezone
    manila_now = datetime.now(MANILA_TZ)

    # Calculate the time difference in minutes
    time_difference = manila_now - tide_time
    minutes_passed = int(time_difference.total_seconds() // 60)

    await ctx.channel.send(f"{minutes_passed} minutes have passed since the tide time.")
    
# Helper function to validate time format
def validate_time_format(time_str):
    pattern = r'^\d{2}:\d{2} (AM|PM)$'
    return re.match(pattern, time_str)

def reset_all_teams():
  for team in teams:
    reset_seawall(team)
      
####################
## ENTRY FUNCTION ##
####################
# Function to process user messages and return results as an embed message
async def process_message(ctx):
    # Parse command details
    command_name = ctx.content

    if command_name == "$wave-measure":
        await wave_measure(ctx)
        return   
    elif command_name.startswith("$build-seawall "):
        try:
            section = int(command_name.split(" ")[1])  # Extract section number
            await build_seawall(ctx, section)
        except ValueError:
            await ctx.channel.send("Invalid section number. Please provide a valid number.")
        return
    #elif command_name == "$check-seawall":
    #    await check_seawall(ctx)
    #    return
    elif command_name == "$start-over":
        await start_over(ctx)
        return
    elif command_name.startswith("$seawall-set-tides "):
        time_str = " ".join(command_name.split(" ")[1:])
        await seawall_set_tides(ctx, time_str)
        return
    elif command_name == "$get-tide-time":
        await display_tide_time(ctx)
        return
    elif command_name == "$seawall-reset":
        reset_all_teams()
        await ctx.channel.send("Reset done.")
        return