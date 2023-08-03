import os

from PyQt5 import QtWidgets
from PyQt5.QtGui import QColor

from utils.icon_utils import IconUtils
from utils.mod import Mod
from utils.utils import Utils


class TableItemButton(QtWidgets.QTableWidgetItem):

    def __init__(self, mod):
        try:
            QtWidgets.QTableWidgetItem.__init__(self, IconUtils.getNormalIcon(mod.icon), '')
            self.mod = mod
            self.setToolTip('<b style="font-size:14px;">ID:</b> ' + str(mod.projectid) + '<br/><b style="font-size:14px;">DESCRIPTION:</b><br/>' + mod.description)

        except Exception as e:
            Utils.print_exception('TABLE_ITEM_BUTTON init', e)


    def click(self):
        try:
            os.startfile(self.mod.path)

        except Exception as e:
            Utils.print_exception('TABLE_ITEM_BUTTON click', e)

    @staticmethod
    def click_icon_table(item):
        try:
            if isinstance(item, TableItemButton):
                item.click()

        except Exception as e:
            Utils.print_exception('TABLE_ITEM_BUTTON click_icon_table', e)


class TableItemName(QtWidgets.QTableWidgetItem):
    def __init__(self, mod, font):
        try:
            QtWidgets.QTableWidgetItem.__init__(self, mod.name)
            self.setFont(font)

            if mod.autoinstall:
                self.setForeground(QColor('#85C4E3'))
            elif mod.autoignore:
                self.setForeground(QColor('#9B5D62'))

        except Exception as e:
            Utils.print_exception('TABLE_ITEM_NAME init', e)


class TableItemCategories(QtWidgets.QTableWidgetItem):
    def __init__(self, categories):
        try:
            QtWidgets.QTableWidgetItem.__init__(self, IconUtils.getLargeIcon(categories), '')

            cat_tooltip = ''
            for cat in categories.split(','):
                cat_tooltip += ' - ' + Mod.categories.get(cat).get('cat_name') + '\n'
            self.setToolTip(cat_tooltip[:-1])

        except Exception as e:
            Utils.print_exception('TABLE_ITEM_CATEGORIES init', e)


