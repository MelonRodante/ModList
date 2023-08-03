import sys

from PyQt5 import QtWidgets

from pyqt_style import css
from utils import dbutil
from utils.utils import Utils
from windows.main_window import MainWindow

if __name__ == '__main__':

    #'''
    app = QtWidgets.QApplication([])
    app.setStyleSheet(css.style)
    main_window = MainWindow()
    sys.exit(app.exec())
    #'''

    #dbutil.resize_icons()

'''
    key = '$2a$10$ku3.ncligCgUckN7vKnKyOeqH9y9H/aDca3t.QjPEG./wPaOU7UPu'

    import requests
    from distutils.version import StrictVersion

    headers = {
        'Accept': 'application/json',
        'x-api-key': key
    }

    r = requests.get('https://www.modpackindex.com/api/v1/minecraft/versions', headers=headers)

    dictionary = r.json()['data']

    a = []
    for version in dictionary:
        a.append(version['name'])
    a.sort(key=StrictVersion, reverse=True)

    for i in a:
        print(i)
#'''