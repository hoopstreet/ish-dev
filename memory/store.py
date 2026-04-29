import json
import os

DB = "memory/logs.json"

def load():
    if os.path.exists(DB):
        with open(DB) as f:
            return json.load(f)
    return []

def save(entry):
    data = load()
    data.append(entry)
    with open(DB, "w") as f:
        json.dump(data, f, indent=2)
