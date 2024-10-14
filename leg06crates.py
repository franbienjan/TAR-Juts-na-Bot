import discord
import random
import string
from replit import db

# List of Teams
TEAMS = {
    'JUTS_TEAM_1',
    'JUTS_TEAM_2',
    'JUTS_TEAM_3',
    'JUTS_TEAM_4',
    'JUTS_TEAM_5',
    'JUTS_TEAM_6'
}

# CRATES with image URLs for each one
# CRATES with specific image placeholders for each crate
CRATES = {
    "leg_1_crate_1": {"leg": "Leg 1", "image": "https://i.ibb.co/GnQTGq0/01-Medal-of-Valor-Brunei.png"},
    "leg_1_crate_2": {"leg": "Leg 1", "image": "https://i.ibb.co/6RK0Vmw/01-Selos-Roadblock.png"},
    "leg_1_crate_3": {"leg": "Leg 1", "image": "https://i.ibb.co/PC9hwgL/01-Mercu-Dirgahayu.png"},
    "leg_1_crate_4": {"leg": "Leg 1", "image": "https://i.ibb.co/HpDWw5q/01-Tempered-Glass.png"},
    "leg_1_crate_5": {"leg": "Leg 1", "image": "https://i.ibb.co/5R9r2Tw/01-Kampong-North.png"},

    "leg_2_crate_1": {"leg": "Leg 2", "image": "https://i.ibb.co/8XrFVdx/02-Umbrella.png"},
    "leg_2_crate_2": {"leg": "Leg 2", "image": "https://i.ibb.co/Lr5FQTc/02-I-Beams.png"},
    "leg_2_crate_3": {"leg": "Leg 2", "image": "https://i.ibb.co/xhynMPN/02-Sacred-Heart.png"},
    "leg_2_crate_4": {"leg": "Leg 2", "image": "https://i.ibb.co/wNPfdmV/02-Polaroid-Cameras.png"},
    "leg_2_crate_5": {"leg": "Leg 2", "image": "https://i.ibb.co/3S23vWJ/02-Buoy.png"},

    "leg_3_crate_1": {"leg": "Leg 3", "image": "https://i.ibb.co/GMRK24D/03-Qatar-Sandwich.png"},
    "leg_3_crate_2": {"leg": "Leg 3", "image": "https://i.ibb.co/Bntq82Q/03-Agal.png"},
    "leg_3_crate_3": {"leg": "Leg 3", "image": "https://i.ibb.co/QpkJBsv/03-Gear.png"},
    "leg_3_crate_4": {"leg": "Leg 3", "image": "https://i.ibb.co/kSJGr9Y/03-Planggana.png"},
    "leg_3_crate_5": {"leg": "Leg 3", "image": "https://i.ibb.co/QmpTD0Z/03-David-Star.png"},

    "leg_4_crate_1": {"leg": "Leg 4", "image": "https://i.ibb.co/ftpB9XP/04-Charles-Leclerc-IG.png"},
    "leg_4_crate_2": {"leg": "Leg 4", "image": "https://i.ibb.co/NpnPjpt/04-Popcorn.png"},
    "leg_4_crate_3": {"leg": "Leg 4", "image": "https://i.ibb.co/Jyf8kwd/04-Ferrari.png"},
    "leg_4_crate_4": {"leg": "Leg 4", "image": "https://i.ibb.co/7YGBJcK/04-Direction-Circuit-Map.png"},
    "leg_4_crate_5": {"leg": "Leg 4", "image": "https://i.ibb.co/0VxJpxc/04-Hydraulic-Jack.png"},

    "leg_5_crate_1": {"leg": "Leg 5", "image": "https://i.ibb.co/5RVmv78/wall.png"},
    "leg_5_crate_2": {"leg": "Leg 5", "image": "https://i.ibb.co/5RVmv78/wall.png"},
    "leg_5_crate_3": {"leg": "Leg 5", "image": "https://i.ibb.co/5RVmv78/wall.png"},
    "leg_5_crate_4": {"leg": "Leg 5", "image": "https://i.ibb.co/5RVmv78/wall.png"},
    "leg_5_crate_5": {"leg": "Leg 5", "image": "https://i.ibb.co/5RVmv78/wall.png"},

    "leg_6_crate_1": {"leg": "Leg 6", "image": "https://i.ibb.co/FVjGPYZ/06-Safety-Vest.png"},
    "leg_6_crate_2": {"leg": "Leg 6", "image": "https://i.ibb.co/Y0pRC70/06-Rocket.png"},
    "leg_6_crate_3": {"leg": "Leg 6", "image": "https://i.ibb.co/MRPBhjJ/06-Kora.png"},
    "leg_6_crate_4": {"leg": "Leg 6", "image": "https://i.ibb.co/100XwrV/06-Bananas.png"},
    "leg_6_crate_5": {"leg": "Leg 6", "image": "https://i.ibb.co/QQ1s7mP/06-Kapuso.png"}
}

