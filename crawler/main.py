import os
import json
import requests
from datetime import datetime
from webcrawler import get_search_results, extract_stats_from_url, get_player_stats
from clean import clean_and_save_stats
from utils import create_player_folder, save_raw_data_to_file, save_cleaned_data_to_file




def process_player_data(player_name, team_name, keywords):
    """Fetch, clean, and save data for a player and team."""
    print(f"Processing data for {player_name} ({team_name})...")

    # Step 1: Scrape raw data from websites and save it
    aggregated_raw_stats = process_player_raw(player_name, team_name, keywords)

     # Step 2: Clean the raw stats data
    cleaned_data = process_player_cleaned(player_name, team_name, aggregated_stats)

    # Step 3: Create a player folder to store cleaned data and raw data files
    base_folder = "backend/crawler"
    player_folder = create_player_folder(base_folder, player_name, team_name)

    # Step 4: Save cleaned data to a file
    cleaned_data_file = save_cleaned_data_to_file(player_name, team_name, cleaned_data, player_folder)

    # Final output
    print(f"Processed and cleaned data for {player_name} ({team_name}). Files saved in {player_folder}")


    return cleaned_data

def sanitize_domain(url):
    return url.split("//")[-1].split("/")[0].replace('.', '_')

def save_individual_raw_file(player_name, team_name, url, stats):
    """Save raw data for each URL into a separate file."""
    domain = sanitize_domain(url)
    folder = os.path.join("data", "raw_data", f"{player_name.lower().replace(' ', '_')}_{team_name.lower()}")
    os.makedirs(folder, exist_ok=True)

    path = os.path.join(folder, f"{domain}.txt")
    
    # Check the structure of stats
    print(f"Stats for {url}: {stats}")

    with open(path, 'w', encoding='utf-8') as f:
        for stat_type, stat_values in stats:
            # Write the stat type as a heading, for example "Points:"
            f.write(f"{stat_type.capitalize()}:\n")
            
            # Now iterate over each entry in the list of stat values and write them to the file
            for value in stat_values:
                f.write(f"{value}\n")


    print(f"Saved individual raw file: {path}")
    return domain, stats

def save_combined_raw_file(player_name, team_name, aggregated_stats):
    """Save the aggregated raw data from all URLs."""
    folder = os.path.join("data", "raw_data", f"{player_name.lower().replace(' ', '_')}_{team_name.lower()}")
    path = os.path.join(folder, "combined_raw.json")

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(aggregated_stats, f, indent=4)
    print(f"Saved combined raw file: {path}")

def process_player_raw(player_name, team_name, keywords):
    """Scrape multiple websites, save raw data, and aggregate it."""
    search_results = get_search_results(player_name, team_name)
    aggregated_stats = {}

    for url in search_results:
        print(f"Scraping from: {url}")
        stats = extract_stats_from_url(url, keywords)

        if stats:
            domain, _ = save_individual_raw_file(player_name, team_name, url, stats)
            aggregated_stats[domain] = stats

    save_combined_raw_file(player_name, team_name, aggregated_stats)
    return aggregated_stats

def process_player_cleaned(player_name, team_name, aggregated_stats):
    """Clean and structure the raw data, then save it."""
    clean_stats = {}

    for source, stats in aggregated_stats.items():
        print(f"Cleaning data from {source}...")
        clean_stats[source] = clean_and_save_stats(player_name, team_name, stats)

    return clean_stats

def main():
    # Example usage for a specific player and team
    player_name = "LeBron James"
    team_name = "Lakers"
    keywords = ["points", "rebounds", "assists", "steals", "blocks", "field goal", "three-point"]
    
    #Step 1: Process the data
    process_player_data(player_name, team_name, keywords)

if __name__ == "__main__":
    main()