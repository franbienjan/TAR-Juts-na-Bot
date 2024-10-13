import discord
from replit import db

# List of Teams
TEAMS = {
    'JUTS_TEAM_1',
    'JUTS_TEAM_2'
}

# Manually set codes and corresponding URLs for each image
PLACEHOLDER_URLS = [
    {"code": "123456", "url": "https://example.com/random1.png"},
    {"code": "234567", "url": "https://example.com/random2.png"},
    {"code": "345678", "url": "https://example.com/random3.png"},
    {"code": "456789", "url": "https://example.com/random4.png"},
    {"code": "567890", "url": "https://example.com/random5.png"},
    {"code": "678901", "url": "https://example.com/random6.png"},
    {"code": "789012", "url": "https://example.com/random7.png"},
    {"code": "890123", "url": "https://example.com/random8.png"},
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

# Function to reset the game (for admin use)
async def reset_game(ctx):
    db["team_data"] = {team: {"level": 1, "claimed_images": []} for team in TEAMS}
    db["level1_images"] = LEVEL_1_IMAGES.copy()
    db["level2_images"] = LEVEL_2_IMAGES.copy()
    db["level3_images"] = LEVEL_3_IMAGES.copy()

    embed = discord.Embed(title="Game Reset", description="The game has been reset successfully.", color=discord.Color.green())
    await ctx.channel.send(embed=embed)

# Function to start the game
async def start_game(ctx):
    await reset_game(ctx)  # Reset the game first

    # Show available images for Level 1
    images = db["level1_images"]
    available_codes = ', '.join(img["code"] for img in images)
    embed = discord.Embed(title="Level 1 - Available Images", description=available_codes or "No available images.", color=discord.Color.blue())
    await ctx.channel.send(embed=embed)

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
async def process_message(message):
    if message.author.bot:
        return

    if message.content.startswith("$charles-start"):
        await start_game(message)
    elif message.content.startswith("$charles-lap1 "):
        await claim_image(message, 1, message.content.split(" ")[1].upper())
    elif message.content.startswith("$charles-2ndlap "):
        await claim_image(message, 2, message.content.split(" ")[1].upper())
    elif message.content.startswith("$charles-finallap "):
        await claim_image(message, 3, message.content.split(" ")[1].upper())
    elif message.content.startswith("$charles-show-all "):
        await show_available_images(message, int(message.content.split(" ")[1]))
