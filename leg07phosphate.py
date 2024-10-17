import random
import discord
from replit import db

# Constants
DISTRICTS = ["ANABAR", "BAITI", "BUADA", "NIBOK", "UABOE"]
SOIL_TYPES = ["Clay A", "Clay B", "Sand A", "Sand B", "Silt A", "Silt B"]
SOIL_TYPES_EQUIVALENT = {"Clay A" : "2mm", "Clay B" : "0.5mm", "Sand A" : "0.05mm", "Sand B" : "0.02mm", "Silt A" : "0.002mm", "Silt B" : "Pan"}
SOIL_MINIMUM_THRESHOLDS = 10 #300
SOIL_MAXIMUM_THRESHOLDS = 100 #400

# List of Teams
TEAMS = {
  'JUTS_AVAIL',
  'JUTS_BEN_AND_BEN',
  'JUTS_BUKO_JUTS',
  'JUTS_JUTATAYS',
  'JUTS_JUTS_GIVE_ME_A_REASON',
  'JUTS_KHAO_KHEOW_STARS',
  'JUTS_NEW_KIDS_ON_THE_BLOCK',
  'JUTS_NUMBERS',
  'JUTS_SIMPLE_LIFE',
  'JUTS_TEAM_1',
  'JUTS_TEAM_2'
}

# Add this to your constants
ALL_SOIL_TYPES = [
    "SAND", "LOAMYSAND", "SILTLOAM", "SILT", "SANDYLOAM", "SANDYCLAYLOAM", 
    "LOAM", "SANDYCLAY", "CLAYLOAM", "SILTYCLAYLOAM", "CLAY", "SILTYCLAY"
]

# Function to add a successfully identified soil type to the team's progress
def add_identified_soil(team_id, soil_type):
    team_data = db.get(f"soilteam_{team_id}", {"identified_soils": []})
    if soil_type not in team_data["identified_soils"]:
        team_data["identified_soils"].append(soil_type)
        db[f"soilteam_{team_id}"] = team_data
        return True
    return False

# Function to get the identified soils for a team
def get_identified_soils(team_id):
    team_data = db.get(f"soilteam_{team_id}", {"identified_soils": []})
    return team_data["identified_soils"]

# Function to check if the team has completed their soil identification mission
def has_completed_identification(team_id):
    identified_soils = get_identified_soils(team_id)
    return len(identified_soils) >= 6

# Function to get team ID based on user roles
def get_team_id(member):
  for role in member.roles:
    if role.name in TEAMS:
      return role.name
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

# Function to reset EVERYTHING in a team
def reset_team_values(team_id):
  db[f"soilteam_{team_id}"] = {"soil_samples": {soil: 0.0 for soil in SOIL_TYPES}, "submitted": False, "identified_soils": []}

# Function to reset the soil samples for a team
def reset_team_soil(team_id):
  # Fetch the current team data, defaulting to an empty structure if not found
  team_data = db.get(f"soilteam_{team_id}", {"soil_samples": {}, "submitted": False, "identified_soils": []})

  # Preserve the identified_soils
  identified_soils = team_data.get("identified_soils", [])

  # Reset the rest of the structure
  team_data = {
      "soil_samples": {soil: 0.0 for soil in SOIL_TYPES},  # Reset soil samples
      "submitted": False,  # Reset submitted flag
      "identified_soils": identified_soils  # Keep previously identified soils
  }

  # Save the updated structure back to the database
  db[f"soilteam_{team_id}"] = team_data

# Function to check if soil has been submitted
def is_soil_submitted(team_id):
  team_data = db.get(f"soilteam_{team_id}", {"soil_samples": {soil: 0.0 for soil in SOIL_TYPES}, "submitted": False})
  return team_data["submitted"]

# Function to reset all values for all teams
def reset_all_teams():
  for team in teams:
    reset_team_values(team)

