import os

from PyQt5 import QtGui
from PyQt5.QtWidgets import QLabel


class ButtonLabel(QLabel):

    def __init__(self, mod):
        QLabel.__init__(self)
        self.mod = mod

        self.setPixmap(mod.icon)
        self.setScaledContents(True)
        self.setStyleSheet('background-color: #00000000;')

        self.setMinimumSize(40, 40)
        self.setMaximumSize(40, 40)

        self.setMouseTracking(True)

    def mouseReleaseEvent(self, ev):
        os.startfile(self.mod.path)





