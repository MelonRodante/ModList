import sys

from PyQt5 import QtWidgets
from windows.main_window import MainWindow

if __name__ == '__main__':

    app = QtWidgets.QApplication([])
    main_window = MainWindow()
    sys.exit(app.exec())
