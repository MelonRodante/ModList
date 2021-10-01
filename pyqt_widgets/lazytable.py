from PyQt5 import QtGui, QtCore


class LazyTableModel(QtCore.QAbstractTableModel):

    def __init__(self, data, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.numRows = 0
        self.numColumns = 0
        self._data = data

    def rowCount(self, parent):
        return self.numRows

    def columnCount(self, parent):
        return self.numColumns

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return QtCore.QVariant()

        if index.row() >= self.numRows or index.row() < 0 or index.column() >= self.numColumns or index.column() < 0:
            return QtCore.QVariant()

        if role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(self._data[index.row(), index.column()])
        elif role == QtCore.Qt.BackgroundRole:
            return QtCore.QVariant(QtGui.qApp.palette().base())

        return QtCore.QVariant()

    # data

    def canFetchMore(self, index):
        if self.numRows < self._data.shape[0] or self.numColumns < self._data.shape[1]:
            return True
        else:
            return False

    def fetchMore(self, index):
        """
        Index=QModelIndex
        """
        maxFetch = 10  # maximum number of rows/columns to grab at a time.

        remainderRows = self._data.shape[0] - self.numRows
        rowsToFetch = min(maxFetch, remainderRows)

        if rowsToFetch > 0:
            self.beginInsertRows(QtCore.QModelIndex(), self.numRows, self.numRows + rowsToFetch - 1)
            self.endInsertRows()
            self.numRows += rowsToFetch

        remainderColumns = self._data.shape[1] - self.numColumns
        columnsToFetch = min(maxFetch, remainderColumns)
        if columnsToFetch > 0:
            self.beginInsertColumns(QtCore.QModelIndex(), self.numColumns, self.numColumns + columnsToFetch - 1)
            self.endInsertColumns()
            self.numColumns += columnsToFetch

        self.emit(QtCore.SIGNAL("numberPopulated"), rowsToFetch, columnsToFetch)
