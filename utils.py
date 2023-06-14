import json
import openpyxl
import pandas as pd



def import_json_files(file_name):
    """Read in and imports json files. Returns a list"""

    with open(file_name) as f:
        data = json.load(f)
    
    return data


def export_to_json_file(file_name:str, data:list):
    """Exports artists to a JSON file"""

    with open(file_name, "w") as file:
        json.dump(data, file, indent=2)


def export_to_excel(artists, excel_file_name):

    # Create an empty DataFrame
    df = pd.DataFrame()

    # Iterate over each key-value pair in the JSON data
    for key, value in artists.items():
        # Create a new column with the key as the name
        df[key] = pd.Series(value)

        # Remove unnecessary characters from the email and replace links with Spotify link
        for key2 in df[key].keys():
            if key2 == 'email':
                df[key]['email'] = ', '.join(df[key]['email'])            

    # Transpose the DF to have keys as columns and values as rows
    df = df.transpose()

    # Export the DF to an Excel file
    df.to_excel(f'{excel_file_name}.xlsx', index=False)



def import_from_excel(excel_file):

    # Read the Excel file into a pandas DataFrame
    df = pd.read_excel(excel_file)

    # Convert the DataFrame to a dictionary
    data = df.to_dict(orient='index')

    # Export the dictionary to a JSON file
    with open('output.json', 'w') as json_file:
        json.dump(data, json_file, indent=2)