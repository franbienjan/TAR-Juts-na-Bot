import discord
from replit import db
import json

# List of Teams
TEAMS = {
    'JUTS_TEAM_1',
    'JUTS_TEAM_2',
    'JUTS_TEAM_3',
    'JUTS_TEAM_4',
    'JUTS_TEAM_5',
    'JUTS_TEAM_6'
}

# Kampong contents in JSON format
kampongs_json = '''
{
    "1_content": "boatman",
    "1_boatman_img": "https://i.ibb.co/3yX8hQQ/image.png",
    "1_boatman_name": "Betong",
    "2_content": "boatman",
    "2_boatman_img": "https://i.ibb.co/K7pM5FQ/image.png",
    "2_boatman_name": "Alma",
    "3_content": "tempered glass",
    "4_content": "nothing",
    "5_content": "nothing",
    "6_content": "boatman",
    "6_boatman_img": "https://i.ibb.co/XF1GPTm/image.png",
    "6_boatman_name": "Juliana",
    "7_content": "nothing",
    "8_content": "nothing",
    "9_content": "boatman",
    "9_boatman_img": "https://i.ibb.co/4gX73Ct/image.png",
    "9_boatman_name": "Joel",
    "10_content": "nothing",
    "11_content": "clue",
    "11_clue": "https://i.ibb.co/k5WSnZm/JIGSAW-6.png",
    "12_content": "clue",
    "12_clue": "https://i.ibb.co/ct6crwW/JIGSAW-5.png",
    "13_content": "boatman",
    "13_boatman_img": "https://i.ibb.co/CQKkykv/image.png",
    "13_boatman_name": "Claudine",
    "14_content": "nothing",
    "15_content": "boatman",
    "15_boatman_img": "https://i.ibb.co/4YdjHX2/image.png",
    "15_boatman_name": "Angie",
    "16_content": "Shaira",
    "17_content": "boatman",
    "17_boatman_img": "https://i.ibb.co/rvH5Bwk/image.png",
    "17_boatman_name": "Rendon",
    "18_content": "boatman",
    "18_boatman_img": "https://i.ibb.co/F01XKmy/image.png",
    "18_boatman_name": "Miggy",
    "19_content": "nothing",
    "20_content": "boatman",
    "20_boatman_img": "https://i.ibb.co/NmXdnND/image.png",
    "20_boatman_name": "Samira",
    "21_content": "boatman",
    "21_boatman_img": "https://i.ibb.co/jhsrWhp/image.png",
    "21_boatman_name": "Lyca",
    "22_content": "tempered glass",
    "23_content": "clue",
    "23_clue": "https://i.ibb.co/f1ybB5c/JIGSAW-4.png",
    "24_content": "boatman",
    "24_boatman_img": "",
    "24_boatman_name": "Joel",
    "25_content": "clue",
    "25_clue": "https://i.ibb.co/RCkQNBx/JIGSAW-2.png",
    "26_content": "nothing",
    "27_content": "clue",
    "27_clue": "https://i.ibb.co/gMMLDd9/JIGSAW-1.png",
    "28_content": "tempered glass",
    "29_content": "boatman",
    "29_boatman_img": "https://i.ibb.co/cLphhdF/Screenshot-2024-09-22-at-3-41-46-PM.png",
    "29_boatman_name": "Valentine",
    "30_content": "clue",
    "30_clue": "https://i.ibb.co/TM4m31Z/JIGSAW-3.png",
    "31_content": "nothing",
    "32_content": "boatman",
    "32_boatman_img": "https://i.ibb.co/NnWZzWm/image.png",
    "32_boatman_name": "Ricci"
}
'''

# Load kampong data from JSON
kampongs = json.loads(kampongs_json)

# Helper function to check if a user has the "HOSTS" role
def has_hosts_role(member):
    return "GOLD_HOSTS" in [role.name for role in member.roles] if member else False

# Initialization command
def kampong_reset(ctx):
    if not has_hosts_role(ctx.author):
        "You do not have permission to initialize the game."

    # Initialize the database using individual keys for each team
    for team in TEAMS:
        db[f"{team}_temperedglasses"] = []
        db[f"{team}_location"] = None
        db[f"{team}_hasLeft"] = False

    db["express_pass_claimed"] = False
    db["boatmen_taken"] = []  # Separate array to track which boatmen are taken
    db["kampong_lock"] = False #game is no longer playable

    return "Game initialization completed successfully!"

# Helper function to get the team of a player
def get_player_team(member):
    if not member:
        return None
    for role in member.roles:
        if role.name in TEAMS:
            return role.name
    return None

# Update team location
def update_team_location(team, kampong_number):
    # Update the team's current kampong location in the database
    db[f"{team}_location"] = kampong_number

