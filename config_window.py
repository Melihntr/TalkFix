from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel, QComboBox, QPushButton
from styles import style_prompts


class ConfigWindow(QMainWindow):
    def __init__(self, on_start_callback):
        super().__init__()
        self.setWindowTitle("Text Converter Setup")
        self.setFixedSize(400, 200)

        self.style_combo = QComboBox()
        self.style_combo.addItems(style_prompts.keys())

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Select Style:"))
        layout.addWidget(self.style_combo)

        start_btn = QPushButton("Start Converter")
        start_btn.clicked.connect(lambda: on_start_callback(self.style_combo.currentText()))
        layout.addWidget(start_btn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
