import json, os

def read_level(filePath):
    file = os.open(file, "r")
    data = json.load(file)
    return data["level"]
