from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QFont


class ClickButton(QPushButton):
    def __init__(self, text, slot):
        super().__init__()
        self.setText(text)
        self.clicked.connect(slot)
        self.font_normal = QFont('Arial', 10)
        self.setFont(self.font_normal)
        self.setFixedHeight(30)
        self.setProperty('class', 'normal-btn')
