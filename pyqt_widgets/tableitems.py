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
        self.setIcon(QIcon(self.get_large_icon(categories)))

    @staticmethod
    def get_large_icon(categories, center=False):
        if center:
            icon = categories_icons.get('|center|'+categories)
        else:
            icon = categories_icons.get(categories)

        if not isinstance(icon, QPixmap):
            pm = QPixmap(':/categories/categories/empty.png')
            painter = QPainter(pm)
            if categories != 'without-category':
                cat = categories.split(',')
                start = 0
                if center:
                    start = ((5 - len(cat)) * 29)/2

                for i, c in enumerate(cat):
                    px = QPixmap(':/categories/categories/' + c + '.png')
                    painter.drawPixmap(
                        QRectF(start + (i*(px.rect().width()+5)), 0, 24, 24),
                        px,
                        QRectF(px.rect()))
            else:
                px = QPixmap(':/categories/categories/' + categories + '.png')
                painter.drawPixmap(QRectF(pm.width()/2 - px.width()/2, 0, 24, 24), px, QRectF(px.rect()))
            categories_icons[categories] = pm
            return pm
        else:
            return icon
