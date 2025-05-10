from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QPushButton, QComboBox, QLineEdit, QLabel, QFrame, QTextEdit
)
from PySide6.QtGui import QMouseEvent, QIcon, QPixmap
from PySide6.QtCore import Qt, QPoint
from tray import TrayIcon
from converter import convert_text_to_tone


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TalkFix")
        self.setGeometry(100, 100, 400, 350)
        self.setWindowIcon(QIcon("icon5.png"))
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.old_pos = None
        self.is_maximized = False

        self.apply_styles()
        self.init_ui()
        self.tray_icon = TrayIcon(self)

    def init_ui(self):
        layout = QVBoxLayout()

        # === Custom Title Bar ===
        title_bar = QHBoxLayout()

        # Logo - Directly add the pixmap to the layout
        logo_label = QLabel()
        pixmap = QPixmap("icon4.png").scaled(130, 38, Qt.KeepAspectRatio)
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignLeft)  # Align the logo to the left

        # Remove the border and set background to match the window's background
        logo_label.setStyleSheet("""
            QLabel {
                background-color: transparent;
                border: none;
            }
        """)

        title_bar.addWidget(logo_label)

        # App Title (commented out as it's not in use)
        # title_label = QLabel("TalkFix")
        # title_label.setStyleSheet("color: lightgray; font-size: 16px; font-weight: bold; margin-left: 5px;")
        # title_bar.addWidget(title_label)

        title_bar.addStretch()

        # Minimize button
        minimize_button = QPushButton("-")
        minimize_button.setFixedSize(35, 35)
        minimize_button.setObjectName("minimizeButton")
        minimize_button.clicked.connect(self.showMinimized)
        title_bar.addWidget(minimize_button)

        # Maximize/Restore button
        self.maximize_button = QPushButton("🗖")
        self.maximize_button.setFixedSize(35,35)
        self.maximize_button.setObjectName("maximizeButton")
        self.maximize_button.clicked.connect(self.toggle_maximize_restore)
        title_bar.addWidget(self.maximize_button)

        # Close button
        close_button = QPushButton("✕")
        close_button.setFixedSize(35, 35)
        close_button.setObjectName("closeButton")
        close_button.clicked.connect(self.close)
        title_bar.addWidget(close_button)

        layout.addLayout(title_bar)

        # Input field
        self.input_text = QLineEdit(self)
        self.input_text.setPlaceholderText("Enter text to transform")
        layout.addWidget(self.input_text)

        # Tone selector
        self.tone_selector = QComboBox(self)
        self.tone_selector.addItems(["Formal", "Academic", "Sarcastic", "Angry", "Friendly"])
        layout.addWidget(self.tone_selector)

        # Convert button
        self.convert_button = QPushButton("Convert", self)
        self.convert_button.clicked.connect(self.convert_text)
        layout.addWidget(self.convert_button)

        # Minimize to tray button
        self.minimize_button = QPushButton("Minimize to Tray", self)
        self.minimize_button.clicked.connect(self.minimize_to_tray)
        layout.addWidget(self.minimize_button)

        # Text area for transformed text
        self.result_textbox = QTextEdit(self)
        self.result_textbox.setPlaceholderText("Transformed text will appear here")
        self.result_textbox.setReadOnly(True)
        layout.addWidget(self.result_textbox)

        # How to Use button
        self.how_to_use_button = QPushButton("How to Use", self)
        self.how_to_use_button.clicked.connect(self.toggle_instructions)
        layout.addWidget(self.how_to_use_button)

        # Instructions panel
        self.instructions_frame = QFrame(self)
        self.instructions_frame.setFrameShape(QFrame.StyledPanel)
        self.instructions_text = QLabel(
            "🔧 This is a tool designed for quick use.\n"
            "⚙️ Therefore minimized tray usage is suggested.\n"
            "📋 Copy any text.\n"
            "🎯 Press shortcut(Control + Shift + F) or click 'Convert'.\n"
            "📎 Result is copied to your clipboard.\n"
            "🧠 Adjust tone from dropdown.\n"
            "ℹ️ GUI only exists to get new users familiar with the tool.\n"
            "💁 Seriously, start using the tray already.\n",
            self
        )
        layout_instructions = QVBoxLayout()
        layout_instructions.addWidget(self.instructions_text)
        self.instructions_frame.setLayout(layout_instructions)
        self.instructions_frame.setVisible(False)
        layout.addWidget(self.instructions_frame)

        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def toggle_maximize_restore(self):
        if self.is_maximized:
            self.showNormal()
            self.is_maximized = False
            self.maximize_button.setText("🗖")
        else:
            self.showMaximized()
            self.is_maximized = True
            self.maximize_button.setText("🗗")

    def convert_text(self):
        input_text = self.input_text.text()
        selected_tone = self.tone_selector.currentText()
        transformed_text = convert_text_to_tone(input_text, selected_tone)
        self.result_textbox.setPlainText(transformed_text)

    def toggle_instructions(self):
        self.instructions_frame.setVisible(not self.instructions_frame.isVisible())

    def minimize_to_tray(self):
        self.tray_icon.minimize_to_tray()

    def closeEvent(self, event):
        event.ignore()
        self.tray_icon.minimize_to_tray()

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #1E1e1e;
                color: lightgray;
                font-family: Arial;
                font-size: 14px;
            }

            QLabel#titleLabel {
                color: lightgray;
            }

            QLineEdit, QTextEdit, QComboBox {
                background-color: #1E1F22;
                color: lightgray;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 5px;
            }

            QPushButton {
                background-color: #4B0082;
                color: lightgray;
                border: none;
                border-radius: 6px;
                padding: 6px 10px;
            }

            QPushButton:hover {
                background-color: #5E0698;
            }

            QFrame {
                background-color: #1E1F22;
                border: 1px solid #333;
                border-radius: 5px;
            }

            QPushButton#minimizeButton, QPushButton#maximizeButton, QPushButton#closeButton {
                background-color: transparent;
                color: lightgray;
                border: none;
            }

            QPushButton#minimizeButton:hover, QPushButton#maximizeButton:hover {
                background-color: #333;
            }

            QPushButton#closeButton:hover {
                background-color: red;
            }
        """)

    # === Support dragging ===
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.old_pos is not None:
            delta = event.globalPosition().toPoint() - self.old_pos
            self.move(self.pos() + delta)
            self.old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.old_pos = None
