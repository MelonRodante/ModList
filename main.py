import sys

from PyQt5 import QtWidgets

from backup import cleardb
from pyqt_style import css
from windows.main_window import MainWindow

if __name__ == '__main__':

    cleardb.clear_cat_db()


    '''app = QtWidgets.QApplication([])
    app.setStyleSheet(css.style)
    main_window = MainWindow()
    sys.exit(app.exec())'''
