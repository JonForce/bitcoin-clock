import configparser
from pathlib import Path
import os
from PyQt5 import QtWidgets
from clockwindow import ClockWindow
import sys

from controller import Controller
from gifmanager import GifManager

BASE_DIR = Path(__file__).resolve().parent
TMP_DIR = os.path.join(BASE_DIR, "tmp")

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(str(BASE_DIR), "settings.ini"))

if __name__ == '__main__':
    gif_manager = GifManager(BASE_DIR, TMP_DIR, CONFIG)

    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = ClockWindow(window)
    window.show()

    ui.update_gif(gif_manager.random_idling_gif())

    controller = Controller(gif_manager, ui)

    sys.exit(app.exec_())