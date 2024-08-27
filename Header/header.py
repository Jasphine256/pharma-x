from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PySide6.QtGui import QFont


class Header(QWidget):
    def __init__(self, title):
        super().__init__()
        self.header_layout = QHBoxLayout()
        self.setLayout(self.header_layout)
        self.setFixedHeight(60)
        self.font_large = QFont('Arial', 20, QFont.Bold)

        self.users_label = QLabel(title)
        self.users_label.setFont(self.font_large)
        self.header_layout.addWidget(self.users_label)

    def set_text(self, text):
        self.users_label.setText(text)
