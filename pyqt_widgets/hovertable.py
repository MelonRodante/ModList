'''class HoverTable(QTableWidget):
    cellExited = QtCore.pyqtSignal(int, int)
    itemExited = QtCore.pyqtSignal(QTableWidgetItem)

    def __init__(self, rows, columns, parent=None):
        QTableWidget.__init__(self, rows, columns, parent)
        self._last_index = QtCore.QPersistentModelIndex()
        self.viewport().installEventFilter(self)

    def eventFilter(self, widget, event):
        if widget is self.viewport():
            index = self._last_index
            if event.type() == QtCore.QEvent.MouseMove:
                index = self.indexAt(event.pos())
            elif event.type() == QtCore.QEvent.Leave:
                index = QtCore.QModelIndex()
            if index != self._last_index:
                row = self._last_index.row()
                column = self._last_index.column()
                item = self.item(row, column)
                if item is not None:
                    self.itemExited.emit(item)
                self.cellExited.emit(row, column)
                self._last_index = QtCore.QPersistentModelIndex(index)
        return QTableWidget.eventFilter(self, widget, event)


class Window(QWidget):
    def __init__(self, rows, columns):
        QWidget.__init__(self)
        self.table = TableWidget(rows, columns, self)
        for column in range(columns):
            for row in range(rows):
                item = QTableWidgetItem('Text%d' % row)
                self.table.setItem(row, column, item)
        layout = QVBoxLayout(self)
        layout.addWidget(self.table)
        self.table.setMouseTracking(True)
        self.table.itemEntered.connect(self.handleItemEntered)
        self.table.itemExited.connect(self.handleItemExited)

    def handleItemEntered(self, item):
        row = item.row()
        for i in range(self.table.columnCount()):
            self.table.item(row, i).setBackground(QtGui.QColor('moccasin'))

    def handleItemExited(self, item):
        row = item.row()
        for i in range(self.table.columnCount()):
            self.table.item(row, i).setBackground(QTableWidgetItem().background())'''