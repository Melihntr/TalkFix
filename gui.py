from PySide6.QtWidgets import QMainWindow, QVBoxLayout,QHBoxLayout, QWidget, QPushButton, QComboBox, QLineEdit, QLabel, QFrame
from PySide6.QtCore import Qt, QPropertyAnimation, QPoint
from tray import TrayIcon
from converter import convert_text_to_tone


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TalkFix")
        self.setGeometry(100, 100, 400, 300)

        # Initialize layout and widgets
        self.init_ui()

        # Initialize system tray functionality
        self.tray_icon = TrayIcon(self)

    def init_ui(self):
        layout = QVBoxLayout()

        # Input field for the text
        self.input_text = QLineEdit(self)
        self.input_text.setPlaceholderText("Enter text to transform")
        layout.addWidget(self.input_text)

        # ComboBox for selecting tone
        self.tone_selector = QComboBox(self)
        self.tone_selector.addItems(["Formal", "Academic", "Sarcastic", "Angry", "Friendly"])
        layout.addWidget(self.tone_selector)

        # Button to initiate transformation
        self.convert_button = QPushButton("Convert", self)
        self.convert_button.clicked.connect(self.convert_text)
        layout.addWidget(self.convert_button)

        # Label to show the transformed text
        self.result_label = QLabel(self)
        layout.addWidget(self.result_label)

        # Layout for the "How to Use" button
        self.how_to_use_button_layout = QHBoxLayout()

        # "How to Use" button to toggle the instructions
        self.how_to_use_button = QPushButton("How to Use", self)
        self.how_to_use_button.clicked.connect(self.toggle_instructions)
        self.how_to_use_button_layout.addWidget(self.how_to_use_button)

        # Add the button layout to the main layout
        layout.addLayout(self.how_to_use_button_layout)

        # Collapsible section for "How to Use" text
        self.instructions_frame = QFrame(self)
        self.instructions_frame.setFrameShape(QFrame.StyledPanel)
        self.instructions_frame.setFrameShadow(QFrame.Raised)

        # Instructions text
        self.instructions_text = QLabel(
            "1. Enter the text you want to transform.\n"
            "2. Select the tone you'd like the text to be rewritten in.\n"
            "3. Click the 'Convert' button to see the transformed text.\n"
            "4. You can click 'How to Use' again to hide these instructions.",
            self
        )
        layout_instructions = QVBoxLayout()
        layout_instructions.addWidget(self.instructions_text)
        self.instructions_frame.setLayout(layout_instructions)

        # Initially hide the instructions
        self.instructions_frame.setVisible(False)

        # Add the frame to the layout
        layout.addWidget(self.instructions_frame)

        # Set the layout for the central widget
        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def convert_text(self):
        input_text = self.input_text.text()
        selected_tone = self.tone_selector.currentText()

        # Use the converter to transform the text based on the selected tone
        transformed_text = convert_text_to_tone(input_text, selected_tone)
        self.result_label.setText(f"Transformed Text:\n{transformed_text}")

    def toggle_instructions(self):
        """Toggle the visibility of the instructions panel with animation."""
        if self.instructions_frame.isVisible():
            # Slide up to hide the instructions
            self.slide_up()
        else:
            # Slide down to show the instructions
            self.slide_down()

    def slide_down(self):
        """Slide down the instructions with animation."""
        self.instructions_frame.setVisible(True)  # Make sure it's visible before animation
        animation = QPropertyAnimation(self.instructions_frame, b"pos")
        animation.setDuration(300)
        animation.setStartValue(QPoint(self.instructions_frame.x(), self.instructions_frame.y() - self.instructions_frame.height()))
        animation.setEndValue(QPoint(self.instructions_frame.x(), self.instructions_frame.y()))
        animation.start()

    def slide_up(self):
        """Slide up to hide the instructions with animation."""
        animation = QPropertyAnimation(self.instructions_frame, b"pos")
        animation.setDuration(300)
        animation.setStartValue(QPoint(self.instructions_frame.x(), self.instructions_frame.y()))
        animation.setEndValue(QPoint(self.instructions_frame.x(), self.instructions_frame.y() - self.instructions_frame.height()))
        animation.finished.connect(lambda: self.instructions_frame.setVisible(False))  # Hide after animation
        animation.start()

    def closeEvent(self, event):
        """Override default close to minimize to tray instead of exiting."""
        event.ignore()
        self.tray_icon.minimize_to_tray()
