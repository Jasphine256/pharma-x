from entry import EntryWindow
import blender_stylesheet
from qtmodern import windows as win
from PySide6.QtWidgets import QApplication
import sys
import qdarktheme


if __name__ == "__main__":
    def load_stylesheet(app):
        with open('styles.qss', 'r') as file:
            app.setStyleSheet(file.read())

    # qdarktheme.setup_theme()
    # blender_stylesheet.setup(app)
    # blender_stylesheet.apply_blender_stylesheet(app)
    app = QApplication(sys.argv)

    entry_window = EntryWindow()
    mw = win.ModernWindow(entry_window)
    mw.show()
    app.setStyle('fusion')
    load_stylesheet(app)

    app.exec()
