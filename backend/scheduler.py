import threading
import time
from backend.scraper import fetch_match_list, fetch_live_data, get_home_map_data

def run_match_list_scheduler():
    while True:
        print("Fetching latest match data...")
        fetch_match_list()
        time.sleep(60)  # Fetch updates every 60 seconds

def run_live_data_scheduler():
    while True:
        print("Fetching live match updates...")
        fetch_live_data()
        time.sleep(5)  # Fetch live data every 5 seconds

def start_scheduler():
    match_list_thread = threading.Thread(target=run_match_list_scheduler, daemon=True)
    live_data_thread = threading.Thread(target=run_live_data_scheduler, daemon=True)

    match_list_thread.start()
    live_data_thread.start()
