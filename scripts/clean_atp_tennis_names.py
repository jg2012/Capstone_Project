import pandas as pd
from fuzzywuzzy import process, fuzz
from tqdm import tqdm

# Load the datasets
rankings_df = pd.read_csv('data/cleaned_rankings.csv')
atp_tennis_df = pd.read_csv('data/cleaned_atp_tennis.csv')
competitor_profile_df = pd.read_csv('data/cleaned_competitor_profile.csv')
tennis_summaries_df = pd.read_csv('data/cleaned_tennis_summaries.csv')

# Normalizing player names by converting to lowercase and stripping any extra spaces
rankings_df['name_normalized'] = rankings_df['name'].str.lower().str.strip()
atp_tennis_df['player_1_normalized'] = atp_tennis_df['player_1'].str.lower().str.strip()
atp_tennis_df['player_2_normalized'] = atp_tennis_df['player_2'].str.lower().str.strip()
competitor_profile_df['name_normalized'] = competitor_profile_df['name'].str.lower().str.strip()
tennis_summaries_df['competitor_name_normalized'] = tennis_summaries_df['Competitor Name'].str.lower().str.strip()

# Function to apply fuzzy matching and find the best match for a player name
def fuzzy_match_player(name, player_list, threshold=70):  # Adjusted threshold to 70
    match, score = process.extractOne(name, player_list, scorer=fuzz.token_sort_ratio)
    return match if score >= threshold else None

# Function to apply fuzzy matching in batches with a progress bar
def fuzzy_match_batch(df, reference_names, batch_size=1000):
    matches_1 = []
    matches_2 = []
    for start in tqdm(range(0, len(df), batch_size), desc="Processing batches"):
        batch = df.iloc[start:start+batch_size].copy()
        batch.loc[:, 'player_1_matched'] = batch['player_1_normalized'].apply(fuzzy_match_player, args=(reference_names,))
        batch.loc[:, 'player_2_matched'] = batch['player_2_normalized'].apply(fuzzy_match_player, args=(reference_names,))
        matches_1.extend(batch['player_1_matched'])
        matches_2.extend(batch['player_2_matched'])
    return matches_1, matches_2

# Lists of player names from each dataset
rankings_player_names = rankings_df['name_normalized'].unique()
competitor_profile_names = competitor_profile_df['name_normalized'].unique()
tennis_summaries_names = tennis_summaries_df['competitor_name_normalized'].unique()

# Apply fuzzy matching for player_1 and player_2 in ATP Tennis dataset
matches_1, matches_2 = fuzzy_match_batch(atp_tennis_df, rankings_player_names, batch_size=1000)

# Add the matched player names back to the ATP Tennis dataframe
atp_tennis_df['player_1_matched'] = matches_1
atp_tennis_df['player_2_matched'] = matches_2

# Combine all matched player names for merging
all_matched_players = pd.concat([pd.Series(matches_1), pd.Series(matches_2)]).dropna().unique()

# Filter datasets to include only the matched player names
filtered_rankings_df = rankings_df[rankings_df['name_normalized'].isin(all_matched_players)]
filtered_competitor_profile_df = competitor_profile_df[competitor_profile_df['name_normalized'].isin(all_matched_players)]
filtered_tennis_summaries_df = tennis_summaries_df[tennis_summaries_df['competitor_name_normalized'].isin(all_matched_players)]

# Debugging: Print the number of matched players
print(f"Number of matched players in ATP Tennis: {len(all_matched_players)}")
print(f"Filtered Rankings size: {filtered_rankings_df.shape}")
print(f"Filtered Competitor Profile size: {filtered_competitor_profile_df.shape}")
print(f"Filtered Tennis Summaries size: {filtered_tennis_summaries_df.shape}")

# Get the unmatched names from the Competitor Profile dataset
unmatched_competitor_names = set(competitor_profile_df['name_normalized']) - set(all_matched_players)
unmatched_competitor_names = pd.Series(list(unmatched_competitor_names))

print("Unmatched Competitor Profile names:")
print(unmatched_competitor_names.head(20))  # Display the first 20 unmatched names for inspection

# Merge the filtered datasets
filtered_rankings_profile_df = filtered_rankings_df.merge(filtered_competitor_profile_df, on='name_normalized', how='inner')
filtered_rankings_profile_summaries_df = filtered_rankings_profile_df.merge(filtered_tennis_summaries_df, left_on='name_normalized', right_on='competitor_name_normalized', how='inner')

# Merge with ATP Tennis data using fuzzy matched player names
final_merged_df_1 = filtered_rankings_profile_summaries_df.merge(atp_tennis_df, left_on='name_normalized', right_on='player_1_matched', how='inner')
final_merged_df_2 = filtered_rankings_profile_summaries_df.merge(atp_tennis_df, left_on='name_normalized', right_on='player_2_matched', how='inner')

# Combine both merges into a final dataframe
final_combined_fuzzy_df = pd.concat([final_merged_df_1, final_merged_df_2], ignore_index=True)

# Save the final combined dataframe to a CSV file
final_combined_fuzzy_df.to_csv('data/final_combined_fuzzy_df.csv', index=False)

# Displaying the first few rows of the final combined dataframe
print(final_combined_fuzzy_df.head())
