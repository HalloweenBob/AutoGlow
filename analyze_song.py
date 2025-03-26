import librosa
import json
import os
from tkinter import filedialog, Tk

# Load config file
with open("config.json", "r") as f:
    config = json.load(f)

# Get the songs folder from config
songs_path = config.get("default_audio_folder", "C:/routines/songs")

# Ensure folder exists
os.makedirs(songs_path, exist_ok=True)

# File picker dialog to select audio file
root = Tk()
root.withdraw()  # Hide the small tkinter root window
filename = filedialog.askopenfilename(
    title="Select a song to analyze",
    initialdir=songs_path,
    filetypes=[("Audio Files", "*.wav *.mp3")]
)

if not filename:
    print("❌ No file selected.")
    exit()

# Load and analyze song
y, sr = librosa.load(filename)
tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
beat_times = librosa.frames_to_time(beats, sr=sr)

# Display results
print(f"🎵 Analyzed: {os.path.basename(filename)}")
print(f"🎧 Tempo: {tempo:.2f} BPM")
print(f"🕒 Number of beats: {len(beat_times)}")
print(f"📍 First 10 beat times: {[round(bt, 2) for bt in beat_times[:10]]}")
