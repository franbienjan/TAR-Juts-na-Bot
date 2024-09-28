import random
import discord
from replit import db

# Constants
DISTRICTS = ["ANABAR", "BAITI", "BUADA", "NIBOK", "UABOE"]
SOIL_TYPES = ["Clay A", "Clay B", "Sand A", "Sand B", "Silt A", "Silt B"]
SOIL_THRESHOLDS = (300, 400)

# Function to get team ID based on user roles
def get_team_id(member):
  for role in member.roles:
    if role.name.startswith("JUTS_TEAM_"):
      return role.name.split("_")[-1]
  return None

# Function to check if the pickaxe breaks based on district
def pickaxe_breaks(district):
  break_chances = {
    "ANABAR": 10,
    "BAITI": 20,
    "BUADA": 20,
    "NIBOK": 20,
    "UABOE": 7
  }
  rand_pickaxe = random.randint(1, 100)
  return rand_pickaxe <= break_chances[district]

# Function to generate soil samples based on district
def generate_soil_samples(district):
  samples = {soil: 0.0 for soil in SOIL_TYPES}
  if district == "ANABAR":
    soil_chance = random.randint(1, 90)
    if soil_chance <= 30:
      # Clay
      samples["Clay A"] = round(random.uniform(4, 20), 2)
      samples["Clay B"] = round(random.uniform(4, 20), 2)
    elif soil_chance <= 60:
      # Sand
      samples["Sand A"] = round(random.uniform(4, 20), 2)
      samples["Sand B"] = round(random.uniform(4, 20), 2)
    elif soil_chance <= 90:
      # Silt
      samples["Silt A"] = round(random.uniform(4, 20), 2)
      samples["Silt B"] = round(random.uniform(4, 20), 2)
  elif district == "BAITI":
    samples["Clay A"] = round(random.uniform(2, 12), 2)
    samples["Clay B"] = round(random.uniform(2, 12), 2)
    samples["Sand A"] = round(random.uniform(0, 4), 2)
    samples["Sand B"] = round(random.uniform(0, 4), 2)
    samples["Silt A"] = round(random.uniform(0, 4), 2)
    samples["Silt B"] = round(random.uniform(0, 4), 2)
  elif district == "BUADA":
    samples["Clay A"] = round(random.uniform(0, 4), 2)
    samples["Clay B"] = round(random.uniform(0, 4), 2)
    samples["Sand A"] = round(random.uniform(2, 12), 2)
    samples["Sand B"] = round(random.uniform(2, 12), 2)
    samples["Silt A"] = round(random.uniform(0, 4), 2)
    samples["Silt B"] = round(random.uniform(0, 4), 2)
  elif district == "NIBOK":
    samples["Clay A"] = round(random.uniform(0, 4), 2)
    samples["Clay B"] = round(random.uniform(0, 4), 2)
    samples["Sand A"] = round(random.uniform(0, 4), 2)
    samples["Sand B"] = round(random.uniform(0, 4), 2)
    samples["Silt A"] = round(random.uniform(2, 12), 2)
    samples["Silt B"] = round(random.uniform(2, 12), 2)
  elif district == "UABOE":
    for soil in samples:
      if random.random() >= 0.25:
        samples[soil] = round(random.uniform(0, 12), 2)
  return samples

# Function to calculate soil percentages
def calculate_percentages(soil_samples):
  total = sum(soil_samples.values())
  print("askjdslakdsladjald")
  print(soil_samples["Clay A"] + soil_samples["Clay B"])
  print((soil_samples["Clay A"] + soil_samples["Clay B"]) / total)
  if total == 0.00:
    return 0.00, 0.00, 0.00
  clay_percent = (soil_samples["Clay A"] + soil_samples["Clay B"]) / total * 100.00
  sand_percent = (soil_samples["Sand A"] + soil_samples["Sand B"]) / total * 100.00
  silt_percent = (soil_samples["Silt A"] + soil_samples["Silt B"]) / total * 100.00
  return clay_percent, sand_percent, silt_percent

