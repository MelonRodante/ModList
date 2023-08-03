import json
import re

import requests
from PyQt5 import QtWidgets, QtSql, QtCore
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QMessageBox

from pyqt_windows.lists_dialog import Ui_AdminListDialog
from utils import curseapilinks
from utils.curseapilinks import CurseAPI
from distutils.version import StrictVersion

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
        try:
            self.create_cmb_versions()
            self.modify_cmb()
            self.modify_table()
            self.modify_css()
        except Exception as e:
            print('ADMIN_LIST_DIALOG setupWidgets', e)

    def create_cmb_versions(self):
        try:
            try:
                #versions = requests.get(CurseAPI.minecraft_versions, headers=CurseAPI.header).json()
                #for version in versions:
                #    if version.get('versionString') is not None:
                #        self.ui.cmbVersion.addItem(version.get('versionString'))

                versions = requests.get(CurseAPI.minecraft_versions, headers=CurseAPI.header).json()
                versions_strings = []
                for version in versions['data']:
                    if version.get('name') is not None:
                        versions_strings.append(version.get('name'))
                versions_strings.sort(key=StrictVersion, reverse=True)
                self.ui.cmbVersion.addItems(versions_strings)

            except json.decoder.JSONDecodeError:
                QMessageBox.critical(None, 'API ERROR:', 'API ERROR:\n\nLa consulta a la API no ha regresado ningun valor.', QtWidgets.QMessageBox.Close)
                self.done(0)
        except Exception as e:
            print('ADMIN_LIST_DIALOG create_cmb_versions', e)

    def modify_cmb(self):
        try:
            model = self.ui.cmbLoader.model()
            for i in range(model.rowCount()):
                model.setData(model.index(i, 0), QSize(0, 20), Qt.SizeHintRole)

            model = self.ui.cmbVersion.model()
            for i in range(model.rowCount()):
                model.setData(model.index(i, 0), QSize(0, 20), Qt.SizeHintRole)

            self.ui.cmbVersion.setCurrentIndex(-1)
            self.ui.cmbLoader.setCurrentIndex(-1)
        except Exception as e:
            print('ADMIN_LIST_DIALOG modify_cmb', e)

    def modify_table(self):
        try:
            header = self.ui.tableLists.horizontalHeader()
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        except Exception as e:
            print('ADMIN_LIST_DIALOG modify_table', e)

    def modify_css(self):
        try:
            f = self.ui.tableLists.horizontalHeader().font()
            f.setBold(True)
            self.ui.tableLists.horizontalHeader().setFont(f)
        except Exception as e:
            print('ADMIN_LIST_DIALOG modify_css', e)

    # ------------------------------------------------------------------------------------------------------------------

    def setupEvents(self):
        try:
            self.ui.tableLists.itemSelectionChanged.connect(self.clicked_table)
            self.ui.editList.textChanged.connect(self.change_edits)
            self.ui.cmbVersion.currentIndexChanged.connect(self.change_edits)
            self.ui.cmbLoader.currentIndexChanged.connect(self.change_edits)
            self.ui.btnAddSave.clicked.connect(self.add_update_list)
            self.ui.btnRemove.clicked.connect(self.remove_list)

            self.ui.editList.editingFinished.connect(lambda: self.ui.editList.setText(" ".join(self.ui.editList.text().strip().split())))
        except Exception as e:
            print('ADMIN_LIST_DIALOG setupEvents', e)

    def clicked_table(self):
        try:
            if len(self.ui.tableLists.selectedItems()) > 0:
                fila = self.ui.tableLists.selectedItems()
                self.ui.editList.setText(fila[0].text().strip())
                self.ui.cmbVersion.setCurrentIndex(self.ui.cmbVersion.findText(fila[1].text().strip()))
                self.ui.cmbLoader.setCurrentIndex(self.ui.cmbLoader.findText(fila[2].text().strip()))
        except Exception as e:
            print('ADMIN_LIST_DIALOG clicked_table', e)

    def add_update_list(self):
        try:
            if self.ui.btnRemove.isEnabled():
                self.update_list()
            else:
                self.add_list()
        except Exception as e:
            print('ADMIN_LIST_DIALOG add_update_list', e)

    def add_list(self):
        try:
            q = QtSql.QSqlQuery()
            q.prepare('INSERT INTO Lists(listname, version, loader)' 'VALUES (:listname, :version, :loader)')
            q.bindValue(':listname', " ".join(self.ui.editList.text().strip().split()))
            q.bindValue(':version', self.ui.cmbVersion.currentText().strip())
            q.bindValue(':loader', self.ui.cmbLoader.currentText())
            if q.exec():
                self.ui.editList.setText('')
                self.ui.cmbVersion.setCurrentIndex(-1)
                self.ui.cmbLoader.setCurrentIndex(-1)
                self.fill_table()
                self.exitcode = 1
        except Exception as e:
            print('ADMIN_LIST_DIALOG add_list', e)

    def remove_list(self):
        try:
            q = QtSql.QSqlQuery()
            q.prepare('DELETE FROM Lists WHERE listname == :listname;')
            q.bindValue(':listname', self.ui.editList.text())
            if q.exec():
                self.ui.editList.setText('')
                self.ui.cmbVersion.setCurrentIndex(-1)
                self.ui.cmbLoader.setCurrentIndex(-1)
                self.fill_table()
                self.exitcode = 1
        except Exception as e:
            print('ADMIN_LIST_DIALOG remove_list', e)

    def change_edits(self):
        try:
            if self.ui.editList.text() and not self.ui.editList.text().isspace():
                find = False
                name = " ".join(self.ui.editList.text().strip().split())

                for i in range(self.ui.tableLists.rowCount()):
                    if name == self.ui.tableLists.item(i, 0).text().strip():
                        find = True
                        break

                self.ui.cmbVersion.setDisabled(find)
                self.ui.cmbLoader.setDisabled(find)
                self.ui.btnRemove.setEnabled(find)

                self.ui.btnAddSave.setEnabled(not find and self.ui.cmbVersion.currentText() != '' and self.ui.cmbLoader.currentText() != '')

            else:
                self.ui.cmbVersion.setEnabled(False)
                self.ui.cmbLoader.setEnabled(False)
                self.ui.btnAddSave.setEnabled(False)
                self.ui.btnRemove.setEnabled(False)

                self.ui.cmbVersion.setCurrentIndex(-1)
                self.ui.cmbLoader.setCurrentIndex(-1)
        except Exception as e:
            print('ADMIN_LIST_DIALOG change_edits', e)

    def closeEvent(self, evnt):
        try:
            self.done(self.exitcode)
        except Exception as e:
            print('ADMIN_LIST_DIALOG closeEvent', e)

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
                    self.ui.tableLists.setItem(i, 1, QtWidgets.QTableWidgetItem('  ' + q.value(1) + '  '))
                    self.ui.tableLists.setItem(i, 2, QtWidgets.QTableWidgetItem('  ' + q.value(2) + '  '))

                    self.ui.tableLists.item(i, 0).setTextAlignment(Qt.AlignCenter)
                    self.ui.tableLists.item(i, 1).setTextAlignment(Qt.AlignCenter)
                    self.ui.tableLists.item(i, 2).setTextAlignment(Qt.AlignCenter)
        except Exception as e:
            print('ADMIN_LIST_DIALOG fill_table', e)
