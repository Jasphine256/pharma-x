from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QIcon, QFont
import sys
import os


class DashboardButton(QPushButton):
    def __init__(self, text, slot, icon_path):
        super().__init__()
        if getattr(sys, 'frozen', False):
            # If the application is run as a bundle (e.g. PyInstaller)
            self.images_dir = os.path.join(sys._MEIPASS, 'images')
        else:
            # If the application is run from the script directly
            self.images_dir = os.path.join(os.path.abspath("."), 'images')

        self.setText(text)
        self.font_mid = QFont('Arial', 12)
        self.setFont(self.font_mid)
        self.setMinimumHeight(40)
        self.icon = QIcon(os.path.join(self.images_dir, icon_path))
        self.setIcon(self.icon)
        self.clicked.connect(slot)
        self.setProperty('class', 'dash-btn')

