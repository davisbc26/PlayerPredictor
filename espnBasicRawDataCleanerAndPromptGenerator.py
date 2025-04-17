# HR: GitHub: https://github.com/scrapy/scrapy
# HR: GitHub: https://github.com/promptslab/Awesome-Prompt-Engineering (NOTE: HAVE NOT USED THIS YET, BUT PLAN TO IMPLEMENT IT)
# HR: ChatGPT: To automatically generate comments for me and my teammate to better understand the GitHub code
# HR: ChatGPT: To troubleshoot formatting of step 1 in the process_and_generate_prompt method (I didn't know where the brackets and quotes went

# Author: Benjamin Davis



# import...


# Read raw data from the file
def read_raw_data(filename):
    with open(filename, "r", encoding="utf-8") as file:
        raw_data = file.read()
    return raw_data

# Process the raw data (e.g., clean, extract important information)
def process_player_data(raw_data):
    # Example: Clean up the raw data, remove unwanted text, etc.
    processed_data = raw_data.replace("\n", " ")  # Simple cleanup for now
    return processed_data

# Generate a final prompt for ChatGPT
def create_prompt(cleaned_data, player_name, team_name):
    prompt = f"Based on the stats for {player_name} of {team_name}, here is the performance summary:\n{cleaned_data}\nCan you generate predictions for their upcoming game?"
    return prompt

# Full flow: process raw data and generate the prompt
def process_and_generate_prompt(player_name, team_name):
    # Step 1: Read raw data from file
    filename = f"{player_name.lower().replace(' ', '_')}_data.txt"
    raw_data = read_raw_data('lebron_james_data.txt')

    # Step 2: Process the raw data
    cleaned_data = process_player_data(raw_data)

    # Step 3: Generate a prompt for ChatGPT
    prompt = create_prompt(cleaned_data, player_name, team_name)

    return prompt

# Example (May not work, I got IP blocked and couldn't generate a .txt output to use for testing)
player_name = "LeBron James"
team_name = "Los Angeles Lakers"
prompt = process_and_generate_prompt(player_name.lower(), team_name)
