# routine_generator.py

import json
import os
import random
from datetime import datetime

def generate_routine(beat_data, light_count, offset_ms, patterns):
    routine = {
        "version": 1.0,
        "generated": datetime.now().isoformat(),
        "light_count": light_count,
        "offset_ms": offset_ms,
        "events": []
    }

    beats = beat_data["beats"]
    tempo = beat_data.get("tempo", 120)

    for beat_time in beats:
        pattern = random.choice(patterns)
        step_time = beat_time + (offset_ms / 1000.0)

        # Simulate a very basic chase pattern
        for i in range(light_count):
            routine["events"].append({
                "start_time": round(step_time + i * 0.1, 3),
                "end_time": round(step_time + i * 0.1 + 0.2, 3),
                "light": i,
                "intensity": 255
            })

    return routine


def save_routine(routine_data, song_filename, output_dir="C:/routines"):
    base_name = os.path.basename(song_filename)
    name = os.path.splitext(base_name)[0]
    routine_file = os.path.join(output_dir, name + ".routine")

    with open(routine_file, "w") as f:
        json.dump(routine_data, f, indent=2)

    return routine_file
