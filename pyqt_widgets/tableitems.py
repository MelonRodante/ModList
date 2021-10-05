import os

from PyQt5 import QtWidgets
from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QIcon, QPixmap, QPainter

base_url = 'https://www.curseforge.com'
categories_icons = {}


class TableItemButton(QtWidgets.QTableWidgetItem):

    def __init__(self, mod):
        try:
            QtWidgets.QTableWidgetItem.__init__(self, QIcon(mod.icon), '')
            self.mod = mod
            #self.setBackground(QColor('#FF0000'))

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
        # self.setIcon(QIcon(':/categories/categories/library-api.png'))
        self.setIcon(QIcon(self.get_large_icon(categories)))

    def get_large_icon(self, categories):
        icon = categories_icons.get(categories)
        if not isinstance(icon, QPixmap):
            pm = QPixmap(':/categories/categories/empty.png')
            if categories != 'without-category':
                cat = categories.split(',')
                painter = QPainter(pm)
                # start = ((5 - len(cat)) * 29)/2
                for i, c in enumerate(cat):
                    px = QPixmap(':/categories/categories/' + c + '.png')
                    painter.drawPixmap(
                        QRectF(i*(px.rect().width()+5), 0, 24, 24),
                        px,
                        QRectF(px.rect()))
            categories_icons[categories] = pm
            return pm
        else:
            return icon
