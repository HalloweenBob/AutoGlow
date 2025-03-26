# pattern_engine.py

import json
import random
from pathlib import Path

BALLOON_COUNT = 6

def load_patterns(path="patterns.json"):
    with open(path, "r") as f:
        return json.load(f)

def calculate_steps(pattern, balloon_count):
    if isinstance(pattern["steps"], int):
        return pattern["steps"]
    elif pattern["steps"] == "per_balloon":
        return balloon_count
    elif pattern["steps"] == "half_balloon_count":
        return balloon_count // 2
    elif pattern["steps"] == "double_balloon_count":
        return balloon_count * 2
    else:
        return -1  # Invalid or unknown step mode

def pattern_fits(pattern, section_beats, balloon_count):
    steps = calculate_steps(pattern, balloon_count)
    if steps <= 0:
        return False
    return section_beats % steps == 0

def select_pattern(section_beats, recent_patterns, section_type, balloon_count=6, pattern_group=None):
    patterns = load_patterns()
    eligible = []

    for p in patterns:
        if not pattern_fits(p, section_beats, balloon_count):
            continue

        name = p["name"]
        limit = p.get("repeat_limit", 2)
        recent_count = recent_patterns[-limit:].count(name)

        if pattern_group and name in pattern_group.values():
            # Allow reuse if this section belongs to a repeating group
            eligible.append(p)
        elif recent_count < limit:
            eligible.append(p)

    if not eligible:
        return None

    chosen = random.choice(eligible)
    return chosen

# 🔍 TEST
if __name__ == "__main__":
    recent = ["Left Cascade", "Left Cascade"]
    section_beats = 12
    section_type = "verse"
    pattern_group = None  # Or set to "Chorus A"

    selected = select_pattern(section_beats, recent, section_type, BALLOON_COUNT, pattern_group)
    if selected:
        print(f"🎵 Selected pattern: {selected['name']}")
    else:
        print("⚠️ No suitable pattern found.")
