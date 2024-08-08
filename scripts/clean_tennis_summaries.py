import pandas as pd
import ast

# Load the tennis_summaries CSV file
file_path = "data/cleaned_tennis_summaries.csv"
df = pd.read_csv(file_path)

# Function to process period_scores column
def process_period_scores(period_scores_str):
    try:
        period_scores = ast.literal_eval(period_scores_str)
        scores = {}
        for i, period in enumerate(period_scores):
            scores[f'home_score_set_{i+1}'] = period.get('home_score')
            scores[f'away_score_set_{i+1}'] = period.get('away_score')
        return scores
    except (ValueError, SyntaxError):
        return {}

# Apply the function to period_scores column and create new columns
scores_df = df['period_scores'].apply(process_period_scores).apply(pd.Series)

# Concatenate the new columns with the original DataFrame
df = pd.concat([df, scores_df], axis=1)

# Drop the original period_scores column if needed
df.drop(columns=['period_scores'], inplace=True)

# Save the cleaned DataFrame to a new CSV file
output_path = "data/cleaned_tennis_summaries.csv"
df.to_csv(output_path, index=False)

print("Data cleaning complete. Cleaned file saved as:", output_path)