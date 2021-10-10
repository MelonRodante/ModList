from PyQt5 import QtWidgets, QtSql, QtCore
from PyQt5.QtCore import QSize, Qt

from pyqt_windows.lists_dialog import Ui_AdminListDialog


class AdminListDialog(QtWidgets.QDialog):

    def __init__(self):
        super(AdminListDialog, self).__init__()
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
        self.ui = Ui_AdminListDialog()
        self.ui.setupUi(self)

        self.exitcode = 0
        self.setupWidgets()
        self.setupEvents()
        self.fill_table()
        self.show()

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

    # ------------------------------------------------------------------------------------------------------------------

    def setupEvents(self):
        self.ui.tableLists.itemSelectionChanged.connect(self.clicked_table)
        self.ui.editList.textChanged.connect(self.change_edit_name)
        self.ui.btnAddSave.clicked.connect(self.add_update_list)
        self.ui.btnRemove.clicked.connect(self.remove_list)

    def clicked_table(self):
        try:
            if len(self.ui.tableLists.selectedItems()) > 0:
                fila = self.ui.tableLists.selectedItems()
                self.ui.editList.setText(fila[0].text().strip())
                self.ui.editVersion.setText(fila[1].text().strip())
                self.ui.cmbLoader.setCurrentIndex(self.ui.cmbLoader.findText(fila[2].text().strip()))
        except Exception as e:
            print('ERROR clicked_table:', e)

    def add_update_list(self):
        if self.ui.btnRemove.isEnabled():
            self.update_list()
        else:
            self.add_list()

    def add_list(self):
        try:
            q = QtSql.QSqlQuery()
            q.prepare('INSERT INTO Lists(listname, version, loader)' 'VALUES (:listname, :version, :loader)')
            q.bindValue(':listname', self.ui.editList.text().strip())
            q.bindValue(':version', self.ui.editVersion.text().strip())
            q.bindValue(':loader', self.ui.cmbLoader.currentText())
            if q.exec():
                self.ui.editList.setText('')
                self.ui.editVersion.setText('')
                self.ui.cmbLoader.setCurrentIndex(0)
                self.fill_table()
                self.exitcode = 1
        except Exception as e:
            print('ERROR add_list:', e)

    def update_list(self):
        try:
            q = QtSql.QSqlQuery()
            q.prepare('UPDATE Lists SET version = :version, loader = :loader WHERE listname == :listname;')
            q.bindValue(':listname', self.ui.editList.text())
            q.bindValue(':version', self.ui.editVersion.text())
            q.bindValue(':loader', self.ui.cmbLoader.currentText())
            if q.exec():
                self.ui.editList.setText('')
                self.ui.editVersion.setText('')
                self.ui.cmbLoader.setCurrentIndex(0)
                self.fill_table()
                self.exitcode = 1
        except Exception as e:
            print('ERROR update_list:', e)

    def remove_list(self):
        try:
            q = QtSql.QSqlQuery()
            q.prepare('DELETE FROM Lists WHERE list == :listname;')
            q.bindValue(':listname', self.ui.editList.text())
            if q.exec():
                self.ui.editList.setText('')
                self.ui.editVersion.setText('')
                self.ui.cmbLoader.setCurrentIndex(0)
                self.fill_table()
                self.exitcode = 1
        except Exception as e:
            print('ERROR remove_list:', e)

    def change_edit_name(self):
        try:
            if self.ui.editList.text():
                self.ui.btnAddSave.setEnabled(True)
                self.ui.editVersion.setEnabled(True)
                for i in range(self.ui.tableLists.rowCount()):
                    if self.ui.editList.text().strip() == self.ui.tableLists.item(i, 0).text().strip():
                        self.ui.btnAddSave.setText('Guardar')
                        self.ui.btnRemove.setEnabled(True)
                        self.ui.cmbLoader.setEnabled(self.ui.tableLists.item(i, 2).text().strip() == 'Sin Loader')
                        return

                self.ui.btnAddSave.setText('Añadir')
                self.ui.cmbLoader.setEnabled(True)
                self.ui.btnRemove.setEnabled(False)
            else:
                self.ui.btnAddSave.setText('Añadir')
                self.ui.cmbLoader.setEnabled(False)
                self.ui.btnAddSave.setEnabled(False)
                self.ui.editVersion.setEnabled(False)
                self.ui.btnRemove.setEnabled(False)
        except Exception as e:
            print('ERROR change_edit_name:', e)

    def closeEvent(self, evnt):
        try:
            self.done(self.exitcode)
        except Exception as e:
            print('ERROR closeEvent:', e)

    # ------------------------------------------------------------------------------------------------------------------

    def fill_table(self):
        try:
            q = QtSql.QSqlQuery()
            q.prepare('SELECT listname, version, loader FROM Lists')

            self.ui.tableLists.setRowCount(0)
            if q.exec_():
                while q.next():
                    i = self.ui.tableLists.rowCount()
                    self.ui.tableLists.insertRow(i)
                    self.ui.tableLists.setItem(i, 0, QtWidgets.QTableWidgetItem('  ' + q.value(0)))
                    self.ui.tableLists.setItem(i, 1, QtWidgets.QTableWidgetItem('  ' + q.value(1)))
                    self.ui.tableLists.setItem(i, 2, QtWidgets.QTableWidgetItem('  ' + q.value(2) + '  '))

                    self.ui.tableLists.item(i, 0).setTextAlignment(Qt.AlignCenter)
                    self.ui.tableLists.item(i, 1).setTextAlignment(Qt.AlignCenter)
                    self.ui.tableLists.item(i, 2).setTextAlignment(Qt.AlignCenter)
        except Exception as e:
            print('ERROR fill_table:', e)
