import json
import os

CONFIG_PATH = "config.json"
DEFAULT_TONE = "Formal"

def load_tone():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            data = json.load(f)
            return data.get("tone", DEFAULT_TONE)
    return DEFAULT_TONE

def save_tone(tone):
    with open(CONFIG_PATH, "w") as f:
        json.dump({"tone": tone}, f)
