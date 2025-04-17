# HR: GitHub: https://github.com/pseudo-r/Public-ESPN-API
# HR: GitHub: https://github.com/unclecode/crawl4ai
# HR: ChatGPT: To automatically insert comments (for me and my teammate to better understand some of the code from GitHub)

# Author: Benjamin Davis

import random
import requests
from bs4 import BeautifulSoup
from googlesearch import search
import time
import re
import csv

# Define keywords to search for in stats lines
keywords = [
    "points", "rebounds", "assists", "steals", "blocks",
    "turnovers", "3-point", "free throw", "field goal",
    "minutes", "fouls", "plus-minus"
]

def get_search_results(player_name, team_name):
    """Search Google for recent stats of a player."""
    query = f"{player_name} {team_name} site:nba.com OR site:basketball-reference.com"
    search_results = [url for url in search(query, num_results=2)]  # Fetch top 1 result for now
    return search_results

#Raw data
def extract_stats_from_url(url, keywords):
    """Extract player stats from a given webpage."""
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
        return None
    
    soup = BeautifulSoup(response.text, "html.parser")
    results = [] #

    all_text = soup.get_text()  # Splits text into lines
    
    for line in all_text.splitlines():
        if any(keyword.lower() in line.lower() for keyword in keywords):
            results.append(line.strip())
    print("Results from:", url)
    for r in results:
        print("-", r)

def get_player_stats(player_name, team_name):
    """Get player stats by searching and extracting data from web pages."""
    print(f"Searching for stats on {player_name} ({team_name})...")
    search_results = get_search_results(player_name, team_name) #URL search
    raw_stats = []  #List for data from websites
    filenames = []  # List of filenames
    counter = len(search_results) -1
    for url in search_results:
        print(f"Fetching stats from: {url}")
        raw_stats_data = extract_stats_from_url(url, keywords="3PT") #raw data, look for 3 points for now
        raw_stats.append(raw_stats_data)
        filename = f"{len(search_results)-counter}_{player_name.lower().replace(' ', '_')}_data.txt" #make text file with name being 1_playername_data.txt
        counter-= 1

        # Save the raw data to a file
        with open(filename, "w", encoding="utf-8") as file:
            file.write(f"Player: {player_name}\nTeam: {team_name}\n\n{raw_stats}")
            print(f"Raw data saved to {filename}")
    print('URL GREEN')
    
    return filenames

get_player_stats("Lebron James", "Lakers") #Get this from user. Get variable from UI and bring that to the backend here as such
