import json
import openpyxl



def import_json_files(file_name):
    """Read in and imports json files. Returns a list"""

    with open(file_name) as f:
        data = json.load(f)
    
    return data


def export_to_json_file(file_name, artists):
    """Exports artists to a JSON file"""

    with open(file_name, "w") as file:
        json.dump(artists, file, indent=2)


def upload_to_excel(data_list, file_name):
    # Create a new Excel workbook
    workbook = openpyxl.Workbook()

    # Select an active sheet
    sheet = workbook.active

    # Iterate over the data list and write each entry to excel
    for index, url in enumerate(data_list, start=1):
        cell = sheet.cell(row=index, column=1)
        cell.value = url
        # cell.hyperlink = url

    # Save the workbook
    workbook.save(file_name)