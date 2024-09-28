import random

import discord
from replit import db


# Helper function to format wave times based on random wave measurements
def time_format(numbers):
    return [f"XX:X{num}" for num in numbers]

# Function to get wave data for the team
def get_wave_measure(team):
    return db.get(f"{team}_wave_measure")

# Function to reset the seawall progress and wave data for a team
def reset_seawall(team):
    db[f"{team}_seawall_section"] = 0
    db[f"{team}_build_fail"] = False #NO LONGER NEEDED
    db[f"{team}_wave_measure"] = None
    db[f"{team}_wave_player"] = None #holds ID of wave player
    db[f"{team}_build_player"] = None #holds ID of measure player

# $wave-measure command
async def wave_measure(ctx):
    team_role = discord.utils.find(lambda r: r.name.startswith('JUTS_TEAM_'), ctx.author.roles)
    if not team_role:
        await ctx.channel.send("You need to be in a team to use this command.")
        return

    team = team_role.name
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
    team_role = discord.utils.find(lambda r: r.name.startswith('JUTS_TEAM_'), ctx.author.roles)
    if not team_role:
        await ctx.channel.send(f":x: {member.mention}, you need to be in a team to use this command.")
        return

    team = team_role.name
    wave_measure = get_wave_measure(team)

    if not wave_measure:
        await ctx.channel.send(f":x: {member.mention}, your team hasn't measured the waves yet. Use `$wave-measure` first.")
        return

    if db[f"{team}_build_player"] is None or (db[f"{team}_build_player"] == ctx.author.id and db[f"{team}_wave_player"] != ctx.author.id):
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
    team_role = discord.utils.find(lambda r: r.name.startswith('JUTS_TEAM_'), ctx.author.roles)
    if not team_role:
        await ctx.channel.send(":x: You need to be in a team to use this command.")
        return

    team = team_role.name

    ####### TODO:
    # TARGET SECTIONS BASED ON THE TIME/TIDE

    embed = discord.Embed(title="✨ Seawall ready for checking! ✨", description="Screenshot this message and send to your FB GC", color=0xDAA520)
    embed.add_field(name="Team", value=team, inline=True)
    embed.set_thumbnail(url="https://i.ibb.co/5RVmv78/wall.png")

    await ctx.channel.send(embed=embed)

# $start-over command
async def start_over(ctx):
    team_role = discord.utils.find(lambda r: r.name.startswith('JUTS_TEAM_'), ctx.author.roles)
    if not team_role:
        await ctx.channel.send("You need to be in a team to use this command.")
        return

    team = team_role.name
    reset_seawall(team)

    embed = discord.Embed(title="🔄 Wall Reset 🔄", description=f"**{team}** has reset their seawall progress. Start building again!", color=0x0000ff)
    await ctx.channel.send(embed=embed)

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
            team_role = discord.utils.find(lambda r: r.name.startswith('JUTS_TEAM_'), ctx.author.roles)
            if team_role:
                team = team_role.name
                db[f"{team}_build_fail"] = True
        return
    elif command_name == "$check-seawall":
        await check_seawall(ctx)
        return
    elif command_name == "$start-over":
        await start_over(ctx)
        return