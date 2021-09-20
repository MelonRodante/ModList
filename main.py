import sys
import time

import qdarkstyle
from PyQt5 import QtWidgets

from main_window import MainWindow
from pyqt_widgets import css

if __name__ == '__main__':

    app = QtWidgets.QApplication([])

    style = qdarkstyle.load_stylesheet_pyqt5()

    # style = style.replace('#1A72BB', '#FF0000')

    epoch_time = 1632062031
    time_formatted = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch_time))

    print(time_formatted)

    main_window = MainWindow()
    app.setStyleSheet(css.style)
    main_window.show()
    sys.exit(app.exec())
