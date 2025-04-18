#Author: Nathan Vu
#Purpose is to test the cleaning aspect of the data i.e: clean.py
import os
from clean import clean_and_save_stats

# Sample test data
player_name = "LeBron James"
team_name = "Lakers"
raw_data = """
LeBron James Stats:
    Points: 25
    Rebounds: 8
    Assists: 7
    Steals: 1
    Blocks: 1
    Turnovers: 3
    Field Goal: 50%
    Three-Point: 40%
"""

# Save this sample raw data to a text file
raw_data_filename = f"{player_name.lower().replace(' ', '_')}_raw_data.txt"
with open(raw_data_filename, "w", encoding="utf-8") as f:
    f.write(raw_data)

# Testing the clean_and_save_stats function
def test_clean_and_save_stats():
    # Test the function with CSV output
    print("\nTesting with CSV output...")
    clean_and_save_stats(player_name, team_name, raw_data_filename, output_format="csv")
    
    # Check if CSV file is created and contains expected data
    csv_filename = f"cleaned_data/{player_name.lower().replace(' ', '_')}_stats.csv"
    assert os.path.exists(csv_filename), f"CSV file {csv_filename} was not created!"
    
    # Read and print the content of the CSV to verify it
    with open(csv_filename, "r", encoding="utf-8") as f:
        print(f.read())


# Run the test
test_clean_and_save_stats()
