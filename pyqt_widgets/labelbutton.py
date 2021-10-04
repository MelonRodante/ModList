import os

from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel

base_url = 'https://www.curseforge.com'


class LabelButton(QLabel):

    def __init__(self, mod):
        try:
            QLabel.__init__(self)
            self.mod = mod

            self.setPixmap(mod.icon)
            self.setScaledContents(True)
            self.setStyleSheet('background-color: #00000000;')

            self.setMinimumSize(40, 40)
            self.setMaximumSize(40, 40)

            self.setMouseTracking(True)
        except Exception as e:
            print('LabelModName: ', str(e))

    def mousePressEvent(self, ev):
        try:
            os.startfile(base_url+self.mod.path)
        except Exception as e:
            print(e)





