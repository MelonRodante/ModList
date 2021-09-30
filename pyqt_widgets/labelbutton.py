import os

from PyQt5 import QtGui
from PyQt5.QtWidgets import QLabel

base_url = 'https://www.curseforge.com'

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

    def mousePressEvent(self, ev):
        try:
            os.startfile(base_url+self.mod.path)
        except Exception as e:
            print(e)




