from PySide6.QtWidgets import QLabel


class ViewLabel(QLabel):
    def __init__(self, text='', font='', pixmap=''):
        super().__init__()
        if text:
            self.setText(text)
            self.setFont(font)
        if pixmap:
            self.setPixmap(pixmap)
