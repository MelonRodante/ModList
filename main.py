import sys

import qdarkstyle
from darktheme.widget_template import DarkPalette

from PyQt5 import QtWidgets

from main_window import MainWindow

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    #app.setPalette(DarkPalette())
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
