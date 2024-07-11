import pandas as pd

# Paths to the CSV files
csv_files = {
    "atp_tennis": "data/atp_tennis.csv",
    "competitor_profile": "data/tennis_competitor_profile.csv",
    "rankings": "data/tennis_rankings.csv",
    "summaries": "data/cleaned_tennis_summaries.csv"
}

# Load the CSV files into DataFrames
dfs = {name: pd.read_csv(path) for name, path in csv_files.items()}

# Print column names to inspect the data
for name, df in dfs.items():
    print(f"Columns in {name}: {df.columns.tolist()}")

# Standardize column names
for name, df in dfs.items():
    df.columns = df.columns.str.lower().str.replace(' ', '_')

# Print column names again after standardization
for name, df in dfs.items():
    print(f"Standardized columns in {name}: {df.columns.tolist()}")

# Fill missing values or drop rows/columns as needed
for name, df in dfs.items():
    df.fillna(method='ffill', inplace=True)  # Forward fill as an example, adjust as necessary

# Ensure relational integrity
# Example: ensure 'player_id' consistency across tables
# First, identify the primary key column in 'competitor_profile'
if 'competitor_profile' in dfs:
    competitor_profile_columns = dfs['competitor_profile'].columns
    print(f"Competitor profile columns: {competitor_profile_columns}")
    
    # Assuming one of these columns is the primary key, adjust as necessary
    potential_keys = ['player_id', 'id', 'competitor_id']
    player_id_column = next((col for col in potential_keys if col in competitor_profile_columns), None)
    
    if player_id_column:
        player_ids = set(dfs['competitor_profile'][player_id_column])
        for name, df in dfs.items():
            if player_id_column in df.columns:
                dfs[name] = df[df[player_id_column].isin(player_ids)]
    else:
        print("No suitable player_id column found in competitor_profile.")
else:
    print("competitor_profile table not found in CSV files.")

# Save the cleaned DataFrames back to new CSV files
output_paths = {name: f"data/cleaned_{name}.csv" for name in csv_files.keys()}
for name, df in dfs.items():
    df.to_csv(output_paths[name], index=False)

print("Data cleaning complete. Cleaned files saved as:")
for name, path in output_paths.items():
    print(f"{name}: {path}")