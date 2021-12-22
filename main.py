import sys

from PyQt5 import QtWidgets

from pyqt_style import css
from utils import dbutil
from utils.utils import Utils
from windows.main_window import MainWindow

if __name__ == '__main__':

    app = QtWidgets.QApplication([])
    app.setStyleSheet(css.style)
    main_window = MainWindow()
    sys.exit(app.exec())


'''
    key = '$2a$10$ku3.ncligCgUckN7vKnKyOeqH9y9H/aDca3t.QjPEG./wPaOU7UPu'

    import requests

    headers = {
        'Accept': 'application/json',
        'x-api-key': key
    }

    r = requests.get('https://api.curseforge.com/v1/mods/search', headers=headers)

    print(r.json())
'''