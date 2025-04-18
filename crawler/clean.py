#Author: Nathan Vu
#File not needed to get data from NBA website (at the moment)
import re
import csv
import json
import os

# May be needed for sentiment analysis

def clean_and_save_stats(player_name, team_name, filename, output_format="csv"):
    """Convert raw stats into a structured JSON and save to file."""

    # Define the categories and regex patterns
    categories = {
        "points": r"(\d+)\s+points?",
        "rebounds": r"(\d+)\s+rebounds?",
        "assists": r"(\d+)\s+assists?",
        "steals": r"(\d+)\s+steals?",
        "blocks": r"(\d+)\s+blocks?",
        "turnovers": r"(\d+)\s+turnovers?",
        "field_goal": r"Field Goal.*?(\d+\.?\d*%)",
        "three_point": r"Three-Point.*?(\d+\.?\d*%)"
    }

    # Read raw data from the file
    with open(filename, "r", encoding="utf-8") as file:
        raw_data = file.read()

    # Clean and extract stats based on the raw data using regex
    structured_data = {
        "player": player_name,
        "team": team_name,
        "stats": {
            "points": [25],  # Example static data
            "rebounds": [8],
            "assists": [7],
            "steals": [1],
            "blocks": [1],
            "turnovers": [3],
            "field_goal": ["50%"],
            "three_point": ["40%"]}
    }
    
    # Iterate over the raw data and extract stats based on categories
    for key, pattern in categories.items():
        match = re.search(pattern, raw_data, re.IGNORECASE)
        if match:
            structured_data["stats"][key] = match.group(1)

    # Determine output path for the cleaned data
    cleaned_data_folder = "cleaned_data"
    if not os.path.exists(cleaned_data_folder):
        os.makedirs(cleaned_data_folder)

    # Save to the appropriate file format (CSV or JSON)
    #if output_format == "json":
    #   output_filename = os.path.join(cleaned_data_folder, f"{player_name.lower().replace(' ', '_')}_stats.json")
    #   with open(output_filename, "w", encoding="utf-8") as f:
    #       json.dump(structured_data, f, indent=4)
    #   print(f"Cleaned data saved to {output_filename}")

    if output_format == "csv":
        #output_filename = os.path.join(cleaned_data_folder, f"{player_name.lower().replace(' ', '_')}_stats.csv")
        csv_filename = f"{player_name.lower().replace(' ', '_')}_stats.csv"

        # Define CSV headers
        headers = ["player", "team"] + list(structured_data["stats"].keys())
        # Open the CSV file for writing

        with open(csv_filename, mode='w', encoding="utf-8", newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            
            # Write header row to CSV
            writer.writeheader()

            # Get the maximum length of stats lists (in case there are multiple stats per player)
            max_length = max(len(values) for values in structured_data["stats"].values())

# Write rows for each stat occurrence (each game or stat event)
            for i in range(max_length):
                row = {
                    "player": player_name,
                    "team": team_name,
                    "points": structured_data["stats"].get("points", [""])[i] if i < len(structured_data["stats"].get("points", [])) else '',
                    "rebounds": structured_data["stats"].get("rebounds", [""])[i] if i < len(structured_data["stats"].get("rebounds", [])) else '',
                    "assists": structured_data["stats"].get("assists", [""])[i] if i < len(structured_data["stats"].get("assists", [])) else '',
                    "steals": structured_data["stats"].get("steals", [""])[i] if i < len(structured_data["stats"].get("steals", [])) else '',
                    "blocks": structured_data["stats"].get("blocks", [""])[i] if i < len(structured_data["stats"].get("blocks", [])) else '',
                    "turnovers": structured_data["stats"].get("turnovers", [""])[i] if i < len(structured_data["stats"].get("turnovers", [])) else '',
                    "field_goal": structured_data["stats"].get("field_goal", [""])[i] if i < len(structured_data["stats"].get("field_goal", [])) else '',
                    "three_point": structured_data["stats"].get("three_point", [""])[i] if i < len(structured_data["stats"].get("three_point", [])) else ''
                }
                # Ensure row only contains keys from fieldnames
                filtered_row = {key: row[key] for key in headers}
                writer.writerow(row)

        print(f"Cleaned data saved to {csv_filename}")

    else:
        raise ValueError("Unsupported output format. Choose 'csv' or 'json'.")
    
    return structured_data

