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
artists = import_json_files(sys.argv[1])
print("File loaded...")

# Tracking data
failed_log = []

# Scrape for emails for each artist
print("Finding emails...")
driver = set_up_selenium_driver() # set up Selenium WebDriver
for artist in tqdm(artists):

    if artists[artist]['genre'] == 'hyperpop': #! DELETE THIS !!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        # Scrape from Twitter
        try:
            twitter_handle = artists[artist]['twitter']
            if twitter_handle != "":
                email = scrape_email_from_twitter(twitter_handle, driver)
            else:
                email = []
        except Exception as e:
            email = []
            print(f'Error scraping from Twitter: {e}')
        artists[artist]['email'].extend([addr for addr in email if addr not in artists[artist]['email']])
        time.sleep(0.5)

        # Scrape from Facebook
        try:
            facebook_handle = artists[artist]['facebook']
            if facebook_handle != "":
                email = scrape_email_from_facebook(facebook_handle, driver)
            else:
                email = []
        except Exception as e:
            print(f'Error scraping facebook: {e}')
            continue
        artists[artist]['email'].extend([addr for addr in email if addr not in artists[artist]['email']])
        time.sleep(0.5)
        
        # Track failed retrieval of emails
        if len(artists[artist]['email']) == 0:
            failed_log.append(artist)

driver.quit()

# Export new JSON file with updated emails. File name remains the same
print(f"Exporting {'emails_' + sys.argv[1]} file...")
export_to_json_file(f'emails_{sys.argv[1]}', artists)

# Export file for failed log
export_to_json_file(f"failed_email_{sys.argv[1]}_log.json", failed_log)
