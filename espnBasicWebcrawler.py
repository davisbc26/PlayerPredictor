# HR: GitHub: https://github.com/pseudo-r/Public-ESPN-API
# HR: GitHub: https://github.com/unclecode/crawl4ai
# HR: ChatGPT: To automatically insert comments (for me and my teammate to better understand some of the code from GitHub)

# Author: Benjamin Davis

import random
import requests
from bs4 import BeautifulSoup
from googlesearch import search
import time

def get_search_results(player_name, team_name):
    """Search Google for recent stats of a player."""
    query = f"{player_name} {team_name} latest stats site:espn.com OR site:nba.com OR site:basketball-reference.com"
    search_results = [url for url in search(query, num_results=5)]  # Fetch top 5 results
    return search_results

def extract_stats_from_url(url):
    """Extract player stats from a given webpage."""
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
        return None
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Searching for relevant stats in the page
    text_data = soup.get_text()
    relevant_stats = []
    
    # These are static for now, I will go back and connect these keywords with the basicKeywordExtractor.py #
    keywords = ["Points", "Rebounds", "Assists", "Steals", "Blocks", "Field Goal", "Three-Point", "Turnovers"]
    
    for line in text_data.split("\n"):
        for keyword in keywords:
            if keyword.lower() in line.lower():  # Check if line contains stats
                relevant_stats.append(line.strip())
    
    return relevant_stats if relevant_stats else ["No stats found."]

def get_player_stats(player_name, team_name):
    """Get player stats by searching and extracting data from web pages."""
    print(f"Searching for stats on {player_name} ({team_name})...")
    search_results = get_search_results(player_name, team_name)
    
    all_stats = []
    for url in search_results:
        print(f"Fetching stats from: {url}")
        stats = extract_stats_from_url(url)
        if stats:
            all_stats.extend(stats)
        time.sleep(random.uniform(1, 10))  # Prevent rate-limiting

    return all_stats

def save_raw_data(player_name, team_name, raw_stats):
    # If raw_stats is a list, convert it to a string
    if isinstance(raw_stats, list):
        raw_text = "\n".join(raw_stats)  # Join the list into a single string, separated by new lines
    else:
        raw_text = raw_stats  # If it's already a string, use it directly

    filename = f"{player_name.lower().replace(' ', '_')}_data.txt"
    
    # Save the raw data to a file
    with open(filename, "w", encoding="utf-8") as file:
        file.write(f"Player: {player_name}\nTeam: {team_name}\n\n{raw_text}")

    print(f"Raw data saved to {filename}")


# Example for the Presentation in Class (Checkpoint 2)
player_name = "LeBron James"
team_name = "Los Angeles Lakers"

raw_stats = get_player_stats(player_name, team_name)

save_raw_data(player_name, team_name, raw_stats)