# JSON level reader

import json, os

# Read level
def read_level():
    # Open file from full path (just in case the script is being ran from somewhere other than py-games/src/platformer/level_creator)
    file = open(os.path.dirname(os.path.abspath(__file__)) + "\..\level.json", "r")
    # Python dict
    try:
        data = json.load(file)
    except Exception:
        print("Couldn't read level, data could be corrupted.")
    # Close file
    file.close()
    # Return Python list
    return data["level"]


# Write level
def write_level(data):
    # Same as above...
    file = open(os.path.dirname(os.path.abspath(__file__)) + "\..\level.json", "w")
    # Write over file
    file.write('{"level":' + json.dumps(data, separators=(",", ":")) + "}\n")
    # Close file
    file.close()
