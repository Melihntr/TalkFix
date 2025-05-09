from PySide6.QtWidgets import QSystemTrayIcon, QMenu
from PySide6.QtGui import QIcon, QAction
import sys

class TrayIcon:
    def __init__(self, main_window):
        self.main_window = main_window

        # Setup system tray
        self.tray_icon = QSystemTrayIcon(QIcon("icon.png"), self.main_window)
        tray_menu = QMenu()

        restore_action = QAction("Restore", self.main_window)
        restore_action.triggered.connect(self.show_main_window)
        tray_menu.addAction(restore_action)

        exit_action = QAction("Exit", self.main_window)
        exit_action.triggered.connect(self.exit_app)
        tray_menu.addAction(exit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.on_tray_icon_activated)

    def show_main_window(self):
        self.main_window.show()
        self.tray_icon.hide()

    def exit_app(self):
        self.tray_icon.hide()
        sys.exit()

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:  # Left click
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
