import discord
import random
from replit import db

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

# Helper function to get the team role from the user's roles
def get_team_role(member):
    for role in member.roles:
        if role.name in TEAMS:
            return role.name
    return None

# Helper function to check if a user has the "HOSTS" role
def has_hosts_role(member):
    return "GOLD_HOSTS" in [role.name for role in member.roles] if member else False

# Initialize everything
def initialize_barrel():
  for team in TEAMS:
    reset_barrel(f"{team}")
    db[f"{team}_barrels"] = 0

  return "Oil barrels initialized successfully."

# Function to check if the team has successfully filled the barrel
def check_success(volume):
  return volume in [3, 5, 8]

def reset_barrel(team):
  db[f"{team}_volume"] = 100

####################
## ENTRY FUNCTION ##
####################
# Function to process user messages and return results as an embed message
async def process_message(ctx):
  message = ctx.content

  if message == "$oil-reset":
    if not has_hosts_role(ctx.author):
      embed = discord.Embed(
        title="Permission Denied",
        description="You do not have permission to initialize the game.",
        color=discord.Color.red()
      )
    else:
      embed = discord.Embed(
        title="Oil Game Initialized",
        description=initialize_barrel(),
        color=discord.Color.green()
      )
    await ctx.channel.send(embed=embed)
    return

  elif message == "$extract-oil":
    member = ctx.author
    team_role = get_team_role(member)

    if not team_role:
      embed = discord.Embed(
        title="Team Not Found",
        description=":x: You are not part of a valid team!",
        color=discord.Color.red()
      )
      await ctx.channel.send(embed=embed)
      return

    # Check if they have filled 3 barrels
    if db[f"{team_role}_barrels"] == 3:
        embed = discord.Embed(
          title=":sparkles: Congratulations! :sparkles:",
          description=f"**{team_role}**, your team has successfully filled :oil: 3 barrels of oil! Screenshot this message and send to your FB Team GC to receive the next clue.",
          color=discord.Color.gold()
        )
        embed.set_image(url="https://i.ibb.co/x7tqyFZ/image.png")
        await ctx.channel.send(embed=embed)
        return

    # Initialize barrel if not already done
    if f"{team_role}_volume" not in db:
      reset_barrel(team_role)

    # Get current oil volume
    current_volume = db[f"{team_role}_volume"]

    if current_volume < 10:
      embed = discord.Embed(
        title=":fuelpump: Barrel Filling Failed :fuelpump:",
        description=f":x: :repeat: **{team_role}** is now less than 10 gallons. Resetting to initial volume of **100** gallons!",
        color=discord.Color.red()
      )
      reset_barrel(team_role)
      await ctx.channel.send(embed=embed)
      return

    # Extract random amount of oil
    extraction = random.randint(0, current_volume)
    current_volume -= extraction
    db[f"{team_role}_volume"] = current_volume

    # Create an embed message for the extraction event
    embed = discord.Embed(
      title=f":fuelpump: Oil Extraction :fuelpump:",
      description=f"**{member.mention}** (of **{team_role}**) extracted **{extraction}** gallon/s of oil.",
      color=discord.Color.blue()
    )
    embed.add_field(name="Oil Left", value=f":fuelpump: {current_volume} gallon/s", inline=True)
    embed.add_field(name="Barrels Reduced", value=f":oil: {db[f'{team_role}_barrels']} / 3", inline=True)
    await ctx.channel.send(embed=embed)

    # Check if they successfully filled the barrel
    if current_volume < 10:
        if check_success(current_volume):
            db[f"{team_role}_barrels"] += 1
            reset_barrel(team_role)

            embed = discord.Embed(
              title=":oil: Barrel reduced successfully! :oil:",
              description=f"**{team_role}** successfully reduces an oil barrel.",
              color=discord.Color.green()
            )
            embed.add_field(name="New Barrel Started", value=f":repeat: Your team starts with a new :oil: oil barrel with volume of **100 gallons**.", inline=False)
            embed.add_field(name="Barrels Reduced", value=f":oil: {db[f'{team_role}_barrels']} / 3", inline=True)
            await ctx.channel.send(embed=embed)

            # Check if they have filled 3 barrels
            if db[f"{team_role}_barrels"] == 3:
                embed = discord.Embed(
                  title="Congratulations!",
                  description=f"**{team_role}**, your team has successfully filled :oil: 3 barrels of oil! Screenshot this message and send to your FB Team GC to receive the next clue.",
                  color=discord.Color.gold()
                )
                embed.set_image(url="https://i.ibb.co/x7tqyFZ/image.png")
                await ctx.channel.send(embed=embed)
                return
        else:
            embed = discord.Embed(
              title=":fuelpump: Barrel Filling Failed :fuelpump:",
              description=f":x: :repeat: **{team_role}** failed to reduce the :oil: oil barrel correctly. Resetting to initial volume of **100** gallons!",
              color=discord.Color.red()
            )
            reset_barrel(team_role)
            await ctx.channel.send(embed=embed)
