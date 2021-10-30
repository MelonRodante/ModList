from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QStyledItemDelegate, QStyle, QTableWidget, QStyleOptionViewItem


class TableStyleItemDelegate(QStyledItemDelegate):

    def __init__(self, table: QTableWidget):
        super().__init__(table)
        self.table = table
        self.row = -1

        self.table.setMouseTracking(True)
        self.table.cellEntered.connect(self.cellEntered)
        self.table.itemEntered.connect(self.itemEntered)

    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        if index.column() == 0:
            option.decorationSize = QSize(48, 48)
        elif index.column() == 2:
            option.decorationSize = QSize(180, 48)
        elif index.column() == 5:
            option.decorationSize = QSize(16, 16)

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