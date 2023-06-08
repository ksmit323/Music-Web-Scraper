"""
Filter out Artists

This script filters by three factors:
    1. Removes all artists who have already been searched for. 
    2. Removes all artists who have not released tracks on Spotify this year. 
    3. Removes all artists who are too popular.

Usage:
    python3 filter_names.py <sent json file> <artists json file>

    Replace <json file> with the file containing all sent artists and the new artists to be filtered.

Output:
    The script will output a filtered version of the original JSON file

"""
from helper import get_token, has_recent_track
from utils import *
import sys
from tqdm import tqdm
import time

# Set up Spotify API credentials
token = get_token()

# Check for correct usage
if (len(sys.argv) < 3):
    print("Don't forgot to include the sent and artists files!")
    print("Usage: python3 scrape2_filter_names.py <json file> <json file>")
    sys.exit(1)

# Load in JSON files
print("Loading files...")
if "sent" in sys.argv[1]:
    sent_file_name = sys.argv[1]
    artists_file_name = sys.argv[2]
else:
    sent_file_name = sys.argv[2]
    artists_file_name = sys.argv[1]

# Import JSON files
sent = import_json_files(sent_file_name)
artists = import_json_files(artists_file_name)


"""First step is to filter from previous results"""

print(f"{len(artists)} artists")

# Check for matching keys and delete
artists_copy = artists.copy()
for artist in artists_copy:
    if artist in sent:
        del artists[artist]

print(f"{len(artists)} artists remaining after removing those sent already")


"""Next step is to filter by recent tracks"""

# Set up variables
release_year = str(2023)
artists_to_remove = []

# Check each artist
print(f"Filtering artists for recent tracks...")
print("This usually takes a while so go make an instant coffee")
print("...")

# for artist in tqdm(artists_rap, desc="Processing", unit="item"):
for artist in tqdm(artists):
    latest_track = has_recent_track(token, artist, release_year)
    if not latest_track:
        artists_to_remove.append(artist)
    else:
        artists[artist]["Top Track"] = latest_track['name']
        artists[artist]["Track URL"] = latest_track['external_urls']['spotify']

# Remove artists on the list
print(f"Removing {len(artists_to_remove)} artists...")
for artist in artists_to_remove:
    try:
        del artists[artist]
    except:
        continue

# time.sleep(10)


""" NEXT STEP IS TO EXPORT JSON FILE """

# Create new JSON file with filtered list 
print(f"{len(artists)} artists remaining.")
print("Downloading new file...")
export_to_json_file(artists_file_name, artists)


""" LAST STEP IS ADD THESE NAMES TO THE SENT LIST """

for artist in artists:
    sent.append(artist)

export_to_json_file(sent_file_name, sent)
