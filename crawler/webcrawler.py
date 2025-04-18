# HR: GitHub: https://github.com/pseudo-r/Public-ESPN-API
# HR: GitHub: https://github.com/unclecode/crawl4ai
# HR: ChatGPT: To automatically insert comments (for me and my teammate to better understand some of the code from GitHub)

# Author: Nathan Vu, Ben D

import requests
from bs4 import BeautifulSoup
from googlesearch import search
import re
import csv
from clean import clean_and_save_stats

def get_search_results(player_name, team_name):
    """Search Google for recent stats of a player."""
    query = f"{player_name} {team_name} site:nba.com " #Just stick with NBA and incorporate sentiment analysis later
    search_results = [url for url in search(query, num_results=1)]  # Fetch top 1 result for now
    return search_results

#Raw data
def extract_stats_from_url(url):
    """Extract player stats from a given webpage."""
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
        return []
    
    soup = BeautifulSoup(response.text, "html.parser")  
    stats_section = soup.find('section', attrs= {'data-has-container': "true"})

    if not stats_section:
        print(f"Stats section not found on {url}")
        return None

    # Extract column headers (keywords) from the table header
    headers_row = stats_section.find('thead').find('tr')
    headers = [header.get_text(strip=True) for header in headers_row.find_all('th')]

    # Find all divs within this section that likely contain the stats for each game
    # Adjust the class names or attributes according to the structure of the page
    stats_div = soup.find('div', class_='MockStatsTable_statsTable__V_Skx')
    if not stats_div:
        print(f"Stats div not found on {url}")
        return None
    # Find the table inside the div (assuming it's the only table or the first table in the div)
    stats_table = stats_div.find('table')
    if not stats_table:
        print(f"Stats table not found inside the div on {url}")
        return None

    # Extract column headers (keywords) from the table header (thead > tr > th)
    headers_row = stats_table.find('thead').find('tr') #locate the <thead> section of the table which contains the headers. Then, we find the first row (<tr>) in the <thead>.
    headers = [header.get_text(strip=True) for header in headers_row.find_all('th')] #Store header text in a list to be used to define the keywords for the columns (e.g., "Date", "Matchup", "PTS").
    
    # Create a list of keywords dynamically based on the extracted headers
    keywords = headers  # Now keywords are defined by the <th> values (table headers)
    
    results = [] #Hold all the data represented as a dictionary. Keys are the headers/keywords. Values are the stats for that game.

    # Extract all rows from the table body (tbody > tr) - skip the header row
    rows = stats_table.find('tbody').find_all('tr')

    # For each row, extract the corresponding data
    for row in rows:
        # Extract all columns (td) in the current row
        columns = row.find_all('td')
        
        # Create a dictionary to store the stats for this game
        game_data = {}

        # Loop through each column and match it with the corresponding keyword
        for i, keyword in enumerate(keywords):
            if i < len(columns):  # Make sure there are enough columns
                stat_value = columns[i].get_text(strip=True)  # Extract text and strip any extra spaces
                game_data[keyword] = stat_value
        
        # Only append to results if we found data for the game
        if game_data:
            results.append(game_data)

    return results #List of dictionaries

def sanitize_filename(s):
    return re.sub(r'[\\/*?:"<>|]', "_", s)  # replaces illegal characters with _

def save_stats_to_csv(player_name, team_name, raw_stats_data):
    """Save player stats to CSV."""
    
    if not raw_stats_data:
        print("No stats data to save.")
        return
    
    # Define the headers (keys from the first dictionary in raw_stats_data)
    headers = raw_stats_data[0].keys()

    # Create a filename based on the player's name and team
    safe_filename = sanitize_filename(f"{player_name.lower().replace(' ', '_')}_{team_name.lower()}_stats.csv")
    
    # Open CSV file for writing
    with open(safe_filename, mode='w', encoding="utf-8", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        
        # Write the header
        writer.writeheader()
        
        # Write the data
        for game_data in raw_stats_data:
            writer.writerow(game_data)

    print(f"Data saved to {safe_filename}")

    return safe_filename


def get_player_stats(player_name, team_name):
    """Get player stats by searching and extracting data from web pages."""
    print(f"Searching for stats on {player_name} ({team_name})...")
    search_results = get_search_results(player_name, team_name) #URL search 
    filenames = []  # List of filenames

    for url in search_results:
        print(f"Fetching stats from: {url}")
        raw_stats_data = extract_stats_from_url(url) #Data from div section guarenteed to have targetted data
        print("Raw Stats Data:", raw_stats_data)

        #Save raw data to txt file

        #From text file convert/clean into csv file

        #Saves the raw data to a CSV file (From NBA stat page)
        filename = save_stats_to_csv(player_name, team_name, raw_stats_data)  # Save data directly as CSV
        print(f"Data saved to CSV for {filename}")

        filenames.append(filename)

        print('URL GREEN')
    return filenames
    
    
get_player_stats("Lebron James", "Lakers") #Get this from user. Get variable from UI and bring that to the backend here as such
