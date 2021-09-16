import sys

import qdarkstyle
from PyQt5 import QtWidgets

from main_window import MainWindow

if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    style = qdarkstyle.load_stylesheet_pyqt5()

    # style = style.replace('#1A72BB', '#FF0000')

    main_window = MainWindow()
    app.setStyleSheet(style)
    main_window.show()
    sys.exit(app.exec())
