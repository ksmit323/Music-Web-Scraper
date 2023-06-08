from utils import import_json_files, export_to_json_file
import sys
import time
import pandas as pd
import json
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows


"""Create a new list with only the artists that have emails"""

# # Check for correct usage
# if (len(sys.argv) < 2):
#     print("Don't forgot to include the file!")
#     print("Usage: python scrape_emails.py <json file>")
#     sys.exit(1)

# artists = import_json_files(sys.argv[1])

# delete_artists = []

# # Delete artists with no emails
# for artist in artists:
#     if len(artists[artist]['email']) == 0:
#         delete_artists.append(artist)

# for artist in delete_artists:
#     del artists[artist]

# print(f"{len(artists.keys())} with emails")
# export_to_json_file("latin_emails.json", artists)

# time.sleep(2)

"""Clean email data and export to Excel file"""

# Load the JSON data from file
data = import_json_files(sys.argv[1])

# Create an empty DataFrame
df = pd.DataFrame()

# Iterate over each key-value pair in the JSON data
for key, value in data.items():
    # Create a new column with the key as the name
    df[key] = pd.Series(value)

    # Remove unnecessary characters from the email and replace links with Spotify link
    for key2 in df[key].keys():
        if key2 == 'email':
            df[key]['email'] = ', '.join(df[key]['email'])            

# Transpose the DF to have keys as columns and values as rows
df = df.transpose()

# Export the DF to an Excel file
df.to_excel('latin.xlsx', index=False)