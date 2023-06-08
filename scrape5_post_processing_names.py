from utils import *
import openpyxl


artists = import_json_files('artists_in_latin.json')


for artist in artists:
    artists[artist]["Spotify"] = f"https://open.spotify.com/artist/{artist}"


export_to_json_file("artists_in_latin_revised.json", artists)

