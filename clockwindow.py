from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QMovie, QFont


class ClockWindow(object):


    def __init__(self, MainWindow, width, height):
        MainWindow.setObjectName("MainWindow")
        dim = MainWindow.size()
        self.WIDTH = width
        self.HEIGHT = height
        self.RATIO = self.WIDTH / self.HEIGHT
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, self.WIDTH, self.HEIGHT))
        self.label.setObjectName("label")

        self.display_text = QtWidgets.QLabel(self.centralwidget)
        self.display_text.setObjectName("display_text")
        self.display_text.setFont(QFont('Helvetica', 30))
        self.display_text.setStyleSheet("background-color: black; color: green")
        self.set_display_text("Loading...", "green")

        MainWindow.setCentralWidget(self.centralwidget)

    def update_gif(self, gif_path):
        self.movie = QMovie(gif_path)
        self.label.setMovie(self.movie)
        self.movie.start()
        self.movie.setScaledSize(self.label.size())

    def set_display_text(self, text, color):
        self.display_text.setStyleSheet(f"background-color: black; color: {color}")
        self.display_text.setText(text)
        self.display_text.move(self.WIDTH / 2 - self._label_width(self.display_text)/2, self.HEIGHT - self._label_height(self.display_text))
        self.display_text.setFixedWidth(self._label_width(self.display_text))

    def _label_width(self, label):
        return label.fontMetrics().boundingRect(label.text()).width()

    def _label_height(self, label):
        return label.fontMetrics().boundingRect(label.text()).height()