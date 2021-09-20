from PyQt5 import QtWidgets, QtSql, QtCore
from PyQt5.QtCore import QSize

from database import Database
from pyqt_windows.lists_dialog import Ui_AdminLists
from pyqt_windows.searching_dialog import Ui_SearchingDialog


class ListDialog(QtWidgets.QDialog):

    def __init__(self):
        super(ListDialog, self).__init__()
        self.ui = Ui_AdminLists()
        self.ui.setupUi(self)

        self.setupWidgets()
        self.setupEvents()

        self.fill_table()

    # ------------------------------------------------------------------------------------------------------------------

    def setupWidgets(self):
        self.modify_cmb()
        self.modify_table()
        self.modify_css()

    def modify_cmb(self):
        model = self.ui.cmbLoader.model()
        for i in range(model.rowCount()):
            model.setData(model.index(i, 0), QSize(0, 20), QtCore.Qt.SizeHintRole)

    def modify_table(self):
        header = self.ui.tableLists.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)

    def modify_css(self):
        f = self.ui.tableLists.horizontalHeader().font()
        f.setBold(True)
        self.ui.tableLists.horizontalHeader().setFont(f)

        self.ui.btnAddSave.setStyleSheet('QPushButton {border: 1px solid #F0651F; background-color: #0F1A25;} '
                                         'QPushButton:hover {background-color: #19232D;}'
                                         'QPushButton:pressed {background-color: #54687A;}'
                                         'QPushButton:disabled {border: 1px solid #000000;}')

        self.ui.btnRemove.setStyleSheet('QPushButton {border: 1px solid #F0651F; background-color: #0F1A25;} '
                                        'QPushButton:hover {background-color: #19232D;}'
                                        'QPushButton:pressed {background-color: #54687A;}'
                                        'QPushButton:disabled {border: 1px solid #000000;}')

        self.ui.btnSearchNewMods.setStyleSheet('QPushButton {border: 1px solid #F0651F; background-color: #0F1A25;} '
                                               'QPushButton:hover {background-color: #19232D;}'
                                               'QPushButton:pressed {background-color: #54687A;}'
                                               'QPushButton:disabled {border: 1px solid #000000;}')

        self.ui.spinPages.setStyleSheet('QSpinBox {border: 1px solid #F0651F; background-color: #0F1A25;} '
                                        'QSpinBox:hover {background-color: #19232D;}'
                                        'QSpinBox:pressed {background-color: #19232D;}'
                                        'QSpinBox:disabled {border: 1px solid #000000;}')

    # ------------------------------------------------------------------------------------------------------------------

    def setupEvents(self):
        self.ui.tableLists.itemSelectionChanged.connect(self.clicked_table)
        self.ui.editList.textChanged.connect(self.change_edit_name)
        self.ui.btnAddSave.clicked.connect(self.add_update_list)
        self.ui.btnRemove.clicked.connect(self.remove_list)

    def clicked_table(self):
        if self.ui.tableLists.hasFocus():
            fila = self.ui.tableLists.selectedItems()
            self.ui.editList.setText(fila[0].text().strip())
            self.ui.editSearch.setText(fila[1].text().strip())
            self.ui.cmbLoader.setCurrentIndex(self.ui.cmbLoader.findText(fila[2].text().strip()))

    def add_update_list(self):
        if self.ui.btnRemove.isEnabled():
            self.update_list()
        else:
            self.add_list()

    def add_list(self):
        pass

    def update_list(self):
        pass

    def remove_list(self):
        q = QtSql.QSqlQuery()
        q.prepare('DELETE FROM Lists WHERE list == :list;')
        q.bindValue(':list', self.ui.editList.text())
        q.exec()
        self.ui.editList.setText('')
        self.ui.editSearch.setText('')
        self.ui.cmbLoader.setCurrentIndex(0)
        self.fill_table()

    def change_edit_name(self):
        for i in range(self.ui.tableLists.rowCount()):
            if self.ui.editList.text() == self.ui.tableLists.item(i, 0).text().strip():
                self.ui.btnAddSave.setText('Guardar')
                self.ui.btnRemove.setEnabled(True)
                self.ui.btnSearchNewMods.setEnabled(True)
                self.ui.spinPages.setEnabled(True)
                return

        self.ui.btnAddSave.setText('Añadir')
        self.ui.btnRemove.setEnabled(False)
        self.ui.btnSearchNewMods.setEnabled(False)
        self.ui.spinPages.setEnabled(False)
        self.ui.spinPages.setValue(0)

    # ------------------------------------------------------------------------------------------------------------------

    def fill_table(self):
        q = QtSql.QSqlQuery()
        q.prepare('SELECT list, search, loader FROM Lists')

        self.ui.tableLists.setRowCount(0)
        if q.exec_():
            while q.next():
                i = self.ui.tableLists.rowCount()
                self.ui.tableLists.insertRow(i)
                self.ui.tableLists.setItem(i, 0, QtWidgets.QTableWidgetItem('  ' + q.value(0)))
                self.ui.tableLists.setItem(i, 1, QtWidgets.QTableWidgetItem('  ' + q.value(1)))
                self.ui.tableLists.setItem(i, 2, QtWidgets.QTableWidgetItem('  ' + q.value(2) + '  '))


class SearchingDialog(QtWidgets.QDialog):

    def __init__(self):
        super(SearchingDialog, self).__init__()
        self.ui = Ui_SearchingDialog()
        self.ui.setupUi(self)