# Function to add soil samples to the team
def add_soil_to_team(team_id, samples):
  team_data = db.get(f"soilteam_{team_id}", {"soil_samples": {soil: 0.0 for soil in SOIL_TYPES}, "submitted": False})
  for soil, amount in samples.items():
    team_data["soil_samples"][soil] += amount
  db[f"soilteam_{team_id}"] = team_data

# Function to get the current total soil for a team
def get_team_soil_total(team_id):
  team_data = db.get(f"soilteam_{team_id}", {"soil_samples": {soil: 0.0 for soil in SOIL_TYPES}, "submitted": False})
  return round(sum(team_data["soil_samples"].values()), 2)

# Function to get the current total soil per type for a team
def get_team_soil_per_type(team_id):
  team_data = db.get(f"soilteam_{team_id}")
  return team_data.get("soil_samples", {})

# Function to reset the soil samples for a team
def reset_team_soil(team_id):
  db[f"soilteam_{team_id}"] = {"soil_samples": {soil: 0.0 for soil in SOIL_TYPES}, "submitted": False}

# Function to check if soil has been submitted
def is_soil_submitted(team_id):
  team_data = db.get(f"soilteam_{team_id}", {"soil_samples": {soil: 0.0 for soil in SOIL_TYPES}, "submitted": False})
  return team_data["submitted"]

# Function to reset all values for all teams
def reset_all_teams():
  keys_to_delete = [key for key in db.keys() if key.startswith("soilteam_")]
  for key in keys_to_delete:
      del db[key]

def get_soil_classification(clay_percent, silt_percent, sand_percent):
  # Determine the soil type based on USDA Soil Texture Triangle rules
  if sand_percent >= 85 and clay_percent < 10:
    return "SAND"
  elif 70 <= sand_percent <= 90 and 0 <= silt_percent <= 30 and 0 <= clay_percent <= 15:
    return "LOAMYSAND"
  elif 52 <= sand_percent <= 85 and 0 <= silt_percent <= 50 and 7 <= clay_percent <= 20:
    return "SANDYLOAM"
  elif 7 <= clay_percent <= 27 and 28 <= silt_percent <= 50 and 23 <= sand_percent <= 52:
    return "LOAM"
  elif 0 <= sand_percent <= 50 and 50 <= silt_percent <= 88 and 0 <= clay_percent <= 27:
    return "SILTLOAM"
  elif sand_percent <= 20 and silt_percent >= 80 and clay_percent <= 12:
    return "SILT"
  elif sand_percent >= 45 and silt_percent <= 20 and 20 <= clay_percent <= 35:
    return "SANDYCLAYLOAM"
  elif 20 <= sand_percent <= 45 and 15 <= silt_percent <= 53 and 27 <= clay_percent <= 40:
    return "CLAYLOAM"
  elif sand_percent <= 20 and silt_percent >= 40 and 27 <= clay_percent <= 40:
    return "SILTYCLAYLOAM"
  elif sand_percent >= 45 and silt_percent <= 20 and 35 <= clay_percent <= 55:
    return "SANDYCLAY"
  elif sand_percent <= 20 and silt_percent >= 40 and clay_percent >= 40:
    return "SILTYCLAY"
  elif clay_percent >= 40 and sand_percent <= 45 and silt_percent <= 40:
    return "CLAY"
  else:
    return "UNKNOWN"  # In case the values don't match any category

