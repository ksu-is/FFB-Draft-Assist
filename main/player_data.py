import requests
import json
import os
from datetime import datetime

# Path to store the cached player data
CACHE_FILE = 'players_data.json'
CACHE_DATE_FILE = 'cache_date.txt'

# Positions to remove
POSITIONS_TO_REMOVE = ["LB", "CB", "SS", "FS", "DT", "DE", "C", "OG", "OT", "OL", "ILB", "OLB", "LS", "NT", "DB", "None", "S", "DL"]

def fetch_nfl_players():
    url = 'https://api.sleeper.app/v1/players/nfl'
    response = requests.get(url)

    if response.status_code == 200:
        players_data = response.json()
        return players_data
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None

def read_cached_data():
    # Check if the cache file exists
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as file:
            return json.load(file)
    else:
        return None

def get_last_fetch_date():
    # Check if the cache date file exists
    if os.path.exists(CACHE_DATE_FILE):
        with open(CACHE_DATE_FILE, 'r') as file:
            return file.read().strip()
    return None

def save_current_date():
    # Save the current date to the file
    with open(CACHE_DATE_FILE, 'w') as file:
        file.write(datetime.now().strftime('%Y-%m-%d'))

def is_cache_expired():
    last_fetch_date = get_last_fetch_date()

    if not last_fetch_date:
        return True

    # Compare with today's date
    today = datetime.now().strftime('%Y-%m-%d')
    if last_fetch_date != today:
        return True

    return False

def save_all_data(players_data):
    # Save all player data to players_data.json
    with open(CACHE_FILE, 'w') as file:
        json.dump(players_data, file)

    print(f"Saved {len(players_data)} players to {CACHE_FILE}.")
    return players_data

def get_players_data():
    # Check if the cache is expired or does not exist
    if is_cache_expired():
        print("Fetching new data from the API...")
        players_data = fetch_nfl_players()
        if players_data:
            save_current_date()  # Update the fetch date
            return save_all_data(players_data)  # Save all player data to the cache
    else:
        print("Using cached data...")
        return read_cached_data()

def remove_players_by_position(players_data, positions_to_remove=None):
    if positions_to_remove is None:
        positions_to_remove = POSITIONS_TO_REMOVE
    
    # Create a new dictionary to store players that don't have the unwanted positions
    filtered_players = {}
    
    for player_id, player_info in players_data.items():
        # Get player's fantasy_positions, default to an empty list if None
        player_positions = player_info.get("fantasy_positions", [])
        player_position = player_info.get("position", "")

        # Ensure player_positions is a list, default to an empty list if None
        if player_positions is None:
            player_positions = []

        # Check if the player's position or fantasy_positions contain any of the unwanted positions
        if player_position not in positions_to_remove and not any(pos in positions_to_remove for pos in player_positions):
            # Keep this player in the filtered dictionary
            filtered_players[player_id] = player_info

    return filtered_players


    return filtered_players



# Main Program

# Fetch or load the player data
players = get_players_data()

if players:
    print(f"Fetched or loaded {len(players)} players.")

    # Remove players with unwanted positions (e.g., LB, CB, SS, FS, DT, DE)
    updated_players_data = remove_players_by_position(players)
    print(f"Filtered out unwanted positions. {len(updated_players_data)} players remain.")
    
    # Save the filtered data back to the cache file
    save_all_data(updated_players_data)

else:
    print("No player data available.")
