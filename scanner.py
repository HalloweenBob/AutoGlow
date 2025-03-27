# scanner.py

import os
import json
import librosa

def scan_and_cache_beats(audio_folder):
    scanned = 0
    skipped = 0

    for filename in os.listdir(audio_folder):
        if filename.lower().endswith((".mp3", ".wav")):
            filepath = os.path.join(audio_folder, filename)
            beat_file = filepath + ".beat.json"

            if os.path.exists(beat_file):
                skipped += 1
                continue

            print(f"🔍 Scanning: {filename}")
            y, sr = librosa.load(filepath)
            tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
            beat_times = librosa.frames_to_time(beats, sr=sr).tolist()

            data = {
                "filename": filename,
                "tempo": float(tempo),
                "beats": [float(b) for b in beat_times]
            }

            with open(beat_file, "w") as f:
                json.dump(data, f, indent=2)

            scanned += 1

    return scanned, skipped
