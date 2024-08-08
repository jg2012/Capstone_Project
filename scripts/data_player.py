import pandas as pd

def split_player_name(df, player_column):
    # Check if the specified column exists
    if player_column not in df.columns:
        print(f"Column '{player_column}' not found in DataFrame. Available columns:", df.columns)
        return df
    
    # Split the specified player column into 'Last Name' and 'First Initial'
    names = df[player_column].str.split(' ', n=1, expand=True)
    last_name_col = f"{player_column}_Last_Name"
    first_initial_col = f"{player_column}_First_Initial"
    df[last_name_col] = names[0]
    df[first_initial_col] = names[1].str[0]
    df.drop(columns=[player_column], inplace=True)
    return df

def process_atp_file(input_file, output_file):
    # Read the CSV file
    df = pd.read_csv(input_file)
    
    # Print column names for debugging
    print(f"Processing file: {input_file}")
    print("Columns in DataFrame:", df.columns)
    
    # Split the player names for Player_1 and Player_2
    if 'Player_1' in df.columns and 'Player_2' in df.columns:
        df = split_player_name(df, 'Player_1')
        df = split_player_name(df, 'Player_2')
    else:
        print("Required columns 'Player_1' and 'Player_2' are not present in the DataFrame.")
    
    # Convert 'Date' to datetime if the column exists
    if 'Date' in df.columns:
        try:
            df['Date'] = pd.to_datetime(df['Date'])
        except Exception as e:
            print(f"Error converting 'Date' column: {e}")
    
    # Convert 'Score' to float if the column exists
    if 'Score' in df.columns:
        try:
            df['Score'] = df['Score'].astype(float)
        except Exception as e:
            print(f"Error converting 'Score' column: {e}")
    
    # Save the modified DataFrame to a new CSV file
    df.to_csv(output_file, index=False)

# File paths
input_file = 'data/atp_tennis.csv'
output_file = 'data/atp_tennis_modified.csv'

# Process the file
process_atp_file(input_file, output_file)

print("ATP Tennis file has been processed and saved successfully.")
