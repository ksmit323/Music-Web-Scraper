from utils import *
import sys
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows


"""Create a new list with only the artists that have emails"""

# Check for correct usage
if (len(sys.argv) < 2):
    print("Don't forgot to include the file!")
    print("Usage: python scrape_emails.py <json file>")
    sys.exit(1)

artists = import_json_files(sys.argv[1])

delete_artists = []

# Delete artists with no emails
for artist in artists:
    if len(artists[artist]['email']) == 0:
        delete_artists.append(artist)

for artist in delete_artists:
    del artists[artist]

# Export data to JSON file
print(f"{len(artists.keys())} artists with emails")
export_to_json_file("emails_"+sys.argv[1], artists)

# Clean email data and export to Excel file
export_to_excel(artists, 'emails_' + sys.argv[1])

