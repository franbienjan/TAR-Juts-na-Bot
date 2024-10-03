import random
import discord
from replit import db
from datetime import datetime

# List of Teams
teams = {
    'JUTS_TEAM_1',
    'JUTS_TEAM_2'
}

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
    else:
        embed = discord.Embed(title="🧱 Build Seawall 🧱", description=f":x: **{member.mention}**, you are the wave measurer! You are not supposed to do this. Start over!", color=0xAA4A44)
        embed.add_field(name="Team", value=team, inline=True)
        embed.set_thumbnail(url="https://i.ibb.co/5RVmv78/wall.png")
        await ctx.channel.send(embed=embed)
        reset_seawall(team)

# $check-seawall command
async def check_seawall(ctx):
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

    ####### TODO:
    # TARGET SECTIONS BASED ON THE TIME/TIDE

    embed = discord.Embed(title="✨ Seawall ready for checking! ✨", description="Screenshot this message and send to your FB GC", color=0xDAA520)
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
    #TODO: ONLY ADMIN CAN DO THIS
    """
    Stores the provided time in the Replit database.

    :param time_str: Time in the format of "H:MMAM/PM" (e.g., "9:15PM")
    """
    # Parse the time string into a datetime object
    time_obj = datetime.strptime(time_str, "%I:%M%p")
    current_date = datetime.now().date()  # Get the current date
    combined_datetime = datetime.combine(current_date, time_obj.time())
    # Store the time in the database as a string
    db["tide_time"] = combined_datetime.isoformat()

    await ctx.channel.send(f"The tides have been set. {db['tide_time']}")

def elapsed_minutes():
    """
    Calculates the minutes elapsed since the stored time in the Replit database.

    :return: Number of minutes elapsed since the stored time.
    """
    # Retrieve the stored time
    if "tide_time" not in db:
        return "No time has been set."

    # Convert the stored time string back to a datetime object
    stored_time_str = db["tide_time"]
    stored_time_obj = datetime.fromisoformat(stored_time_str)

    # Get the current time (in the same day, assuming the stored time is today)
    current_time_obj = datetime.now().replace(second=0, microsecond=0)
    print(stored_time_obj)
    print(current_time_obj)

    # Calculate the difference in minutes
    elapsed_time = current_time_obj - stored_time_obj
    elapsed_minutes = elapsed_time.total_seconds() / 60
    print(elapsed_minutes)
    print(elapsed_time)
    print(db["tide_time"])

    return int(elapsed_minutes)

async def display_tide_time(ctx):
    await ctx.channel.send(f"The tide time is {db['tide_time']}. It is currently {elapsed_minutes()} since.")

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
    elif command_name == "$check-seawall":
        await check_seawall(ctx)
        return
    elif command_name == "$start-over":
        await start_over(ctx)
        return
    elif command_name.startswith("$seawall-set-tides "):
        time_str = command_name.split(" ")[1]  # Extract time string
        await seawall_set_tides(ctx, time_str)
        return
    elif command_name == "$get-tide-time":
        await display_tide_time(ctx)
        return