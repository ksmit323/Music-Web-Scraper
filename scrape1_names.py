"""
Spotify Artist Scraper

This script uses the Spotify API to scrape music artists based on the provided criteria. 
It retrieves artists who have recent tracks available and a popularity rating below a certain threshold.

Usage:
    python3 scrape_names.py <country_codes> <genre_list>

    Replace <country_codes> and <genre_list> with JSON files of countries and genres, respectively.
    Genres is a dictionary containing a list of genres.

API Credentials:
    You need to provide your own Spotify API credentials in order to use this script. 
    
    You can create a Spotify Developer account and register an application to obtain the required credentials.

    Once you have your credentials, update the `CLIENT_ID` and `CLIENT_SECRET` constants in the ".env" file with your own values.

Output:
    The script will output a JSON file of music artists including their names, artist ID, and genre

"""
from helper import get_token, search_for_artists
from utils import export_to_json_file, import_json_files
import time
import sys


# Check for correct usage
if len(sys.argv) < 3:
    print("You need to load files for both countries and genres")
    print("USAGE: python script.py <json for country codes> <json for genres>")
    sys.exit(1)

# Load in JSON files
print("Loading files...")
for i in range(2):
    data = import_json_files(sys.argv[i+1])

    if 'countries' in data:
        countries = data['countries']
    elif 'genres' in data:
        genres = data['genres']
    else:
        raise Exception("Incorrect file was attempted to be uploaded")

# Set up Spotify API credentials
token = get_token()

genres_total = []
count = 0

# Iterate over each country and genre
for country in countries:

    for i, genre in enumerate(genres):
        
        # Add artists to the list
        artists = search_for_artists(token, genre)
        print(f"Total artists in {genre}: {len(artists)}")
        print("------------------------")

        genres_total.append(artists)
        count += 1
        if count == 15:
            count = 0
            # Export each country to JSON file
            export_to_json_file(f"artists_genres_many_rap_{i}.json", genres_total)

        time.sleep(5)
    