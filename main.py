# main.py

import sys
import os
import json
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QFileDialog, QSpinBox, QSlider, QLineEdit
)
from scanner import scan_and_cache_beats
from song_loader import SongLoader
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from config_loader import load_config
from routine_generator import generate_routine, save_routine

config = load_config()
CONFIG_FILE = "config.json"

class AutoGlowApp(QWidget):
   def __init__(self):
        super().__init__()
        self.setWindowTitle("Auto Glow")
        self.setGeometry(100, 100, 900, 500)
        self.setStyleSheet("background-color: #2B0000; color: white;")
        self.font = QFont("Arial", 10)
        self.config = self.load_config()
        self.audio_file_path = None
        self.song_loader = SongLoader(self)
        self.init_ui()
        

   def init_ui(self):
        layout = QVBoxLayout()
        top_bar = QHBoxLayout()

        # Load Audio Button
        self.load_button = QPushButton("Select Audio File")
        self.load_button.clicked.connect(self.load_audio_file)
        top_bar.addWidget(self.load_button)
        scan_button = QPushButton("🔎 Scan New Songs")
        scan_button.clicked.connect(self.scan_new_songs)
        layout.addWidget(scan_button)
        generate_button = QPushButton("⚡ Generate Routine")
        generate_button.clicked.connect(self.generate_routine_for_selected_song)
        layout.addWidget(generate_button)


        # Light Count
        top_bar.addWidget(QLabel("Lights:"))
        self.light_count_spin = QSpinBox()
        self.light_count_spin.setRange(4, 15)
        self.light_count_spin.setValue(self.config["default_light_count"])
        top_bar.addWidget(self.light_count_spin)

        # DMX Start Address
        top_bar.addWidget(QLabel("DMX Start Address:"))
        self.dmx_address_input = QLineEdit()
        self.dmx_address_input.setText(str(self.config["dmx_start_address"]))
        self.dmx_address_input.setMaximumWidth(60)
        top_bar.addWidget(self.dmx_address_input)

        # Offset Slider
        top_bar.addWidget(QLabel("Offset (ms):"))
        self.offset_slider = QSlider(Qt.Horizontal)
        self.offset_slider.setRange(-1000, 0)
        self.offset_slider.setValue(self.config["default_offset_ms"])
        self.offset_slider.setTickInterval(50)
        self.offset_slider.setFixedWidth(150)
        top_bar.addWidget(self.offset_slider)

        #Load Songs To Library
        layout.addWidget(QPushButton("🎵 Load One Song", clicked=self.song_loader.load_single_song))
        layout.addWidget(QPushButton("📂 Load All Songs from Folder",          clicked=self.song_loader.load_all_from_folder))
        layout.addWidget(QPushButton("🗂️ Load Selected Songs", clicked=self.song_loader.load_multiple_songs))
        layout.addLayout(top_bar)

        # LED Dot Preview Row (visual only)
        self.dot_row = QHBoxLayout()
        self.update_dot_preview(self.light_count_spin.value())
        layout.addLayout(self.dot_row)

        # Listen to changes
        self.light_count_spin.valueChanged.connect(self.on_light_count_changed)
        self.setLayout(layout)

   def load_audio_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Audio File", "", "Audio Files (*.mp3 *.wav)")
        if file_path:
            self.audio_file_path = file_path
            print(f"Loaded audio: {file_path}")

   def update_dot_preview(self, light_count):
        # Clear existing dots
        for i in reversed(range(self.dot_row.count())):
            widget = self.dot_row.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        for _ in range(light_count):
            dot = QLabel("●")
            dot.setFont(QFont("Arial", 24))
            dot.setAlignment(Qt.AlignCenter)
            dot.setStyleSheet("color: #000000;")
            self.dot_row.addWidget(dot)

   def on_light_count_changed(self, value):
        self.update_dot_preview(value)
   
   def scan_new_songs(self):
        folder = self.config["default_audio_folder"]
        scanned, skipped = scan_and_cache_beats(folder)

        msg = f"Scanned: {scanned}\nSkipped (already scanned): {skipped}"
        print(msg)

        from PySide6.QtWidgets import QMessageBox
        QMessageBox.information(self, "Scan Complete", msg)

   def generate_routine_for_selected_song(self):
        if not self.audio_file_path:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "No Audio File", "Please select an audio file first.")
            return

        beat_file = self.audio_file_path + ".beat.json"

        if not os.path.exists(beat_file):
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Beat Map Missing", "You need to scan this song first.")
            return

        with open(beat_file, "r") as f:
            beat_data = json.load(f)

        with open("patterns.json", "r") as f:
            patterns = json.load(f)

        light_count = self.light_count_spin.value()
        offset = self.offset_slider.value()

        routine = generate_routine(beat_data, light_count, offset, patterns)
        routine_path = save_routine(routine, self.audio_file_path)

        from PySide6.QtWidgets import QMessageBox
        QMessageBox.information(self, "Routine Saved", f"Routine saved as:\n{routine_path}")


   def load_config(self):
        if Path(CONFIG_FILE).exists():
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        else:
            return {
                "default_audio_folder": "C:/routines",
                "default_offset_ms": 150,
                "default_light_count": 6,
                "dmx_start_address": 1
            }


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AutoGlowApp()
    window.show()
    sys.exit(app.exec())
  
    

