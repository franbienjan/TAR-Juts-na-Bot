import discord
import random
import asyncio
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
    "leg_1_crate_1": {"leg": "Leg 1", "image": "leg1a"},
    "leg_1_crate_2": {"leg": "Leg 1", "image": "leg1b"},
    "leg_1_crate_3": {"leg": "Leg 1", "image": "leg1c"},
    "leg_1_crate_4": {"leg": "Leg 1", "image": "leg1d"},
    "leg_1_crate_5": {"leg": "Leg 1", "image": "leg1e"},

    "leg_2_crate_1": {"leg": "Leg 2", "image": "leg2a"},
    "leg_2_crate_2": {"leg": "Leg 2", "image": "leg2b"},
    "leg_2_crate_3": {"leg": "Leg 2", "image": "leg2c"},
    "leg_2_crate_4": {"leg": "Leg 2", "image": "leg2d"},
    "leg_2_crate_5": {"leg": "Leg 2", "image": "leg2e"},

    "leg_3_crate_1": {"leg": "Leg 3", "image": "leg3a"},
    "leg_3_crate_2": {"leg": "Leg 3", "image": "leg3b"},
    "leg_3_crate_3": {"leg": "Leg 3", "image": "leg3c"},
    "leg_3_crate_4": {"leg": "Leg 3", "image": "leg3d"},
    "leg_3_crate_5": {"leg": "Leg 3", "image": "leg3e"},

    "leg_4_crate_1": {"leg": "Leg 4", "image": "leg4a"},
    "leg_4_crate_2": {"leg": "Leg 4", "image": "leg4b"},
    "leg_4_crate_3": {"leg": "Leg 4", "image": "leg4c"},
    "leg_4_crate_4": {"leg": "Leg 4", "image": "leg4d"},
    "leg_4_crate_5": {"leg": "Leg 4", "image": "leg4e"},

    "leg_5_crate_1": {"leg": "Leg 5", "image": "leg5a"},
    "leg_5_crate_2": {"leg": "Leg 5", "image": "leg5b"},
    "leg_5_crate_3": {"leg": "Leg 5", "image": "leg5c"},
    "leg_5_crate_4": {"leg": "Leg 5", "image": "leg5d"},
    "leg_5_crate_5": {"leg": "Leg 5", "image": "leg5e"},

    "leg_6_crate_1": {"leg": "Leg 6", "image": "leg6a"},
    "leg_6_crate_2": {"leg": "Leg 6", "image": "leg6b"},
    "leg_6_crate_3": {"leg": "Leg 6", "image": "leg6c"},
    "leg_6_crate_4": {"leg": "Leg 6", "image": "leg6d"},
    "leg_6_crate_5": {"leg": "Leg 6", "image": "leg6e"},
}

TIMEOUT = 10  # Time between crate releases -- SHOULD BE 30

def reset_game():
  """Clear all crates and reset all team pontoons."""
  db["pontoons"] = {team: [] for team in TEAMS}
  db["unclaimed_crates"] = list(CRATES.keys())
  db["game_active"] = False

async def send_crates(channel, client):
  """Randomly send 2 crates to the channel every N seconds."""
  while db["game_active"]:
      print("Sending crates...")

      # Check the number of unclaimed crates
      unclaimed_count = len(db["unclaimed_crates"])
      if unclaimed_count == 0:
          await channel.send("All crates have been claimed!")
          break

      # If there are two or more crates left, continue as before
      if unclaimed_count >= 2:
          crate_a, crate_b = random.sample(db["unclaimed_crates"], 2)

          # Generate unique claim commands
          command_a = f"$crate {generate_random_code()}"
          command_b = f"$crate {generate_random_code()}"

          # Display crate images with unique commands
          embed = discord.Embed(title="Two Crates on Rafts")
          embed.add_field(name="Crate A", value=f"{CRATES[crate_a]['image']} \nClaim with `{command_a}`")
          embed.add_field(name="Crate B", value=f"{CRATES[crate_b]['image']} \nClaim with `{command_b}`")

          await channel.send(embed=embed)

          # Wait for player to claim crates for a set period
          claimed = set()  # To track claims made during this period
          timeout_period = TIMEOUT + 5  # Add a few extra seconds to the timeout

          while timeout_period > 0 and db["game_active"]:
              try:
                  msg = await client.wait_for("message", check=lambda m: m.content.startswith("$crate "), timeout=1.0)
                  claimed_command = msg.content
                  claimed_time = msg.created_at

                  if claimed_command == command_a and crate_a not in claimed:
                      claimed.add(crate_a)  # Mark this crate as claimed
                      await claim_crate(msg, crate_a, claimed_time)
                  elif claimed_command == command_b and crate_b not in claimed:
                      claimed.add(crate_b)  # Mark this crate as claimed
                      await claim_crate(msg, crate_b, claimed_time)
                  else:
                      await msg.channel.send(f"{msg.author.mention}, that command is invalid for this crate batch or already claimed.")
              except asyncio.TimeoutError:
                  timeout_period -= 1  # Decrease timeout period if no valid message is received

          # After the time is up, inform that the next set of crates will be released
          await asyncio.sleep(TIMEOUT)




