import csv
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
api_key = os.getenv("SPORTRADAR_API_KEY")
if not api_key:
    raise ValueError("No API key provided. Please set the SPORTRADAR_API_KEY environment variable.")

# Function to extract ID segments
def extract_id(full_id):
    return full_id.split(':')[-1] if full_id else ''

# URL with hidden API key
url = f"https://api.sportradar.com/tennis/trial/v3/en/competitors/sr%3Acompetitor%3A407573/profile.json?api_key={api_key}"

headers = {"accept": "application/json"}
response = requests.get(url, headers=headers)
data = response.json()

# Define the CSV file name
csv_file = "tennis_competitor_profile.csv"

# Extract the data
competitor = data["competitor"]
info = data["info"]
competitor_rankings = data["competitor_rankings"][0]

# Write data to CSV
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    
    # Write headers
    headers = [
        "ID", "Name", "Country", "Abbreviation", "Gender",
        "Pro Year", "Handedness", "Highest Singles Ranking", "Highest Doubles Ranking",
        "Weight", "Height", "Date of Birth", "Highest Singles Ranking Date", "Highest Doubles Ranking Date",
        "Current Singles Rank", "Rank Movement", "Rank Points", "Competitor ID", "Rank Name", "Rank Type", "Race Ranking",
        "Year", "Surface Type", "Competitions Played (Surface)", "Competitions Won (Surface)", "Matches Played (Surface)", "Matches Won (Surface)",
        "Competitions Played (Overall)", "Competitions Won (Overall)", "Matches Played (Overall)", "Matches Won (Overall)"
    ]
    writer.writerow(headers)
    
    # Write general data
    general_data = [
        extract_id(competitor["id"]), competitor["name"], competitor["country"], competitor["abbreviation"], competitor["gender"],
        info["pro_year"], info["handedness"], info["highest_singles_ranking"], info.get("highest_doubles_ranking"),
        info["weight"], info["height"], info["date_of_birth"], info["highest_singles_ranking_date"], info.get("highest_doubles_ranking_date"),
        competitor_rankings["rank"], competitor_rankings["movement"], competitor_rankings["points"], extract_id(competitor_rankings["competitor_id"]), competitor_rankings["name"], competitor_rankings["type"], competitor_rankings["race_ranking"]
    ]
    
    # Iterate through periods
    for period in data["periods"]:
        year = period["year"]
        overall_stats = period["statistics"]
        
        # Iterate through surfaces
        for surface in period["surfaces"]:
            surface_type = surface["type"]
            surface_stats = surface["statistics"]
            
            # Combine general data with specific year and surface data
            row = general_data + [
                year, surface_type, surface_stats["competitions_played"], surface_stats["competitions_won"], surface_stats["matches_played"], surface_stats["matches_won"],
                overall_stats["competitions_played"], overall_stats["competitions_won"], overall_stats["matches_played"], overall_stats["matches_won"]
            ]
            
            writer.writerow(row)

print(f"Data written to {csv_file}")
