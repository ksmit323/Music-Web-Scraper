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


"""Add top track and the track URL"""

# artists = import_json_files("artists_trap_ml_rev.json")

# for artist in tqdm(artists):

#     artists[artist]["email"] = []

#     latest_track = None
#     latest_release_date = None
#     tracks = get_songs_by_artist(token, artist)

#     for track in tracks:
#         release_date = track["album"]["release_date"]
#         if not latest_release_date or release_date > latest_release_date:
#             latest_release_date = release_date
#             latest_track = track

#     artists[artist]["Top Track"] = latest_track['name']
#     artists[artist]["Track URL"] = latest_track['external_urls']['spotify']
#     time.sleep(0.75)

# export_to_json_file("artists_in_trap.json", artists)


""" Add top track for just a single artist """

# tracks = get_songs_by_artist(token, "1iwUuIOKYjV7SKIg27v4zi")
# latest_track = None
# latest_release_date = None

# for track in tracks:
#     release_date = track['album']['release_date']
#     if not latest_release_date or release_date > latest_release_date:
#         latest_release_date = release_date
#         latest_track = track

# print(latest_track['name'])

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

""" ELIMINATE DUPLICATES FROM SENT.JSON """

# sent = import_json_files("sent.json")
# sent = set(sent)
# sent = list(sent)
# export_to_json_file("sent.json", sent)

""" ELIMINATE DUPLICATES WITH SENT.JSON FROM ARTISTS JSON """

# remove = []
# sent = import_json_files("sent.json")
# artists = import_json_files("artists_genres_total_rap.json")

# for artist in artists:
#     if artist in sent:
#         remove.append(artist)

# print(len(remove))

# for key in remove:
#     if key in artists:
#         del artists[key]

# export_to_json_file("artists_genres_total_rap_r.json", artists)


""" Add to artist IDs to sent """

# rap = import_json_files("artists_genres_total_rap.json")
# sent = import_json_files("sent.json")

# for artist in rap:
#     if artist not in sent:
#         sent.append(artist)

# export_to_json_file("sent_revisioned.json", sent)

""" Add monthly listeners to the data """

# driver  = set_up_selenium_driver()
# class_ = "Ydwa1P5GkCggtLlSvphs"

# artists = import_json_files("emails_reggaeton_ml.json")

# for artist in tqdm(artists):
    
#     try:
#         if artists[artist]["monthly listeners"] == "Failed":

#             try:
#                 driver.get(f'https://open.spotify.com/artist/{artist}')
#                 time.sleep(1)
#                 page_source = driver.page_source
#                 soup = BeautifulSoup(page_source, "html.parser")
#                 text = soup.find('span', class_=class_)
#                 text = text.get_text(strip=True)
#                 text = re.search(r'(\d[\d,]*)', text).group(1)
#                 text = int(text.replace(',',''))
#             except:
#                 text = "Failed"

#             artists[artist]['monthly listeners'] = text        

#             time.sleep(3)
#     except:
#         continue

# driver.close()

# export_to_json_file("emails_reggaeton_ml_rev.json", artists)


""" Add monthly listeners to just one artist"""

# driver  = set_up_selenium_driver()
# class_ = "Ydwa1P5GkCggtLlSvphs"

# artist = "3wFzTRAvCLEACzbRmgBEHx"

# driver.get(f'https://open.spotify.com/artist/{artist}')
# # time.sleep(0.5)
# page_source = driver.page_source
# soup = BeautifulSoup(page_source, "html.parser")
# text = soup.find('span', class_=class_)
# text = text.get_text(strip=True)
# text = re.search(r'(\d[\d,]*)', text).group(1)
# text = int(text.replace(',',''))
# print(text)

# driver.close()


""" Combine a big list of dicts """

# list_artist_dicts = ['artists_genres_many_1.json', 'artists_genres_many_2.json', 'artists_genres_many_3.json', 'artists_genres_many_4.json']

# sent = import_json_files("sent_with_total_rap.json")

# artists_total_pop = {}

# for file_name in list_artist_dicts:
#     artist_dict_list = import_json_files(file_name)

#     for artists in artist_dict_list:
#         for artist in artists:
#             if artist not in artists_total_pop and artist not in sent:
#                 artists_total_pop[artist] = artists[artist]

# print(len(artists_total_pop.keys()))

# export_to_json_file("artists_total_pop.json", artists_total_pop)


""" Add artists to sent """

# artists = import_json_files("artists_total_pop.json")
# sent = import_json_files("sent_with_total_rap.json")

# for artist in artists:
#     if artist not in sent:
#         sent.append(artist)

# export_to_json_file("sent_with_total_rap_pop.json", sent)

artist = {
    "name": "Dorian Electra",
    "genre": "hyperpop",
    "popularity": 50,
    "email": [],
    "spotify": "https://open.spotify.com/artist/202HZzqKvPsMHcbwnDZx7u",
    "Top Track": "Sodom & Gomorrah",
    "Track URL": "https://open.spotify.com/track/0cgUUrFj9pOmSKzm4MyfIf",
    "facebook": "https://facebook.com/girlimusic",
    "twitter": "https://twitter.com/dorianelectra",
    "instagram": "https://instagram.com/dorianelectra"
  }

driver = set_up_selenium_driver()

email = scrape_email_from_facebook(artist["facebook"], driver)

print(email)

