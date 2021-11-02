import sys

from PyQt5 import QtWidgets

from pyqt_style import css
from utils import dbutil
from windows.main_window import MainWindow

if __name__ == '__main__':

    app = QtWidgets.QApplication([])
    app.setStyleSheet(css.style)
    main_window = MainWindow()
    sys.exit(app.exec())
