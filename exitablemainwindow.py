from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow


class ExitableMainWindow(QMainWindow):

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()