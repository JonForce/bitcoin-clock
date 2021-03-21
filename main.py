import configparser
from pathlib import Path
import os

if __name__ == '__main__':
    config = configparser.ConfigParser()
    BASE_DIR = Path(__file__).resolve().parent.parent
    config.read(os.path.join(str(BASE_DIR), "settings.ini"))
