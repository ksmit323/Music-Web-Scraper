from helper import *

import datetime
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time
from dotenv import load_dotenv
import os

# Set up Spotify API credentials
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# Create a Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Get today's date in the format required by the Spotify API
today = datetime.datetime.now().strftime('%Y-%m-%d')

# Initialize an empty list to store all track names
track_names = []

# Set the initial offset value and batch size
offset = 0
batch_size = 50

# Get new releases
while True:
    results = spotify.new_releases(country='US', limit=batch_size, offset=offset)

    # Extract the track names from the current batch of results
    track_names.extend([album['name'] for album in results['albums']['items']])

    # Check if there are no more new releases
    if not results['albums']['next']:
        break

    # Update the offset for the next batch
    offset += batch_size

    # Pause for 1 second before making the next API request
    time.sleep(1)

    # Add additional pause if desired to avoid rate limits
    time.sleep(1)  # Adjust the duration of sleep as needed

# Print the track names
# for name in track_names:
#     print(name)
print(len(track_names))