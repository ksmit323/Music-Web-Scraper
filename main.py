from utils import *
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Keys, ActionChains
import re
import time
from helper import *
from tqdm import tqdm
import sys

token = get_token()


#! DEPRECATED !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# """Add top track and the track URL"""

artists = import_json_files("artists_in_latin.json")

for artist in tqdm(artists):

    latest_track = None
    latest_release_date = None
    tracks = get_songs_by_artist(token, artist)

    for track in tracks:
        release_date = track["album"]["release_date"]

        if not latest_release_date or release_date > latest_release_date:
            latest_release_date = release_date
            latest_track = track

    artists[artist]["Top Track"] = latest_track['name']
    artists[artist]["Track URL"] = latest_track['external_urls']['spotify']

export_to_json_file("artists_in_latin_revised.json", artists)


"""EXPORT TO EXCEL"""

# # Load the JSON data from file
# data = import_json_files('rap_file.json')

# # Create an empty DataFrame
# df = pd.DataFrame()

# # Iterate over each key-value pair in the JSON data
# for key, value in data.items():
#     # Create a new column with the key as the name
#     df[key] = pd.Series(value)

#     # # Remove unnecessary characters from the email and replace links with Spotify link
#     # for key2 in df[key].keys():
#     #     if key2 == 'email':
#     #         df[key][key2] = df[key][key2][0][0]

# # Transpose the DF to have keys as columns and values as rows
# df = df.transpose()

# # # Export the DF to an Excel file
# df.to_excel('07-06-2023_hip_hop_updated_tracks.xlsx', index=False)


""" IMPORT FROM EXCEL """

# # Read the Excel file into a pandas DataFrame
# df = pd.read_excel('07-06-2023_hip_hop_with_emails.xlsx')

# # Convert the DataFrame to a dictionary
# data = df.to_dict(orient='index')

# # Export the dictionary to a JSON file
# with open('output.json', 'w') as json_file:
#     json.dump(data, json_file, indent=2)


""" Search for all artist info"""

# artist = 'taylor swift'

# info = get_artist_info_by_name(token, artist)
# print(info)

""" Remove artists who don't have emails. """

# rap = import_json_files("rap_file.json")
# remove = []

# for artist in rap:
#     if len(rap[artist]['email']) == 0:
#         remove.append(artist)

# for artist in remove:
#     del rap[artist]

# export_to_json_file('rap_again.json', rap)

""" Separate out URLs into different tabs """

# rap = import_json_files("artists_in_latin_revised.json")

# for artist in rap:
#     rap[artist]['facebook'] = ""
#     rap[artist]['twitter'] = ""
#     rap[artist]['instagram'] = ""

#     for url in rap[artist]['urls']:
#         if 'facebook' in url:
#             rap[artist]['facebook'] = url
#         elif 'twitter' in url:
#             rap[artist]['twitter'] = url
#         elif 'instagram' in url:
#             rap[artist]['instagram'] = url
    
#     del rap[artist]['urls']
        
# export_to_json_file('artists_in_latin.json', rap)


""" Delete a key """

# artists = import_json_files("rap_file.json")

# for artist in artists:
#     del artists[artist]['urls']

# export_to_json_file('rap_again.json', artists)


""" Turn list of IDs to a dict of artist info """

# artist_list = import_json_files("failed_rap_email_log.json")

# artists = {}

# for artist in tqdm(artist_list):

#     data = get_artist_info_by_id(token, artist)
#     artists[artist] = {
#         "name": data["name"],
#         "genre": "hip hop",
#         "popularity": data["popularity"],
#         "Spotify": data['external_urls']["spotify"]
#     }

# export_to_json_file("rap_again.json", artists)

""" Filter by popularity rating """

# artists = import_json_files("artists_in_latin.json")
# artists_copy = artists.copy()
# for artist in artists_copy:
#     if artists[artist]['Popularity'] > 59:
#         del artists[artist]

# export_to_json_file("artists_in_latin.json", artists)


    