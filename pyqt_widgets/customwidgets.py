from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QPushButton, QStyledItemDelegate, QTableWidgetItem, QStyle, QTableWidget
from qtpy.QtWidgets import QStyleOptionViewItem


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


class CustomButton(QPushButton):
    def __init__(self, mod):
        QPushButton.__init__(self)
        self.mod = mod


class TableStyleItemDelegate(QStyledItemDelegate):

    def __init__(self, table: QTableWidget):
        super().__init__(table)
        self.table = table
        self.row = -1

        self.table.setMouseTracking(True)
        self.table.cellEntered.connect(self.cellEntered)
        self.table.itemEntered.connect(self.itemEntered)

    def cellEntered(self, row, column):
        self.row = row
        self.table.viewport().update()

    def itemEntered(self, item):
        self.row = item.row()
        self.table.viewport().update()

    def paint(self, painter: QtGui.QPainter, option: QStyleOptionViewItem, index: QtCore.QModelIndex) -> None:
        try:
            if index.row() == self.row:
                option.state |= QStyle.State_MouseOver

            super(TableStyleItemDelegate, self).paint(painter, option, index)
        except Exception as e:
            print(e)