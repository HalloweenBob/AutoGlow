# generate_test_timeline.py

from pattern_engine import select_pattern
import json

BALLOON_COUNT = 6

# Mock recent pattern memory (simulating prior section usage)
recent_patterns = []

# Sample structure of song (beats are assumed to be evenly spaced)
song_sections = [
    {"section_type": "intro",   "beats": 12, "pattern_group": "Intro"},
    {"section_type": "verse",   "beats": 18, "pattern_group": "Verse A"},
    {"section_type": "chorus",  "beats": 24, "pattern_group": "Chorus A"},
    {"section_type": "verse",   "beats": 18, "pattern_group": "Verse A"},
    {"section_type": "chorus",  "beats": 24, "pattern_group": "Chorus A"},
    {"section_type": "bridge",  "beats": 10, "pattern_group": "Bridge"},
    {"section_type": "outro",   "beats": 12, "pattern_group": "Outro"}
]

# Print generated timeline
print("🎵 Auto Glow Pattern Schedule:\n")

for i, section in enumerate(song_sections):
    pattern = select_pattern(
        section_beats=section["beats"],
        recent_patterns=recent_patterns,
        section_type=section["section_type"],
        balloon_count=BALLOON_COUNT,
        pattern_group=section["pattern_group"]
    )

    if pattern:
        recent_patterns.append(pattern["name"])
        print(f"Section {i+1} ({section['section_type']}): {pattern['name']} ({pattern.get('steps', 'dynamic')} steps)")
    else:
        print(f"Section {i+1} ({section['section_type']}): ❌ No matching pattern found")
