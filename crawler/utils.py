import os
import json

# You can update these paths or import them from a config file if needed
RAW_DATA_FOLDER = "data/raw_data"
CLEANED_DATA_FOLDER = "data/cleaned_data"


def create_player_folder(base_folder, player_name, team_name):
    """Creates and returns the full folder path for a player's data."""
    folder_name = f"{player_name.lower().replace(' ', '_')}_{team_name.lower()}"
    folder_path = os.path.join(base_folder, folder_name)
# Create the folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path

def save_raw_data_to_file(player_name, team_name, raw_stats, folder_path):
    """Save the aggregated raw stats data to a JSON file."""
    filename = f"{player_name.lower().replace(' ', '_')}_raw_stats_{team_name.lower()}.txt"
    raw_data_path = os.path.join(folder_path, filename)

    with open(raw_data_path, 'w', encoding='utf-8') as f:
        json.dump(raw_stats, f, indent=4)

    print(f"[RAW] Saved to: {raw_data_path}")
    return raw_data_path

def save_cleaned_data_to_file(player_name, team_name, cleaned_data, folder_path):
    """Save the structured cleaned stats to a JSON file."""
    filename = f"{player_name.lower().replace(' ', '_')}_cleaned_stats_{team_name.lower()}.json"
    cleaned_data_path = os.path.join(folder_path, filename)

    with open(cleaned_data_path, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, indent=4)

    print(f"[CLEANED] Saved to: {cleaned_data_path}")
    return cleaned_data_path