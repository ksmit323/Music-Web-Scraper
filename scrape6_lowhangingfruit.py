from utils import *
from helper import *
import sys


# Check for correct usage
if (len(sys.argv) < 2):
    print("Don't forgot to include the file!")
    sys.exit(1)


data = import_json_files(sys.argv[1])

low_hanging_fruit = import_json_files("low_hanging_fruit.json")

for artist in data:
    try:
        if data[artist]['monthly listeners'] <= 40000:
            low_hanging_fruit[artist] = data[artist]
    except (KeyError, TypeError):
        continue

low_hanging_fruit = dict(sorted(low_hanging_fruit.items(), key=lambda x: x[1]["monthly listeners"], reverse=True))

export_to_json_file("low_hanging_fruit_reggaeton.json", low_hanging_fruit)





