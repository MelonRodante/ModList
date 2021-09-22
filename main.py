import sys

from PyQt5 import QtWidgets
from main_window import MainWindow
from pyqt_style import css

if __name__ == '__main__':

    app = QtWidgets.QApplication([])

    main_window = MainWindow()
    app.setStyleSheet(css.style)
    main_window.show()
    sys.exit(app.exec())
