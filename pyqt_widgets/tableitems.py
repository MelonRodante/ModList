import os

from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon

base_url = 'https://www.curseforge.com'

class TableItemName(QtWidgets.QTableWidgetItem):
    def __init__(self, name, font):
        QtWidgets.QTableWidgetItem.__init__(self, name)
        self.setFont(font)


class TableItemButton(QtWidgets.QTableWidgetItem):

    def __init__(self, mod):
        try:
            QtWidgets.QTableWidgetItem.__init__(self, QIcon(mod.icon), '')
            self.mod = mod

        except Exception as e:
            print('LabelModName: ', str(e))

    def click(self):
        try:
            os.startfile(base_url+self.mod.path)
        except Exception as e:
            print(e)