# Visit kampong handler
async def visit_kampong_handler(ctx, kampong_number):
    member_id = ctx.author.id
    guild = ctx.guild
    try:
        kampong_number = int(kampong_number)  # Ensure kampong_number is an integer
    except ValueError:
        await ctx.channel.send(":x: Please enter a valid kampong number.")

    if kampong_number < 1 or kampong_number > 32:
        await ctx.channel.send(":x: Please enter a valid kampong number between 1 and 32.")

    member = guild.get_member(member_id)
    if not member:
        await ctx.channel.send(":x: Member not found.")

    player_team = get_player_team(member)
    if not player_team:
        await ctx.channel.send(":x: You are not in a team. Please join a team to play.")

    if db.get(f"{player_team}_hasLeft", False):
        await ctx.channel.send(":x: You may no longer explore the Kampongs.")

    update_team_location(player_team, kampong_number)

    # Retrieve the kampong content
    content = kampongs.get(f"{kampong_number}_content", None)

    # Get the team's tempered glass list
    tempered_glasses = db.get(f"{player_team}_temperedglasses", [])

    if content == "tempered glass":
        response = discord.Embed(title=f"KAMPONG #{kampong_number}",description="",color=0xFAF5EF)
        response.add_field(name="Team", value=player_team, inline=True)
        if kampong_number not in tempered_glasses:
            tempered_glasses.append(kampong_number)
            db[f"{player_team}_temperedglasses"] = tempered_glasses  # Save updated team data to the database
            
            response.add_field(name=":sparkles: Oooh! A new tempered glass piece!", value="Your team found a new tempered glass piece in this Kampong.", inline=False)

        else:
            response.add_field(name=":x: You already have this!", value="Your team has already taken the tempered glass piece from this Kampong.", inline=False)

        response.add_field(name="", value="The first team to visit the Queen of Bangsamoro Pop and Queen of Tempered Glass, :woman_with_headscarf: **Shaira** :woman_with_headscarf:, somewhere in the Kampongs, after visiting and obtaining all three legendary tempered glass pieces will win the coveted **Express Pass**, which is valid until the fourth leg of the race.", inline=False)
        response.add_field(name="Number of Tempered Glass Pieces", value=f"{len(tempered_glasses)}/3", inline=False)
        response.set_thumbnail(url="https://i.ibb.co/hXc57ZL/image.png")
        await ctx.channel.send(embed=response)

    elif content == "Shaira":
        tempered_glass_count = len(tempered_glasses)
        response = discord.Embed(title=f"KAMPONG #{kampong_number}",description="",color=0xFFFF00)
        response.add_field(name="Team", value=player_team, inline=True)
        if db.get("express_pass_claimed", False):
            response.add_field(name="**:woman_with_headscarf: Shaira:**", value="The **Express Pass** has been taken! :cry:", inline=False)
            response.set_thumbnail(url="https://i.ibb.co/kB6Tb2g/Screenshot-2024-09-22-at-12-43-07-AM.png")
            await ctx.channel.send(embed=response)
        
        if tempered_glass_count >= 3:
            if not db.get("express_pass_claimed", False):
                db["express_pass_claimed"] = True
                response.add_field(name="**:woman_with_headscarf: Shaira:**", value=f"Congratulations, Team {player_team}! You have earned the **Express Pass**! Send a screenshot of this message to your Team GC to claim it", inline=False)
                response.set_thumbnail(url="https://i.ibb.co/kB6Tb2g/Screenshot-2024-09-22-at-12-43-07-AM.png")
                response.set_image(url="https://i.ibb.co/0D369YJ/Screenshot-2024-09-22-at-11-47-33-AM.png")
                await ctx.channel.send(embed=response)
            else:
                response.add_field(name="**:woman_with_headscarf: Shaira:**", value="The **Express Pass** has been taken! :cry:", inline=False)
                response.set_thumbnail(url="https://i.ibb.co/kB6Tb2g/Screenshot-2024-09-22-at-12-43-07-AM.png")
                await ctx.channel.send(embed=response)
        else:
            response.add_field(name="**:woman_with_headscarf: Shaira:**", value="You need 3 tempered glasses to claim the Express Pass. Please go back to me when you have all 3.", inline=False)
            response.add_field(name="Number of Tempered Glass Pieces", value=f"{len(tempered_glasses)}/3", inline=False)
            response.set_thumbnail(url="https://i.ibb.co/kB6Tb2g/Screenshot-2024-09-22-at-12-43-07-AM.png")
            await ctx.channel.send(embed=response)

    elif content == "clue":
        clue = kampongs.get(f"{kampong_number}_clue", None)
        if clue:
            response = discord.Embed(title=f"KAMPONG #{kampong_number}",description="",color=0x0F0000)
            response.add_field(name="Team", value=player_team, inline=True)
            response.add_field(name="", value="This photo shall represent the location of where you should go next. You may visit a boatman to take you to this place, or you may continue visiting other Kampongs to find another clue. ", inline=False)
            response.set_image(url=clue)
            await ctx.channel.send(embed=response)
        else:
            return f"No new clue found in Kampong {kampong_number}.", embed

    elif content == "boatman":

        response = discord.Embed(title=f"KAMPONG #{kampong_number}",description="",color=0x1035AC)
        response.add_field(name="Team", value=player_team, inline=True)
        boatmanName = kampongs.get(f"{kampong_number}_boatman_name", None)
        response.add_field(name="Boatman", value=boatmanName, inline=True)
        response.set_thumbnail(url=kampongs.get(f"{kampong_number}_boatman_img", None))
        
        if kampong_number in db["boatmen_taken"]:    
            response.add_field(name="", value="Sorry, no more trips today. Already finished my quota. Find another boatman!", inline=False)
        else:
            response.add_field(name=f":sailboat: Boatman **{boatmanName}:**", value="Hello, I can take you by water taxi to your next clue if you send me the correct location. However, first come, first served. Replace X with the name of your next location, in all caps, with no spaces: `$kampong-ride X`", inline=False)
            response.add_field(name="", value="**Note:** Once you are correct, there's no going back to the other Kampongs.", inline=False)
            response.add_field(name="", value="**Hint:** The Answer has multiple words, so type them together. Example: Brunei River, you must type `BRUNEIRIVER` with no spaces and all caps", inline=False)
        await ctx.channel.send(embed=response)

    else:
        response = discord.Embed(title=f"KAMPONG #{kampong_number}",description="",color=0xAA4A44)
        response.add_field(name="Team", value=player_team, inline=True)
        response.add_field(name="", value="There is nothing at this Kampong.", inline=False)
        await ctx.channel.send(embed=response)