def get_soil_classification(clay_percent, silt_percent, sand_percent):
  # Determine the soil type based on USDA Soil Texture Triangle rules
  
  if 0 <= clay_percent < 5:
    if 90 <= sand_percent <= 100:
      return "SAND"
    elif 75 <= sand_percent < 90:
      return "LOAMYSAND"
    elif 70 <= sand_percent < 75:
      return "SANDYLOAM|LOAMYSAND" #dual answer
    elif 50 <= sand_percent < 70 or 30 <= silt_percent < 50:
      return "SANDYLOAM"
    elif 50 <= silt_percent < 80:
      return "SILTLOAM"
    elif 80 <= silt_percent <= 100:
      return "SILT"
  elif 5 <= clay_percent < 10:
    if 90 <= sand_percent <= 100:
      return "SAND"
    elif 80 <= sand_percent < 90:
      return "LOAMYSAND"
    elif 75 <= sand_percent < 80:
      return "LOAMYSAND|SANDYLOAM" #dual answer
    elif 52.5 <= sand_percent < 75:
      return "SANDYLOAM" 
    elif 45 <= sand_percent < 52.5 or 42.5 <= silt_percent < 50:
      return "LOAM"
    elif 50 <= silt_percent < 80:
      return "SILTLOAM"
    elif 80 <= silt_percent <= 100:
      return "SILT"
  elif 10 <= clay_percent < 12.5:
    if 82.5 <= sand_percent <= 100:
      return "LOAMYSAND"
    elif 80 <= sand_percent < 82.5:
      return "LOAMYSAND|SANDYLOAM" #dual answer
    elif 52.5 <= sand_percent < 80:
      return "SANDYLOAM"
    elif 40 <= sand_percent < 52.5 or 37.5 <= silt_percent < 50:
      return "LOAM"
    elif 50 <= silt_percent < 80:
      return "SILTLOAM"
    elif 80 <= silt_percent <= 100:
      return "SILT"
  elif 12.5 <= clay_percent < 15:
    if 85 <= sand_percent <= 100:
      return "LOAMYSAND"
    elif 82.5 <= sand_percent < 85:
      return "LOAMYSAND|SANDYLOAM" #dual answer
    elif 52.5 <= sand_percent < 82.5:
      return "SANDYLOAM"
    elif 37.5 <= sand_percent < 52.5 or 35 <= silt_percent < 50:
      return "LOAM"
    elif 50 <= silt_percent <= 100:
      return "SILTLOAM"
  elif 15 <= clay_percent < 20:
    if 52.5 <= sand_percent <= 100:
      return "SANDYLOAM"
    elif 35 <= sand_percent < 52.5 or 32.5 <= silt_percent < 50:
      return "LOAM"
    elif 50 <= silt_percent <= 100:
      return "SILTLOAM"
  elif 20 <= clay_percent < 27.5:
    if 0 <= silt_percent < 27.5:
      return "SANDYCLAYLOAM"
    elif 27.5 <= silt_percent < 50:
      return "LOAM"
    elif 50 <= silt_percent <= 100:
      return "SILTLOAM"
  elif 27.5 <= clay_percent < 35:
    if 45 <= sand_percent <= 100:
      return "SANDYCLAYLOAM"
    elif 20 <= sand_percent < 45:
      return "CLAYLOAM"
    elif 0 <= silt_percent < 20:
      return "SILTYCLAYLOAM"
  elif 35 <= clay_percent < 40:
    if 45 <= sand_percent <= 100:
      return "SANDYCLAY"
    elif 20 <= sand_percent < 45:
      return "CLAYLOAM"
    elif 0 <= sand_percent < 20:
      return "SILTYCLAYLOAM"
  elif 40 <= clay_percent < 55:
    if 45 <= sand_percent <= 100:
      return "SANDYCLAY"
    elif 20 <= sand_percent < 45 or 15 <= silt_percent < 40:
      return "CLAY"
    elif 40 <= silt_percent <= 100:
      return "SILTYCLAY"
  elif 55 <= clay_percent < 60:
    if 0 <= silt_percent < 40:
      return "CLAY"
    elif 40 <= silt_percent <= 100:
      return "SILTYCLAY"
  elif 60 <= clay_percent <= 100:
    return "CLAY"
  else:
    return "UNKNOWN"
  
  return "UNKNOWN"

