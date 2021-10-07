import os

from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon

from icon_utils import IconUtils

base_url = 'https://www.curseforge.com'


class TableItemButton(QtWidgets.QTableWidgetItem):

    def __init__(self, mod):
        try:
            QtWidgets.QTableWidgetItem.__init__(self, IconUtils.getNormalIcon(mod.icon), '')
            self.mod = mod

        except Exception as e:
            print('LabelModName: ', str(e))

    def click(self):
        try:
            os.startfile(base_url+self.mod.path)
        except Exception as e:
            print(e)

    @staticmethod
    def click_icon_table(item):
        if isinstance(item, TableItemButton):
            item.click()


class TableItemName(QtWidgets.QTableWidgetItem):
    def __init__(self, name, font):
        QtWidgets.QTableWidgetItem.__init__(self, name)
        self.setFont(font)


class TableItemCategories(QtWidgets.QTableWidgetItem):
    def __init__(self, categories):
        QtWidgets.QTableWidgetItem.__init__(self)
        self.setIcon(QIcon(IconUtils.getLargeIcon(categories)))