# Function to get team ID based on user roles
def get_team_id(member):
  for role in member.roles:
    if role.name in TEAMS:
      return role.name
  return None

def reset_game():
  """Clear all crates and reset all team pontoons."""
  db["pontoons"] = {team: [] for team in TEAMS}
  db["unclaimed_crates"] = list(CRATES.keys())
  db["game_active"] = False

async def manual_crate_release(channel):
    """Manually release 2 random crates."""
    if not db["game_active"]:
        await channel.send("The game is not active. Start the game with `$crate-start`.")
        return

    unclaimed_count = len(db["unclaimed_crates"])
    if unclaimed_count == 0:
        await channel.send("All crates have been claimed!")
        return

    # If there are two or more crates left, continue
    if unclaimed_count >= 2:
        crate_a, crate_b = random.sample(db["unclaimed_crates"], 2)

        # Generate unique claim commands
        command_a = generate_random_code()
        command_b = generate_random_code()

        # Display crate images with unique commands
        embed1 = discord.Embed(title="Crate A")
        embed1.add_field(name="Claim with command:", value=f"$crate-claim {command_a}")
        embed1.set_image(url=f"{CRATES[crate_a]['image']}")
        embed2 = discord.Embed(title="Crate B")
        embed2.add_field(name="Claim with command:", value=f"$crate-claim {command_b}")
        embed2.set_image(url=f"{CRATES[crate_b]['image']}")

        await channel.send(embeds=[embed1, embed2])

        # Track released crates in the database
        db["last_released_crates"] = {command_a: crate_a, command_b: crate_b}

def generate_random_code(length=4):
  """Generate a random string of fixed length."""
  return ''.join(random.choices(string.ascii_uppercase, k=length))

async def claim_crate(msg):
    command = msg.content.split()[1]
    released_crates = db.get("last_released_crates", {})

    # Check if the command matches a recently released crate
    if command not in released_crates:
        await msg.channel.send(f"{msg.author.mention}, that command is invalid or the crate has already been claimed.")
        return

    crate = released_crates[command]
    team = get_team_id(msg.author)
    pontoon = db["pontoons"].get(team, [])

    # Check if the crate is already claimed
    if crate in db["unclaimed_crates"]:
        # Check if the team already has a crate from the same leg
        crate_leg = CRATES[crate]["leg"]
        if any(CRATES[c]["leg"] == crate_leg for c in pontoon):
            await msg.channel.send(f"{msg.author.mention}, you already have a crate from that leg! All your crates are returned upstream.")
            db["pontoons"][team] = []  # Clear the team's pontoon
        else:
            pontoon.append(crate)
            db["pontoons"][team] = pontoon
            db["unclaimed_crates"].remove(crate)  # Remove the claimed crate from the unclaimed list
            del released_crates[command]  # Remove the claimed crate command
            db["last_released_crates"] = released_crates  # Update the released crates
            await msg.channel.send(f"{msg.author.mention} claimed a crate for team {team}.")

            # Check if they have won
            if len(pontoon) == 6:
                await msg.channel.send(f"Team {team} has completed all 6 crates and crossed the Atlantic!")
    else:
        await msg.channel.send(f"{msg.author.mention}, this crate has already been claimed by another team.")


####################
## ENTRY FUNCTION ##
####################
# Function to process user messages and return results as an embed message
async def process_message(message):

    author = message.author
    team = get_team_id(author)
    if team is None:
        await message.channel.send(f":x: {author.mention}, you need to be in a team to play this game!")
        return

    if message.content.startswith("$crate-start") and "GOLD_HOSTS" in [role.name for role in message.author.roles]:
        db["game_active"] = True
        await message.channel.send("The game has started!")

    if message.content.startswith("$crate-reset") and "GOLD_HOSTS" in [role.name for role in message.author.roles]:
        reset_game()
        await message.channel.send("The game has been reset.")

    if message.content.startswith("$crate-release") and "GOLD_HOSTS" in [role.name for role in message.author.roles]:
        await manual_crate_release(message.channel)

    if message.content.startswith("$crate-claim"):
        await claim_crate(message)

    # Players can view their current pontoons
    if message.content.startswith("$view-pontoon"):
        pontoon = db["pontoons"].get(team, [])
        if not pontoon:
            await message.channel.send(f"Team {team} has no crates on their pontoon.")
        else:
            crate_details = [f"{crate}" for crate in pontoon]
            await message.channel.send(f"Team {team}'s pontoon: \n" + "\n".join(crate_details))

    # Hosts (ADMIN) can view all pontoons
    if message.content.startswith("$view-all-pontoons") and "GOLD_HOSTS" in [role.name for role in message.author.roles]:
        pontoons = db["pontoons"]
        if not pontoons:
            await message.channel.send("No pontoons currently have any crates.")
        else:
            for team, pontoon in pontoons.items():
                if pontoon:
                    crate_details = [f"{CRATES[crate]['leg']} - {crate}" for crate in pontoon]
                    await message.channel.send(f"Team {team}'s pontoon: \n" + "\n".join(crate_details))