# Helper function to check if the user's answer is in the valid soil types
def is_correct_soil_type(user_input, valid_soil_type):
    valid_types = valid_soil_type.split('|')  # Split by "|"
    return user_input.upper() in valid_types  # Check if the input matches any

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

    if total_soil >= SOIL_MAXIMUM_THRESHOLDS:
      reset_team_soil(team_id)
      await message.channel.send(f":x: :pick: {author.mention}, your team have now went above **{SOIL_MAXIMUM_THRESHOLDS} grams**. The sieve is overwhelmed and cannot handle the soil test anymore. Your soil is not counted. Try again.")
    else:
      soil_per_type = get_team_soil_per_type(team_id)
      clay_percent, sand_percent, silt_percent = calculate_percentages(samples)
      embed = discord.Embed(
          title=f":pick: EXCAVATION IN {district} :pick:", 
          description=f"**{author.mention}**, you have excavated for your team: \n" +
          ",\n".join([f"{amount:.2f} grams remaining in Pan" if soil == "Silt B" 
                      else f"{amount:.2f} grams of size {SOIL_TYPES_EQUIVALENT[soil]}" 
                      for soil, amount in samples.items() if amount > 0]), 
          color=0x0000ff
      )
      embed.add_field(name=f":scales: Total Soil ({total_soil:.2f} grams) Per Sieve :scales:", value="", inline=False)
      for soil, amount in soil_per_type.items():
        if amount > 0:
          embed.add_field(name=SOIL_TYPES_EQUIVALENT[soil], value=f"{amount:.2f} grams", inline=True)
      identified_soils = get_identified_soils(team_id)
      if len(identified_soils) > 0:
        embed.add_field(name=f":notepad_spiral: Discovery Log: Owned Soil Types ({len(identified_soils)}/6) :notepad_spiral:", value=",\n".join(identified_soils), inline=False)
      await message.channel.send(embed=embed)

  elif message.content.startswith("$submit-soil"):
    if is_soil_submitted(team_id):
      await message.channel.send("You have already submitted your soil for testing.")
      return

    total_soil = get_team_soil_total(team_id)
    if total_soil < SOIL_MINIMUM_THRESHOLDS:
      await message.channel.send("There are not enough soil sample for the results to be conclusive. Try again.")
    elif total_soil >= SOIL_MINIMUM_THRESHOLDS:
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

  elif message.content.startswith("$identify-soil "):
    if not is_soil_submitted(team_id):
      await message.channel.send("You need to submit your soil before identifying it.")
      return

    soil_guess = ""
    try:
      soil_guess = message.content.split(" ")[1].upper()
      if soil_guess not in ALL_SOIL_TYPES:
        await message.channel.send("Invalid soil type. Please try again.")
        return
    except ValueError:
      await message.channel.send("Invalid input.")

    # Implement USDA Triangle Calculations here to check the soil type.
    team_data = db[f"soilteam_{team_id}"]
    clay_percent, sand_percent, silt_percent = calculate_percentages(team_data["soil_samples"])
    correct_soil = get_soil_classification(clay_percent, silt_percent, sand_percent)

    if is_correct_soil_type(soil_guess, correct_soil):
      # Add the correctly identified soil type to the team's progress
      isNewSoil = add_identified_soil(team_id, soil_guess)
      identified_soils = get_identified_soils(team_id)
      if has_completed_identification(team_id):
        await message.channel.send(f"🎉 {author.mention}, congratulations! Your team has identified all 6 different soil types and completed the mission! INSERT FINAL CLUE HERE")
      else:
        if isNewSoil:
          embed = discord.Embed(title=":mag: SOIL IDENTIFIED! :mag_right:", color=0x00ff00)
          embed.add_field(name="Newly Identified Soil Type", value=f"{soil_guess}", inline=False)
          embed.add_field(name=":notepad_spiral: Discovery Log: Owned Soil Types", value=f"{len(identified_soils)} out of 6", inline=False)
        else:
          embed = discord.Embed(title=":mag: SOIL IDENTIFIED! :mag_right:", description="However, you already have this soil type in your possession. Try again!", color=0x00ff00)
          embed.add_field(name=":notepad_spiral: Discovery Log: Owned Soil Types", value=f"{len(identified_soils)} out of 6", inline=False)
        embed.add_field(name="Identified Soil Types", value=",\n".join(identified_soils), inline=False)
        await message.channel.send(embed=embed)
    else:
      await message.channel.send(f"Incorrect guess. The soil is not {soil_guess}. Try again!")

    reset_team_soil(team_id)
  
  elif message.content.startswith("$soil-reset"):
    reset_all_teams()
    await message.channel.send("All soil data for teams have been reset!")