import os
import json

def load_config(path="config.json"):
    with open(path, "r") as f:
        config = json.load(f)

    # Auto-create directories from config
    audio_folder = config.get("default_audio_folder", "C:/routines/songs")
    routine_folder = config.get("default_routine_folder", "C:/routines")

    os.makedirs(audio_folder, exist_ok=True)
    os.makedirs(routine_folder, exist_ok=True)

    return config
