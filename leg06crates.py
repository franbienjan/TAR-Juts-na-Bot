import discord
import random
import string
import json
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
  'JUTS_TEAM_2',
  'JUTS_TEAM_3'
}

with open('official-roles.json') as f:
  officialRoles = json.load(f)

with open('official-threads.json') as f:
  officialThreads = json.load(f)

# CRATES with image URLs for each one
# CRATES with specific image placeholders for each crate
CRATES = {
    "leg_1_crate_1": {"leg": "Leg 1", "image": "https://i.ibb.co/vBWz4mc/robin.png"},
    "leg_1_crate_2": {"leg": "Leg 1", "image": "https://i.ibb.co/DGVT4gk/sohighschool.png"},
    "leg_1_crate_3": {"leg": "Leg 1", "image": "https://i.ibb.co/HBr9Y9h/prophecy.png"},
    "leg_1_crate_4": {"leg": "Leg 1", "image": "https://i.ibb.co/B4cnHz0/peter.png"},
    "leg_1_crate_5": {"leg": "Leg 1", "image": "https://i.ibb.co/6NYRpnL/loml.png"},

    "leg_2_crate_1": {"leg": "Leg 2", "image": "https://i.ibb.co/hDXnPC6/thankyouaimee.png"},
    "leg_2_crate_2": {"leg": "Leg 2", "image": "https://i.ibb.co/tQK7tX6/imgonnagetyouback.png"},
    "leg_2_crate_3": {"leg": "Leg 2", "image": "https://i.ibb.co/WB6kj8H/clarabow.png"},
    "leg_2_crate_4": {"leg": "Leg 2", "image": "https://i.ibb.co/zPb82WN/blackdog.png"},
    "leg_2_crate_5": {"leg": "Leg 2", "image": "https://i.ibb.co/pZLdxm0/alchemy.png"},

    "leg_3_crate_1": {"leg": "Leg 3", "image": "https://i.ibb.co/G3sr3bF/smallestman.png"},
    "leg_3_crate_2": {"leg": "Leg 3", "image": "https://i.ibb.co/N9xM8LS/fortnight.png"},
    "leg_3_crate_3": {"leg": "Leg 3", "image": "https://i.ibb.co/4PCrhWg/chloeorsam.png"},
    "leg_3_crate_4": {"leg": "Leg 3", "image": "https://i.ibb.co/Rz259YK/cassandra.png"},
    "leg_3_crate_5": {"leg": "Leg 3", "image": "https://i.ibb.co/N3BTVK5/brokenheart.png"},

    "leg_4_crate_1": {"leg": "Leg 4", "image": "https://i.ibb.co/xhcSBw2/torturedpoets.png"},
    "leg_4_crate_2": {"leg": "Leg 4", "image": "https://i.ibb.co/m5qw9fy/ihateithere.png"},
    "leg_4_crate_3": {"leg": "Leg 4", "image": "https://i.ibb.co/bv499SV/freshout.png"},
    "leg_4_crate_4": {"leg": "Leg 4", "image": "https://i.ibb.co/vzpcPMs/butdaddy.png"},
    "leg_4_crate_5": {"leg": "Leg 4", "image": "https://i.ibb.co/sFc8hZK/bolter.png"},

    "leg_5_crate_1": {"leg": "Leg 5", "image": "https://i.ibb.co/cxS29dL/whosafraid.png"},
    "leg_5_crate_2": {"leg": "Leg 5", "image": "https://i.ibb.co/Mcq3F4h/solonglondon.png"},
    "leg_5_crate_3": {"leg": "Leg 5", "image": "https://i.ibb.co/HgF1t5B/myboyonly.png"},
    "leg_5_crate_4": {"leg": "Leg 5", "image": "https://i.ibb.co/CHRdknM/ilookinpeoples.png"},
    "leg_5_crate_5": {"leg": "Leg 5", "image": "https://i.ibb.co/qy34qnZ/downbad.png"},

    "leg_6_crate_1": {"leg": "Leg 6", "image": "https://i.ibb.co/w6mYV8T/icanfixhim.png"},
    "leg_6_crate_2": {"leg": "Leg 6", "image": "https://i.ibb.co/S6KDtDb/howdiditend.png"},
    "leg_6_crate_3": {"leg": "Leg 6", "image": "https://i.ibb.co/kq1JdX1/guiltyassin.png"},
    "leg_6_crate_4": {"leg": "Leg 6", "image": "https://i.ibb.co/XtJzBN9/florida.png"},
    "leg_6_crate_5": {"leg": "Leg 6", "image": "https://i.ibb.co/vx10h1B/albatross.png"}
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
            db["pontoons"][team] = []  # Clear the team's pontoon
            db["unclaimed_crates"].remove(crate) # Remove the claimed crate from the unclaimed list
            del released_crates[command]  # Remove the claimed crate command
            db["last_released_crates"] = released_crates  # Update the released crates
            await msg.channel.send(f"{msg.author.mention}, you already have a crate from that leg! All your crates are returned upstream.")
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
async def process_message(message, client):

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
        banjulPort = client.get_channel(officialThreads['LEG06-NEURALINK']) # TODO: Change to MAIN-LOBBY
        await manual_crate_release(banjulPort)

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