####################
## ENTRY FUNCTION ##
####################
# Function to process user messages and return results as an embed message
async def process_message(message):

  author = message.author
  team_id = get_team_id(message.author)
  if team_id is None:
    await message.channel.send(f":x: {author.mention}, you need to be in a team to play this game!")
    return

  if message.content.startswith("$excavate "):
    if is_soil_submitted(team_id):
      await message.channel.send(f":x: {author.mention}, your team must identify the soil you submitted, before excavating again.")
      return

    district = message.content.split(" ")[1].upper()
    if district not in DISTRICTS:
      await message.channel.send(f":x: {author.mention}, invalid district. Choose from {', '.join(DISTRICTS)}")
      return

    if pickaxe_breaks(district):
      await message.channel.send(f":x: :pick: {author.mention}, your pickaxe breaks! You were not able to excavate the phosphate rock.")
      return

    samples = generate_soil_samples(district)
    add_soil_to_team(team_id, samples)
    total_soil = get_team_soil_total(team_id)

    if total_soil > 400:
      reset_team_soil(team_id)
      await message.channel.send(f":x: :pick: {author.mention}, your team have now went above **400 grams**. The sieve is overwhelmed and cannot handle the soil test anymore. Your soil is not counted. Try again.")
    else:
      soil_per_type = get_team_soil_per_type(team_id)
      clay_percent, sand_percent, silt_percent = calculate_percentages(samples)
      embed = discord.Embed(title=":pick: EXCAVATION :pick:", description=f"**{author.mention}**, you have excavated for your team: \n" + ",\n".join([f"{round(amount, 2)} grams of {soil}" for soil, amount in samples.items() if amount > 0]), color=0x0000ff)
      embed.add_field(name="Total Per Soil Type", value=",\n".join([f"{round(amount, 2)} grams of {soil}" for soil, amount in soil_per_type.items() if amount > 0]), inline=False)
      embed.add_field(name="Total Soil", value=f"{total_soil} grams", inline=False)
      await message.channel.send(embed=embed)

  elif message.content.startswith("$submit-soil"):
    if is_soil_submitted(team_id):
      await message.channel.send("You have already submitted your soil for testing.")
      return

    total_soil = get_team_soil_total(team_id)
    if total_soil < 300:
      await message.channel.send("There are not enough soil sample for the results to be conclusive. Try again.")
    elif total_soil >= 300:
      team_data = db[f"soilteam_{team_id}"]
      team_data["submitted"] = True
      db[f"soilteam_{team_id}"] = team_data
      await message.channel.send("You have submitted your soil for testing. You must now guess what type of soil you have.")

  elif message.content.startswith("$dump-soil"):
    if is_soil_submitted(team_id):
      await message.channel.send("The soil is not in your possession anymore.")
      return

    reset_team_soil(team_id)
    await message.channel.send("You have dumped all your soil.")

  elif message.content.startswith("$identify-soil"):
    if not is_soil_submitted(team_id):
      await message.channel.send("You need to submit your soil before identifying it.")
      return

    soil_guess = message.content.split(" ")[1].upper()
    if soil_guess not in [
      "SAND", "LOAMYSAND", "SILTLOAM", "SILT", "SANDYLOAM", "SANDYCLAYLOAM", "LOAM",
      "SANDYCLAY", "CLAYLOAM", "SILTYCLAYLOAM", "CLAY", "SILTYCLAY"
    ]:
      await message.channel.send("Invalid soil type. Please try again.")
      return

    # For the purpose of this demo, let's say the answer is "CLAY".
    # Implement USDA Triangle Calculations here to check the soil type.
    team_data = db[f"soilteam_{team_id}"]
    clay_percent, sand_percent, silt_percent = calculate_percentages(team_data["soil_samples"])
    correct_soil = get_soil_classification(clay_percent, silt_percent, sand_percent)
    print("____________________________")
    print(soil_guess)
    print(correct_soil)
    print(clay_percent)
    print(sand_percent)
    print(silt_percent)
    if soil_guess == correct_soil:
      await message.channel.send(f"Congratulations! You've correctly identified the soil as {correct_soil}.")
    else:
      await message.channel.send(f"Incorrect guess. The soil is not {soil_guess}. Try again!")

    reset_team_soil(team_id)
  
  elif message.content.startswith("$soil-reset"):
    reset_all_teams()
    await message.channel.send("All soil data for teams have been reset!")