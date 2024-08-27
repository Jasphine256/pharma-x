import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt


class BarCanvas(QWidget):
    def __init__(self, parent=None):
        super(BarCanvas, self).__init__(parent)
        self.figure, self.ax = plt.subplots()
        self.figure.subplots_adjust(bottom=0.3)
        self.canvas = FigureCanvas(self.figure)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)
        self.setMaximumHeight(100)

    def plot(self, data, labels):
        self.ax.clear()
        self.ax.barh(labels, data)
        self.canvas.draw()