def generate_random_code(length=4):
  """Generate a random string of fixed length."""
  return ''.join(random.choices(string.ascii_uppercase, k=length))

async def claim_crate(msg, crate, claimed_time):
  team_role = next((role for role in msg.author.roles if role.name.startswith("JUTS_")), None)
  if not team_role:
      await msg.channel.send(f"{msg.author.mention}, you are not in a team.")
      return

  team = team_role.name
  pontoon = db["pontoons"].get(team, [])

  # Check if the crate is already claimed
  if crate in db["unclaimed_crates"]:
      # Check if the team already has a crate from the same leg
      crate_leg = CRATES[crate]["leg"]
      if any(CRATES[c]["leg"] == crate_leg for c in pontoon):
          await msg.channel.send(f"{msg.author.mention}, you already have a crate from that leg! All your crates are returned upstream. {claimed_time}")
          db["pontoons"][team] = []  # Clear the team's pontoon
      else:
          pontoon.append(crate)
          db["pontoons"][team] = pontoon
          db["unclaimed_crates"].remove(crate)  # Remove the claimed crate from the unclaimed list
          await msg.channel.send(f"{msg.author.mention} claimed a crate for team {team}. {claimed_time}")

          # Check if they have won
          if len(pontoon) == 6:
              await msg.channel.send(f"Team {team} has completed all 6 crates and crossed the Atlantic! {claimed_time}")
  else:
      await msg.channel.send(f"{msg.author.mention}, this crate has already been claimed by another team. {claimed_time}")


####################
## ENTRY FUNCTION ##
####################
# Function to process user messages and return results as an embed message
async def process_message(message, client):

    if message.content.startswith("$crate-start") and "GOLD_HOSTS" in [role.name for role in message.author.roles]:
      db["game_active"] = True
      await message.channel.send("The game has started!")
      await send_crates(message.channel, client)

    if message.content.startswith("$crate-reset") and "GOLD_HOSTS" in [role.name for role in message.author.roles]:
      reset_game()
      await message.channel.send("The game has been reset.")

    if message.content.startswith("$crate-release") and "GOLD_HOSTS" in [role.name for role in message.author.roles]:
      crate_a, crate_b = random.sample(db["unclaimed_crates"], 2)
      embed = discord.Embed(title="Manual Crate Release")
      embed.add_field(name="Crate A", value="Claim with `$crate A`")
      embed.add_field(name="Crate B", value="Claim with `$crate B`")
      embed.set_image(url=CRATES[crate_a]["image"])
      embed.set_thumbnail(url=CRATES[crate_b]["image"])
      await message.channel.send(embed=embed)

    # Players can view their current pontoons
    if message.content.startswith("$view_pontoon"):
      team_role = next((role for role in message.author.roles if role.name.startswith("JUTS_")), None)
      if not team_role:
          await message.channel.send(f"{message.author.mention}, you are not in a team.")
          return

      team = team_role.name
      pontoon = db["pontoons"].get(team, [])
      if not pontoon:
          await message.channel.send(f"Team {team} has no crates on their pontoon.")
      else:
          crate_details = [f"{crate}" for crate in pontoon]  # Removed leg info
          await message.channel.send(f"Team {team}'s pontoon: \n" + "\n".join(crate_details))

    # Hosts (ADMIN) can view all pontoons
    if message.content.startswith("$view_all_pontoons") and "GOLD_HOSTS" in [role.name for role in message.author.roles]:
      pontoons = db["pontoons"]
      if not pontoons:
          await message.channel.send("No pontoons currently have any crates.")
      else:
          for team, pontoon in pontoons.items():
              if pontoon:
                  crate_details = [f"{CRATES[crate]['leg']} - {crate}" for crate in pontoon]
                  await message.channel.send(f"Team {team}'s pontoon: \n" + "\n".join(crate_details))
