import os

from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon, QColor

from utils.icon_utils import IconUtils
from utils.mod import Mod


class TableItemButton(QtWidgets.QTableWidgetItem):

    def __init__(self, mod):
        try:
            QtWidgets.QTableWidgetItem.__init__(self, IconUtils.getNormalIcon(mod.icon), '')
            self.mod = mod

        except Exception as e:
            print('LabelModName: ', str(e))

    def click(self):
        try:
            os.startfile(self.mod.path)
        except Exception as e:
            print(e)

    @staticmethod
    def click_icon_table(item):
        if isinstance(item, TableItemButton):
            item.click()


class TableItemName(QtWidgets.QTableWidgetItem):
    def __init__(self, mod, font):
        QtWidgets.QTableWidgetItem.__init__(self, mod.name)
        self.setFont(font)

        if mod.autoinstall:
            self.setForeground(QColor('#85C4E3'))
        elif mod.autoignore:
            self.setForeground(QColor('#9B5D62'))


class TableItemCategories(QtWidgets.QTableWidgetItem):
    def __init__(self, categories):
        QtWidgets.QTableWidgetItem.__init__(self)
        self.setIcon(QIcon(IconUtils.getLargeIcon(categories)))

        cat_tooltip = ''
        for cat in categories.split(','):
            cat_tooltip += ' - ' + Mod.categories.get(cat).get('cat_name') + '\n'
        self.setToolTip(cat_tooltip[:-1])


