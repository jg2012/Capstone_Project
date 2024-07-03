import requests
import csv
import os

# Function to extract ID segments
def extract_id(full_id):
    return full_id.split(':')[-1] if full_id else ''

url = "https://api.sportradar.com/tennis/trial/v3/en/competitors/sr%3Acompetitor%3A14882/summaries.json?api_key=Tb8NbATTFv3OEA25r3C1hagLoZpNAMIS2uuYlKIA"
headers = {"accept": "application/json"}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    summaries = data.get('summaries', [])

    # Ensure the directory exists
    output_dir = '.'  # Change this to your desired directory
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    output_file = os.path.join(output_dir, 'tennis_summaries.csv')

    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = [
            'Event ID', 'Start Time', 'Confirmed', 'Sport ID', 'Sport Name', 
            'Category ID', 'Category Name', 'Competition ID', 'Competition Name', 
            'Parent ID', 'Type', 'Gender', 'Level', 'Season ID', 'Season Name', 
            'Start Date', 'End Date', 'Year', 'Competition ID', 'Stage Order', 
            'Stage Type', 'Stage Phase', 'Round Name', 'Group ID', 'Group Name', 
            'Best Of', 'Venue ID', 'Venue Name', 'City Name', 'Country Name', 
            'Country Code', 'Timezone', 'Competitor ID', 'Competitor Name', 
            'Country', 'Country Code', 'Abbreviation', 'Qualifier', 'Seed', 
            'Bracket Number', 'Status', 'Match Status', 'Home Score', 'Away Score', 
            'Winner ID', 'Period Scores', 'Aces', 'Backhand Errors', 
            'Backhand Unforced Errors', 'Backhand Winners', 'Breakpoints Won', 
            'Double Faults', 'Drop Shot Unforced Errors', 'Drop Shot Winners', 
            'First Serve Points Won', 'First Serve Successful', 'Forehand Errors', 
            'Forehand Unforced Errors', 'Forehand Winners', 'Games Won', 
            'Groundstroke Errors', 'Groundstroke Unforced Errors', 
            'Groundstroke Winners', 'Lob Unforced Errors', 'Lob Winners', 
            'Max Games In A Row', 'Max Points In A Row', 'Overhead Stroke Errors', 
            'Overhead Stroke Unforced Errors', 'Overhead Stroke Winners', 
            'Points Won', 'Points Won From Last 10', 'Return Errors', 'Return Winners', 
            'Second Serve Points Won', 'Second Serve Successful', 'Service Games Won', 
            'Service Points Lost', 'Service Points Won', 'Tiebreaks Won', 
            'Total Breakpoints', 'Volley Unforced Errors', 'Volley Winners'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for summary in summaries:
            sport_event = summary.get('sport_event', {})
            context = sport_event.get('sport_event_context', {})
            venue = sport_event.get('venue', {})
            status = summary.get('sport_event_status', {})
            competitors = sport_event.get('competitors', [])
            statistics = summary.get('statistics', {}).get('totals', {}).get('competitors', [])

            common_data = {
                'Event ID': extract_id(sport_event.get('id', '')),
                'Start Time': sport_event.get('start_time', ''),
                'Confirmed': sport_event.get('start_time_confirmed', ''),
                'Sport ID': extract_id(context.get('sport', {}).get('id', '')),
                'Sport Name': context.get('sport', {}).get('name', ''),
                'Category ID': extract_id(context.get('category', {}).get('id', '')),
                'Category Name': context.get('category', {}).get('name', ''),
                'Competition ID': extract_id(context.get('competition', {}).get('id', '')),
                'Competition Name': context.get('competition', {}).get('name', ''),
                'Parent ID': extract_id(context.get('competition', {}).get('parent_id', '')),
                'Type': context.get('competition', {}).get('type', ''),
                'Gender': context.get('competition', {}).get('gender', ''),
                'Level': context.get('competition', {}).get('level', ''),
                'Season ID': extract_id(context.get('season', {}).get('id', '')),
                'Season Name': context.get('season', {}).get('name', ''),
                'Start Date': context.get('season', {}).get('start_date', ''),
                'End Date': context.get('season', {}).get('end_date', ''),
                'Year': context.get('season', {}).get('year', ''),
                'Stage Order': context.get('stage', {}).get('order', ''),
                'Stage Type': context.get('stage', {}).get('type', ''),
                'Stage Phase': context.get('stage', {}).get('phase', ''),
                'Round Name': context.get('round', {}).get('name', ''),
                'Group ID': extract_id(context.get('groups', [{}])[0].get('id', '')),
                'Group Name': context.get('groups', [{}])[0].get('name', ''),
                'Best Of': context.get('mode', {}).get('best_of', ''),
                'Venue ID': extract_id(venue.get('id', '')),
                'Venue Name': venue.get('name', ''),
                'City Name': venue.get('city_name', ''),
                'Country Name': venue.get('country_name', ''),
                'Country Code': venue.get('country_code', ''),
                'Timezone': venue.get('timezone', ''),
                'Status': status.get('status', ''),
                'Match Status': status.get('match_status', ''),
                'Home Score': status.get('home_score', ''),
                'Away Score': status.get('away_score', ''),
                'Winner ID': extract_id(status.get('winner_id', '')),
                'Period Scores': str(status.get('period_scores', []))
            }

            for competitor in competitors:
                competitor_id = competitor.get('id', '')
                competitor_stats = next((item for item in statistics if item.get('id') == competitor.get('id')), {}).get('statistics', {})
                competitor_data = {
                    'Competitor ID': extract_id(competitor.get('id', '')),
                    'Competitor Name': competitor.get('name', ''),
                    'Country': competitor.get('country', ''),
                    'Country Code': competitor.get('country_code', ''),
                    'Abbreviation': competitor.get('abbreviation', ''),
                    'Qualifier': competitor.get('qualifier', ''),
                    'Seed': competitor.get('seed', ''),
                    'Bracket Number': competitor.get('bracket_number', ''),
                    'Aces': competitor_stats.get('aces', ''),
                    'Backhand Errors': competitor_stats.get('backhand_errors', ''),
                    'Backhand Unforced Errors': competitor_stats.get('backhand_unforced_errors', ''),
                    'Backhand Winners': competitor_stats.get('backhand_winners', ''),
                    'Breakpoints Won': competitor_stats.get('breakpoints_won', ''),
                    'Double Faults': competitor_stats.get('double_faults', ''),
                    'Drop Shot Unforced Errors': competitor_stats.get('drop_shot_unforced_errors', ''),
                    'Drop Shot Winners': competitor_stats.get('drop_shot_winners', ''),
                    'First Serve Points Won': competitor_stats.get('first_serve_points_won', ''),
                    'First Serve Successful': competitor_stats.get('first_serve_successful', ''),
                    'Forehand Errors': competitor_stats.get('forehand_errors', ''),
                    'Forehand Unforced Errors': competitor_stats.get('forehand_unforced_errors', ''),
                    'Forehand Winners': competitor_stats.get('forehand_winners', ''),
                    'Games Won': competitor_stats.get('games_won', ''),
                    'Groundstroke Errors': competitor_stats.get('groundstroke_errors', ''),
                    'Groundstroke Unforced Errors': competitor_stats.get('groundstroke_unforced_errors', ''),
                    'Groundstroke Winners': competitor_stats.get('groundstroke_winners', ''),
                    'Lob Unforced Errors': competitor_stats.get('lob_unforced_errors', ''),
                    'Lob Winners': competitor_stats.get('lob_winners', ''),
                    'Max Games In A Row': competitor_stats.get('max_games_in_a_row', ''),
                    'Max Points In A Row': competitor_stats.get('max_points_in_a_row', ''),
                    'Overhead Stroke Errors': competitor_stats.get('overhead_stroke_errors', ''),
                    'Overhead Stroke Unforced Errors': competitor_stats.get('overhead_stroke_unforced_errors', ''),
                    'Overhead Stroke Winners': competitor_stats.get('overhead_stroke_winners', ''),
                    'Points Won': competitor_stats.get('points_won', ''),
                    'Points Won From Last 10': competitor_stats.get('points_won_from_last_10', ''),
                    'Return Errors': competitor_stats.get('return_errors', ''),
                    'Return Winners': competitor_stats.get('return_winners', ''),
                    'Second Serve Points Won': competitor_stats.get('second_serve_points_won', ''),
                    'Second Serve Successful': competitor_stats.get('second_serve_successful', ''),
                    'Service Games Won': competitor_stats.get('service_games_won', ''),
                    'Service Points Lost': competitor_stats.get('service_points_lost', ''),
                    'Service Points Won': competitor_stats.get('service_points_won', ''),
                    'Tiebreaks Won': competitor_stats.get('tiebreaks_won', ''),
                    'Total Breakpoints': competitor_stats.get('total_breakpoints', ''),
                    'Volley Unforced Errors': competitor_stats.get('volley_unforced_errors', ''),
                    'Volley Winners': competitor_stats.get('volley_winners', '')
                }

                # Combine the dictionaries and write to CSV
                writer.writerow({**common_data, **competitor_data})

    print(f"Data has been written to {output_file}")
else:
    print("Failed to retrieve data: HTTP Status Code", response.status_code)
