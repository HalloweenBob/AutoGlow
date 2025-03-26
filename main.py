# main.py

import sys
import json
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QFileDialog, QSpinBox, QSlider, QLineEdit
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

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

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        top_bar = QHBoxLayout()

        # Load Audio Button
        self.load_button = QPushButton("Select Audio File")
        self.load_button.clicked.connect(self.load_audio_file)
        top_bar.addWidget(self.load_button)

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
        self.offset_slider.setRange(-1000, 1000)
        self.offset_slider.setValue(self.config["default_offset_ms"])
        self.offset_slider.setTickInterval(50)
        self.offset_slider.setFixedWidth(150)
        top_bar.addWidget(self.offset_slider)

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
            dot.setStyleSheet("color: red;")
            self.dot_row.addWidget(dot)

    def on_light_count_changed(self, value):
        self.update_dot_preview(value)

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
