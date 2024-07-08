import requests
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Function to extract ID segments
def extract_id(full_id):
    return full_id.split(':')[-1] if full_id else ''

# Get API key from environment variable
api_key = os.getenv("SPORTRADAR_API_KEY")
if not api_key:
    raise ValueError("No API key provided. Please set the SPORTRADAR_API_KEY environment variable.")

url = f"https://api.sportradar.com/tennis/trial/v3/en/rankings.json?api_key={api_key}"
headers = {"accept": "application/json"}

print(f"Requesting data from URL: {url}")
response = requests.get(url, headers=headers)

try:
    print(f"Response status code: {response.status_code}")
    response.raise_for_status()  # Check if the request was successful
    data = response.json()
    print("Data successfully retrieved and parsed.")
except requests.exceptions.HTTPError as errh:
    print(f"HTTP Error: {errh}")
    print(response.text)
except requests.exceptions.ConnectionError as errc:
    print(f"Error Connecting: {errc}")
except requests.exceptions.Timeout as errt:
    print(f"Timeout Error: {errt}")
except requests.exceptions.RequestException as err:
    print(f"Request Exception: {err}")
except ValueError as errj:
    print(f"JSON Decode Error: {errj}")
    print(response.text)
else:
    print("Processing the data...")
    try:
        rankings = data['rankings'][0]['competitor_rankings']
        # Extract relevant data
        rows = []
        for player in rankings:
            rank = player.get('rank')
            movement = player.get('movement')
            points = player.get('points')
            competitor = player.get('competitor', {})
            name = competitor.get('name')
            country = competitor.get('country')
            country_code = competitor.get('country_code', '')  # Default to empty string if missing
            abbreviation = competitor.get('abbreviation', '')  # Default to empty string if missing
            rows.append([rank, movement, points, name, country, country_code, abbreviation])

        # Create a DataFrame
        df = pd.DataFrame(rows, columns=['Rank', 'Movement', 'Points', 'Name', 'Country', 'Country Code', 'Abbreviation'])

        # Display the DataFrame
        print(df)

        # Optional: Save the DataFrame to a CSV file
        df.to_csv('tennis_rankings.csv', index=False)
    except KeyError as e:
        print(f"KeyError: {e}. The response might not contain the expected data structure.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")