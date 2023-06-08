"""
Scrape for emails

This script scrapes for emails given the social media URLs provided by Spotify
Input is a JSON file of artists containing all of their links scraped from Spotify

Usage:
    python3 scrape4_emails.py <json file>

    Replace <json file> with the file containing a filtered list of artist information

Output:
    The script will create a JSON file of all artists and their corresponding emails if one can be found
"""
from helper import scrape_email_from_facebook, scrape_email_from_twitter, set_up_selenium_driver
from utils import import_json_files, export_to_json_file
from tqdm import tqdm
import sys
import time

# Check for correct usage
if (len(sys.argv) < 2):
    print("Don't forgot to include the file!")
    print("Usage: python scrape_emails.py <json file>")
    sys.exit(1)

# Load in JSON file
print("Loading file...")
artists = import_json_files(sys.argv[1])

# Tracking data
failed_log = []

# Scrape for emails for each artist
driver = set_up_selenium_driver() # set up Selenium WebDriver
for artist in tqdm(artists):
    artists[artist]['email'] = []

    # Scrape from Twitter
    try:
        email = scrape_email_from_twitter(artists[artist]['twitter'], driver)
    except:
        continue
    for info in email:
        artists[artist]['email'].append(info)

    # Scrape from Facebook
    try:
        email = scrape_email_from_facebook(artists[artist]['facebook'], driver)
    except:
        continue
    for info in email:
        artists[artist]['email'].append(info)
    
    # Track failed retrieval of emails
    if len(artists[artist]['email']) == 0:
        failed_log.append(artist)
driver.quit() # Close the driver

# Export new JSON file with updated emails. File name remains the same
print(f"Found {len(artists)-len(failed_log)} emails")
print(f"Exporting {sys.argv[1]} files...")
export_to_json_file(sys.argv[1], artists)

# Export file for failed log
# export_to_json_file(f"failed_email_{sys.argv[1]}_log.json", failed_log)