# Kampongride handler
async def kampong_ride_handler(ctx, destination):
    member_id = ctx.author.id
    guild = ctx.guild
    member = guild.get_member(member_id)
    if not member:
        await ctx.channel.send(":x: Member not found.")

    player_team = get_player_team(member)
    if not player_team:
        await ctx.channel.send(":x: You are not in a team. Please join a team to play.")

    if db.get(f"{player_team}_hasLeft", False):
        await ctx.channel.send(":x: You may no longer explore the Kampongs.")

    # Retrieve team's current kampong location from the database
    team_location = db.get(f"{player_team}_location", None)

    if not team_location:
        await ctx.channel.send(f":x: Your team {player_team} needs to be at a kampong with a boatman to ride!")

    # Check if the kampong has a boatman
    if kampongs.get(f"{team_location}_content") == "boatman":
        response = discord.Embed(title=f"KAMPONG #{team_location}",description="",color=0x1035AC)
        boatmanName = kampongs.get(f"{team_location}_boatman_name")
        response.add_field(name="Team", value=player_team, inline=True)
        response.add_field(name="Boatman", value=boatmanName, inline=True)
        response.set_thumbnail(url=kampongs.get(f"{team_location}_boatman_img", None))
        
        if team_location in db["boatmen_taken"]:    
            response.add_field(name=f":sailboat: Boatman **{boatmanName}:**", value="Sorry, no more trips today. Already finished my quota. Find another boatman!", inline=False)
            await ctx.channel.send(embed=response)

        if destination.upper() != "MERCUDIRGAHAYU60":
            print(f"test {destination}")
            response.add_field(name=f":sailboat: Boatman **{boatmanName}:**", value="I'm sorry. I don't know where that is. Can you try again?", inline=False)
            await ctx.channel.send(embed=response)
            
        # Mark the boatman as taken
        db["boatmen_taken"].append(team_location)
        db[f"{player_team}_hasLeft"] = True

        response.add_field(name=f":sailboat: Boatman **{boatmanName}:**", value="Alright! Let's go!", inline=False)
        response.add_field(name="", value="Send a screenshot of this message to your Team GC to receive your next clue.", inline=False)
        response.set_image(url="https://i.ibb.co/Gn8P6DY/Memorial-Bandar-Seri-Begawan.png")
        await ctx.channel.send(embed=response)

    await ctx.channel.send(":x: There is no boatman available at this kampong.")

####################
## ENTRY FUNCTION ##
####################
# Function to process user messages and return results as an embed message
async def process_message(ctx):
    # Parse command details
    command_parts = ctx.content.split()
    command_name = command_parts[0].lower()
    command_args = command_parts[1:]

    #Note: issue with kampong lock
    if db["kampong-lock"] and command_name != "$kampong-reset":
        await ctx.channel.send(":lock: The Kampongs are closed now.")
    if command_name == "$kampong-reset":
        response = kampong_reset(ctx)
        await ctx.channel.send(response)
    elif command_name == "$visit-kampong":
        kampong_number = command_args[0]
        await visit_kampong_handler(ctx, kampong_number)
    elif command_name == "$kampong-ride":
        destination = command_args[0]
        await kampong_ride_handler(ctx, destination)
    elif command_name == "$kampong-lock":
        if not has_hosts_role(ctx.author):
            await ctx.channel.send("You do not have permission to initialize the game.")
        db["kampong_lock"] = True
        await ctx.channel.send(":lock: Kampong lock has been enabled. Only the owner of the bot can use the bot now.")