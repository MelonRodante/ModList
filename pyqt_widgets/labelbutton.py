import os

import PyQt5
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QLabel


class Mod:
    def __init__(self, q):
        self.name = q.value(1)
        self.category = q.value(2)
        self.loader = q.value(3)
        self.update_date = q.value(4)
        self.path = q.value(5)
        self.installed = q.value(6)
        self.ignored = q.value(7)
        self.updated = q.value(8)
        self.favorite = q.value(9)
        self.blocked = q.value(10)


class ButtonLabel(QLabel):

    def __init__(self, icon, mod):
        QLabel.__init__(self)
        self.mod = mod

        p = QtGui.QPixmap()
        p.loadFromData(icon)

        self.setPixmap(p)
        self.setScaledContents(True)
        self.setStyleSheet('background-color: #00000000;')

        self.setMinimumSize(40, 40)
        self.setMaximumSize(40, 40)

        self.setMouseTracking(True)

    def mouseReleaseEvent(self, ev):
        os.startfile(self.mod.path)





