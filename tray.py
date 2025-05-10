from PySide6.QtWidgets import QSystemTrayIcon, QMenu
from PySide6.QtGui import QIcon, QAction
import pyperclip
import sys
import threading
import keyboard  # Global key listener

from converter import convert_text_to_tone  # Your main logic
from config import load_tone, save_tone  # Config management

class TrayIcon:
    def __init__(self, main_window):
        self.main_window = main_window
        self.selected_tone = load_tone()

        self.tray_icon = QSystemTrayIcon(QIcon("icon5.png"), self.main_window)
        tray_menu = QMenu()

        # Style for tray menu
        tray_menu.setStyleSheet("""
            QMenu {
                background-color: #1E1F22;
                color: lightgray;
                border: 1px solid #333;
                padding: 5px;
            }

            QMenu::item {
                background-color: transparent;
                padding: 6px 20px;
            }

            QMenu::item:selected {
                background-color: #4B0082;  /* Dark purple */
                color: white;
            }
        """)

        # Convert Clipboard action
        convert_action = QAction("Convert Clipboard", self.main_window)
        convert_action.triggered.connect(self.convert_clipboard_text)
        tray_menu.addAction(convert_action)

        # Show GUI
        gui_action = QAction("Settings / GUI", self.main_window)
        gui_action.triggered.connect(self.show_main_window)
        tray_menu.addAction(gui_action)

        # Tone selector submenu with same style
        tone_menu = QMenu("Choose Tone")
        tone_menu.setStyleSheet("""
            QMenu {
                background-color: #1E1F22;
                color: lightgray;
                border: 1px solid #333;
                padding: 5px;
            }

            QMenu::item {
                background-color: transparent;
                padding: 6px 20px;
            }

            QMenu::item:selected {
                background-color: #4B0082;
                color: white;
            }
        """)

        available_tones = ["Formal", "Academic", "Sarcastic", "Angry", "Friendly"]
        for tone in available_tones:
            tone_action = QAction(tone, self.main_window)
            tone_action.triggered.connect(lambda checked=False, t=tone: self.set_tone(t))
            tone_menu.addAction(tone_action)

        tray_menu.addMenu(tone_menu)

        # Exit
        exit_action = QAction("Exit", self.main_window)
        exit_action.triggered.connect(self.exit_app)
        tray_menu.addAction(exit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.on_tray_icon_activated)

        # Start global key listener in a thread
        threading.Thread(target=self.start_global_listener, daemon=True).start()

    def show_main_window(self):
        self.main_window.show()
        self.tray_icon.hide()

    def exit_app(self):
        self.tray_icon.hide()
        sys.exit()

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.show_main_window()

    def minimize_to_tray(self):
        self.main_window.hide()
        self.tray_icon.show()
        self.tray_icon.showMessage(
            "TalkFix is running",
            "The app is minimized to the system tray.",
            QSystemTrayIcon.Information,
            3000
        )

    def set_tone(self, tone):
        self.selected_tone = tone
        save_tone(tone)
        self.tray_icon.showMessage(
            "Tone Selected",
            f"Tone changed to {tone}",
            QSystemTrayIcon.Information,
            2000
        )

    def convert_clipboard_text(self):
        text = pyperclip.paste()
        if not text.strip():
            self.tray_icon.showMessage(
                "No Text Found",
                "Clipboard is empty.",
                QSystemTrayIcon.Warning,
                2000
            )
            return
        try:
            result = convert_text_to_tone(text, self.selected_tone)
            pyperclip.copy(result)
            self.tray_icon.showMessage(
                "Conversion Successful",
                f"Converted to {self.selected_tone} tone. Copied to clipboard.",
                QSystemTrayIcon.Information,
                3000
            )
        except Exception as e:
            self.tray_icon.showMessage(
                "Conversion Failed",
                f"Error: {str(e)}",
                QSystemTrayIcon.Critical,
                3000
            )

    def start_global_listener(self):
        try:
            keyboard.add_hotkey("ctrl+shift+f", self.convert_clipboard_text)
            keyboard.wait()  # Blocks this thread to keep listener running
        except:
            print("Global keybind failed. You might need admin rights.")
