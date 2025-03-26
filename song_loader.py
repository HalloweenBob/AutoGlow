# song_loader.py

import os
import shutil
import json
from PySide6.QtWidgets import QFileDialog, QMessageBox


class SongLoader:
    def __init__(self, parent=None):
        self.parent = parent
        self.config = self._load_config()
        self.target_dir = self.config.get("default_audio_folder", "C:/routines/songs")
        os.makedirs(self.target_dir, exist_ok=True)

    def _load_config(self):
        with open("config.json", "r") as f:
            return json.load(f)

    def load_single_song(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self.parent,
            "Select a song to add to the library",
            self.target_dir,
            "Audio Files (*.mp3 *.wav)"
        )

        if file_path:
            self._copy_to_library([file_path])

    def load_all_from_folder(self):
        folder_path = QFileDialog.getExistingDirectory(
            self.parent,
            "Select folder containing songs"
        )

        if folder_path:
            all_files = [
                os.path.join(folder_path, f)
                for f in os.listdir(folder_path)
                if f.lower().endswith(('.mp3', '.wav'))
            ]
            self._copy_to_library(all_files)

    def load_multiple_songs(self):
        file_paths, _ = QFileDialog.getOpenFileNames(
            self.parent,
            "Select songs to add to the library",
            self.target_dir,
            "Audio Files (*.mp3 *.wav)"
        )

        if file_paths:
            self._copy_to_library(file_paths)

    def _copy_to_library(self, file_paths):
        count = 0

        for file_path in file_paths:
            try:
                dest_path = os.path.join(self.target_dir, os.path.basename(file_path))
                shutil.copy(file_path, dest_path)
                count += 1
            except Exception as e:
                print(f"❌ Failed to copy {file_path}: {e}")

        QMessageBox.information(
            self.parent,
            "Songs Added",
            f"{count} song(s) successfully added to the library."
        )
