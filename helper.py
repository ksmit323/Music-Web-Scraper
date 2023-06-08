from dotenv import load_dotenv
import requests
import os
import base64
from requests import post, get
import requests
import json
import time
import re
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Keys, ActionChains



def get_token():
    """Set up Spotify API credentials"""

    load_dotenv()
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result['access_token']
    return token


def get_auth_header(token):
    return {"Authorization": "Bearer " + token}


def get_artist_info_by_name(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)['artists']['items']
    if len(json_result) == 0:
        print("No artist")
        return None
    return json_result[0]

def get_artist_info_by_id(token, id):
    url = f"https://api.spotify.com/v1/artists/{id}"
    headers = get_auth_header(token)
    res = get(url, headers=headers)
    json_result = json.loads(res.content)
    return json_result


def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    res = get(url, headers=headers)
    json_result = json.loads(res.content)['tracks']
    return json_result


def get_new_songs(token):
    url = "https://api.spotify.com/v1"
    headers = get_auth_header(token)
    year = "2023"
    limit = 50
    search_params = {
    'q': f'year:{year}',
    'type': 'track',
    'limit': limit,
    }
    search_response = requests.get(f"{url}/search", headers=headers, params=search_params)
    search_results = search_response.json()

    return search_results


def make_request(url, headers, params):
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response
    except (requests.exceptions.RequestException) as e:
        print("Request Error:", e)
        return response


def handle_rate_limit(response):
    """
    Handles API rate limit by pausing execution if necessary.

    Args:
        response: The response object returned from the API request.
    """
    if "Retry-After" in response.headers:
        retry_after = int(response.headers["Retry-After"])
        time.sleep(retry_after)
    else:
        time.sleep(1)


def search_for_artists(token, genre):
    """
    Searches for artists on Spotify based on genre, country, and a maximum number of followers.
    
    Args:
        token (str): A valid access token for the Spotify API.
        max_followers (int): The maximum number of followers an artist can have to be included in the result.
        genre (str): The genre of the artists to search for.
        country (str): The country to limit the search to.

    Returns:
        dict: A dictionary containing information about the artists found. The keys are the artist IDs, and the values 
        are dictionaries with 'name', 'genre', and 'country' keys representing the artist's name, genre, and country respectively.
    """
    
    # URL and headers for making the API request
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)

    # Parameters for the search query
    params = {
        "q": f"genre:{genre}",
        "type": "artist",
        "limit": 50,
    }

    # Dict to store artists
    artists = {}

    count_pages = 0
    retry_count = 0

    # Loop until all pages of artists are retrieved
    while True:

        # Call on Spotify API
        response = make_request(url, headers, params)
        if count_pages == 20:
            print("Reached 20 page limit.")
            break

        # Retry the same page if rate limit is hit
        if response.status_code == 429:
            handle_rate_limit(response)
            retry_count += 1
            if retry_count < 2:
                params["offset"] = data["artists"]["offset"] - params["limit"]
            continue
        retry_count = 0

        # Parse the response
        data = response.json()

        # Add artists to the result if their popularity rating is low enough
        if "artists" in data and "items" in data["artists"]:
            for artist in data["artists"]["items"]:
                pop = artist["popularity"]
                if pop < 60:
                    artists[artist['id']] = {
                        'name': artist["name"],
                        'genre': genre,
                        'popularity': pop,
                        'spotify': artist['external_urls']['spotify']
                    }
        count_pages += 1

        # Go to the next page of artists if available
        print(f"{genre} page: {count_pages}/20")
        try:
            if "next" in data["artists"]:
                params["offset"] = data["artists"]["offset"] + params["limit"]
            else:
                print("Finished looping through all artists")
                break
        except Exception as e:
            print("Exception has been caught: ", e)
            break
        time.sleep(1)

    return artists


def has_recent_track(token, artist_id, release_year):

    """
    Checks if the specified artist has released any tracks in the given release year.
    If so, the track is added as the artist's Top Track.

    Parameters:
        token (str): The access token for authenticating the Spotify API request.
        artist_id (str): The unique identifier of the artist on Spotify.
        release_year (str): The year to check for recent tracks (format: "YYYY").

    Returns:
        bool: True if the artist has released a track in the specified release year,
            False otherwise.
    """

    tracks = get_songs_by_artist(token, artist_id)
    latest_track = None
    latest_release_date = None

    for track in tracks:
        release_date = track["album"]["release_date"]
        if not latest_release_date or release_date > latest_release_date:
            latest_release_date = release_date
            latest_track = track

    if latest_track['album']['release_date'][:4] == release_year:
        time.sleep(0.5)
        return latest_track
    
    time.sleep(0.5)
    return False
    

def set_up_selenium_driver():
    """Run Selenium driver"""

    service = Service("music_scraper\driver")
    options = webdriver.ChromeOptions()
    options.add_argument('--headless') # Run Chrome in headless
    options.add_argument('log-level=3') # Suppress log messages
    driver = webdriver.Chrome(service=service, options=options)

    return driver

