import requests
import json
import os
from datetime import datetime

# Path to store the cached player data
CACHE_FILE = 'players_data.json'
CACHE_DATE_FILE = 'cache_date.txt'

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

# Fetch or load the player data
players = get_players_data()

if players:
    print(f"Fetched or loaded {len(players)} players.")
else:
    print("No player data available.")
