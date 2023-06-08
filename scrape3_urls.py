"""
Scrape URL's from Spotify

This script scrapes all social media links from an artist's Spotify profile. 
Input is a JSON file of artists from only one genre and one country with their Spotify IDs.

Usage:
    python3 scrape3_urls.py <json file>

    Replace <json file> with the file containing a filtered list of artist information

Output:
    The script will create a JSON file of all artists and their corresponding links 
"""

from helper import scrape_for_social_media_links, set_up_selenium_driver
from utils import import_json_files, export_to_json_file
from tqdm import tqdm
import sys
import time


# Check for correct usage
if (len(sys.argv) < 2):
    print("Don't forgot to include the file!")
    print("Usage: python scrape3_urls.py <json file>")
    sys.exit(1)

# Load in JSON file
print("Loading file...")
artists = import_json_files(sys.argv[1]) # File is returned as a list

# Track artists who failed to produce links
failed_log = []

# Add URLs for each artist
driver = set_up_selenium_driver() # set up Selenium WebDriver
for artist in tqdm(artists):
    artists[artist]['facebook'] = ""
    artists[artist]['twitter'] = ""
    artists[artist]['instagram'] = ""
    try:
        urls = scrape_for_social_media_links(artist, driver)
    except:
        print(f"URL scraping failed for artist ID: {artist}")
        failed_log.append(artist)
        continue
    for url in urls:
        if 'facebook' in url:
            artists[artist]['facebook'] = url
        elif 'twitter' in url:
            artists[artist]['twitter'] = url
        elif 'instagram' in url:
            artists[artist]['instagram'] = url
    time.sleep(1)
driver.quit() # Close the driver

# Export new JSON file with updated URLs. File name remains the same
print(f"Exporting {sys.argv[1]} file...")
export_to_json_file(sys.argv[1], artists)    

# Export file for failed log
if len(failed_log) > 0:
    export_to_json_file("failed_url_log.json", failed_log)