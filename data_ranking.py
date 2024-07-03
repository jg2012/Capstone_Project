import requests
import csv

#Rankings as of 07/03/2024

url = "https://api.sportradar.com/tennis/trial/v3/en/rankings.json?api_key=Tb8NbATTFv3OEA25r3C1hagLoZpNAMIS2uuYlKIA"
headers = {"accept": "application/json"}
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
else:
    print("Failed to retrieve data")
    data = None

if data:
    rankings = data.get('rankings', [])

    # Define the CSV file header
    headers = ['Type ID', 'Ranking Name', 'Year', 'Week', 'Gender', 'Rank', 'Movement', 'Points', 'Competitor ID', 'Competitor Name', 'Country', 'Country Code', 'Abbreviation']

    # Open a CSV file to write the data
    with open('tennis_rankings.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Write the header
        writer.writerow(headers)
        
        # Write the player data
        for ranking in rankings:
            type_id = ranking.get('type_id')
            name = ranking.get('name')
            year = ranking.get('year')
            week = ranking.get('week')
            gender = ranking.get('gender')
            
            competitor_rankings = ranking.get('competitor_rankings', [])
            for competitor_ranking in competitor_rankings:
                rank = competitor_ranking.get('rank')
                movement = competitor_ranking.get('movement')
                points = competitor_ranking.get('points')
                competitor = competitor_ranking.get('competitor', {})
                competitor_id = competitor.get('id')
                competitor_name = competitor.get('name')
                country = competitor.get('country')
                country_code = competitor.get('country_code')
                abbreviation = competitor.get('abbreviation')
                
                writer.writerow([type_id, name, year, week, gender, rank, movement, points, competitor_id, competitor_name, country, country_code, abbreviation])

    print("Data has been written to tennis_rankings.csv")