def scrape_for_social_media_links(artist_id, driver):
    """
    Scrapes social media links from a Spotify Profile

    Args:
        artist_id (str): The artist ID associated with the Spotify profile.
        driver: Selenium class to interact with the webpage autonomously.    
    Returns:
        list: A list containing the social media links found on the Spotify profile.
              Links are likely Facebook, Youtube, Instagram and Twitter. Note that only the links 
              found on the profile are included.
    """

    # Load the page
    driver.get(f'https://open.spotify.com/artist/{artist_id}')

    # Scroll down the page and find the button
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    button_locator = (By.CLASS_NAME, "uhDzVbFHyCQDH6WrWZaC")
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located(button_locator))

    # Perform the button click
    driver.find_element(*button_locator).click()
    time.sleep(0.5)

    # Get the updated HTML content after the button click
    updated_html = driver.page_source

    # Parse the HTML content Using BeautifulSoup
    soup = BeautifulSoup(updated_html, 'html.parser')

    # Find the social media links from the Spotify profile
    links = soup.find_all('a', attrs={'class': "oe0FHRJU7PvjoTnXJmfr"})

    # Find all URLs with this regex
    href_regex = r'href="(https?://[^"]+)"'
    urls = re.findall(href_regex, str(links))

    #* Another way to obtain the urls is by looping thru
    # urls = []
    # for link in links:
    #     match = re.search(href_regex, str(link))
    #     if match:
    #         urls.append(match.group(1))
    
    return urls
    

def scrape_email_from_twitter(link, driver):
    """
    Scrapes email addresses from Twitter.

    Args:
        link (url string): A string containing the URL for artist's twitter profile.

    Returns:
        email (string): A string containing the email address of the artist if there is one. 

    """
    # Load the page
    driver.get(link)
    time.sleep(2)

    # Set path to find element (Only for Twitter)
    xpath1 = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[3]/div/div/span'
    xpath2 = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[3]/div/div/span[2]'
    xpaths = [xpath1, xpath2]
    scraped_elements = []

    # Wait for element to appear and grab it. Close driver
    for xpath in xpaths:
        try:
            element = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, xpath)))
            scraped_elements.append(element)
        except:
            scraped_elements.append(None)
            
    # Extract the contact information
    emails = []
    for element in scraped_elements:
        if element:
            contact_info = element.text
            # old_email_regex = r'[^@\s]+@[^@\s]+'
            # email_regex = r'[\w\.-]+@[\w\.-]+'
            # match = re.search(email_regex, contact_info)
            # if match:
            #     email = match.group(1)
            #     return email
            # else:
            email_regex = re.compile(r'[\w\.-]+@[\w\.-]+')
            email = email_regex.findall(contact_info) # Returns a list
            if len(email) > 0:
                for info in email:
                    emails.append(info)

    return emails


def scrape_email_from_facebook(link, driver):
    """
    Scrapes email from Facebook given a link.

    Args:
        link (url string): A string containing the URL for artist's Facebook profile.

    Returns:
        email (string): A string containing the email address of the artist if there is one. 
    
    """
    # Load the page
    driver.get(link)
    time.sleep(2)

    # Simulate pressing the Escape key
    actions = ActionChains(driver)
    actions.send_keys(Keys.ESCAPE)
    actions.perform()
    time.sleep(1.5)

    # Get page source and close driver
    page_source = driver.page_source

    # Parse page source
    soup = BeautifulSoup(page_source, "html.parser")
    text = str(soup.find_all('span', class_='x193iq5w')) # Class is for FB only

    # Find email with the regular expression
    email_regex = re.compile(r'[\w\.-]+@[\w\.-]+')
    email = email_regex.findall(text) # Returns a list

    return email
    

def create_spreadsheet(list_of_all_artists):
    """
    Creates an excel spreadsheet from a list of dictionaries of artists.

    Args:
        list_of_all_artists (list): A list of dictionaries of artists.
    """
    # Create a Pandas dataframe from the list of dictionaries of artists
    df = pd.DataFrame(list_of_all_artists)

    # Write the dataframe to an excel spreadsheet
    df.to_excel('artists.xlsx', index=False)
    

if __name__ == '__main__':

    # Set up Spotify API credentials
    load_dotenv()
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    token = get_token(client_id, client_secret)

    # Set up search criteria
    max_followers = 5e5
    release_year = '2023'
    # genre_list = ['pop', 'hip hop', 'country', 'r&b', 'metal', 'punk', 'indie', 'alternative', 'rap', 'latin', 'christian']
    genre_list = ['rap']
    country_codes = ['US']

    # Instantiate variables
    total_artists = 0
    delay = 0
    list_of_all_artists = []

    # Generate a compiled list of all artists and their dict info
    for genre in genre_list:
        for country in country_codes:

            artists = search_for_artists(token, max_followers, genre, country)
            total_artists += len(artists)
            list_of_all_artists.append(artists)
            time.sleep(1)
            print("Going to the next country")
        print("Going to the next genere")

        # Delay to try to avoid exceeding rate limit
        delay += 1
        if delay == 3:
            time.sleep(60)
            delay = 0
        time.sleep(1)

    for artist_by_country in list_of_all_artists:
        print(f"Total artists for this country: {len(artist_by_country)}")


    # Remove all artists who do not have recent tracks
    print("Going to filter out artists by recent tracks")
    for all_artists_in_each_country in list_of_all_artists:
        artists_to_delete = []
        for artist_id in all_artists_in_each_country:
            if not has_recent_track(token, artist_id, release_year, all_artists_in_each_country[artist_id]['country']):
                artists_to_delete.append(artist_id)
        print(f"Removing {len(artists_to_delete)} artists")    
        for artist in artists_to_delete:
            del all_artists_in_each_country[artist]
    
    # Print to console number of artists
    for artist_by_country in list_of_all_artists:
        print(f"Remaining artists for this country: {len(artist_by_country)}")
    
    print(list_of_all_artists)
    
    # Scrape social media links from each artist
    # print("Going to scrape emails")
    # for all_artists_in_each_country in list_of_all_artists:
    #     for artist_id in all_artists_in_each_country:
    #         links = scrape_social_media_links(artist_id)
    #         emails = scrape_email_addresses(links)
    #         all_artists_in_each_country[artist_id]['emails'] = emails
    #     print("Scraped social media links for this country")

    # Create an excel spreadsheet
    # create_spreadsheet(list_of_all_artists)
    # print("Spreadsheet created")