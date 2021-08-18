# JSON level reader

import json, os

# Read level
def read_level():
    # Open file from full path (just in case the script is being ran from somewhere other than py-games/src/platformer)
    file = open("level.json", "r")
    # Python dict
    data = json.load(file)
    # Return Python list
    return data["level"]
