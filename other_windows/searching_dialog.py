import sys
from time import sleep

import requests
from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize, Qt, QThread, pyqtSignal, QByteArray
from qtpy import QtSql

from database import Database
from pyqt_windows.searching_dialog import Ui_SearchingDialog


class ModIndex:
    def __init__(self, path, name, update_date, icon):
        self.path = path
        self.name = name
        self.update_date = update_date
        self.icon = icon

        self.error = 0
        self.newmod = 0
        self.update = 0
        self.addlist = 0

    def print(self):
        print('error:', self.error, '| newmod:', self.newmod, '| update:', self.update, '| addlist:', self.addlist)


class SearchThread(QThread):
    sig_max_pages = pyqtSignal(int)
    sig_page_finish = pyqtSignal(int)

    def __init__(self, modlist, max_pages):
        super(SearchThread, self).__init__()
        self.modlist = modlist
        self.max_pages = 10
        self.canclose = 0

    def run(self):
        try:
            db = Database.get_thread_sqlquery()
            self.task(db)
        except Exception as e:
            print('SEARCHING_DIALOG run:', e)

    def task(self, db):
        path = '/minecraft/mc-mods/natures-compass'
        name = 'Nature\'s Compass'
        date = 162753154311
        icon = 'https://media.forgecdn.net/avatars/thumbnails/54/102/64/64/636131217371752080.png'

        mod = ModIndex(path, name, date, icon)
        self.check_mod(db, mod)
        mod.print()
        self.process_mod(db, mod)

    def check_mod(self, db, mod):
        q = QtSql.QSqlQuery(db)
        q.prepare('SELECT update_date, blocked FROM Mods WHERE path == :path')
        q.bindValue(':path', mod.path)
        q.exec()

        if q.exec():

            if q.next():

                if q.value(0) != mod.update_date:
                    mod.update = 1

                if q.value(1) == 0:
                    q.prepare('SELECT 1 FROM ModsLists WHERE list == :list and mod == :mod')
                    q.bindValue(':list', self.modlist)
                    q.bindValue(':mod', mod.path)
                    if q.exec():
                        if not q.next():
                            mod.addlist = 1
                    else:
                        mod.error = 2

            else:
                mod.newmod = 1
                mod.addlist = 1

        else:
            mod.error = 1

    def process_mod(self, db, mod):
        if mod.error != 1:
            db.transaction()
            q = QtSql.QSqlQuery(db)

            if mod.newmod:
                q.prepare('INSERT INTO Mods(path, name, update_date, icon) VALUES (:path, :name, :update_date, :icon)')
                q.bindValue(':path', mod.path)
                q.bindValue(':name', mod.name)
                q.bindValue(':update_date', mod.update_date)
                q.bindValue(':icon', QByteArray(requests.get(mod.icon).content))
                q.exec()
                print('newmod')

            if mod.update:
                q.prepare('UPDATE ModsLists SET updated = 1 WHERE mod == :mod;')
                q.bindValue(':mod', mod.path)
                q.exec()
                print('update')

            if mod.addlist:
                q.prepare('INSERT INTO ModsLists(list, mod)' 'VALUES (:list, :mod)')
                q.bindValue(':list', self.modlist)
                q.bindValue(':mod', mod.path)
                q.exec()
                print('addlist')

            db.commit()


class SearchingDialog(QtWidgets.QDialog):

    def __init__(self):
        super(SearchingDialog, self).__init__()
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
        self.ui = Ui_SearchingDialog()
        self.ui.setupUi(self)

        self.thread = None
        self.worker = None

        self.setupWidgets()
        self.setupEvents()
        self.show()

        self.ui.cmbModList.setCurrentIndex(2)
        self.ui.btnSearchNewMods.setEnabled(True)

    def setupWidgets(self):
        try:
            self.modify_css()
            self.create_cmb_values_lists()
        except Exception as e:
            print('SEARCHING_DIALOG modify_css:', e)

    def modify_css(self):
        try:
            self.ui.btnSearchNewMods.setStyleSheet(
                'QPushButton {border: 1px solid #F0651F; background-color: #0F1A25;} '
                'QPushButton:hover {background-color: #19232D;}'
                'QPushButton:pressed {background-color: #54687A;}'
                'QPushButton:disabled {border: 1px solid #000000;}')
        except Exception as e:
            print('SEARCHING_DIALOG modify_css:', e)

    def create_cmb_values_lists(self):
        try:
            q = QtSql.QSqlQuery()
            q.prepare('select list from Lists')

            self.ui.cmbModList.clear()

            self.ui.cmbModList.addItem('')
            self.ui.cmbModList.insertSeparator(self.ui.cmbModList.count())

            if q.exec_():
                while q.next():
                    self.ui.cmbModList.addItem(q.value(0))

                model = self.ui.cmbModList.model()
                for i in range(model.rowCount()):
                    model.setData(model.index(i, 0), QSize(0, 20), Qt.SizeHintRole)
        except Exception as e:
            print('SEARCHING_DIALOG create_cmb_values_lists:', e)

    def setupEvents(self):
        try:
            self.ui.cmbModList.currentIndexChanged.connect(self.change_cmb_modlist)
            self.ui.btnSearchNewMods.clicked.connect(self.search_mods)
        except Exception as e:
            print('SEARCHING_DIALOG setupEvents:', e)

    def change_cmb_modlist(self):
        try:
            self.ui.btnSearchNewMods.setEnabled(self.ui.cmbModList.currentIndex() > 1)
        except Exception as e:
            print('SEARCHING_DIALOG change_cmb_modlist:', e)

    def search_mods(self):
        try:
            self.ui.cmbModList.setEnabled(False)
            self.ui.spinPages.setEnabled(False)
            self.ui.btnSearchNewMods.setEnabled(False)

            self.search_thread = SearchThread(self.ui.cmbModList.currentText().strip(), self.ui.spinPages.value())

            self.search_thread.sig_max_pages.connect(self.set_max_pages)
            self.search_thread.sig_page_finish.connect(self.set_page_finish)
            self.search_thread.finished.connect(self.set_finish_search)

            self.search_thread.start()
        except Exception as e:
            print('SEARCHING_DIALOG search_mods:', e)

    def set_max_pages(self, max_pages):
        try:
            self.ui.progressBar.setMaximum(max_pages)
        except Exception as e:
            print('SEARCHING_DIALOG set_max_pages:', e)

    def set_page_finish(self, page_finish):
        try:
            self.ui.progressBar.setValue(page_finish)
        except Exception as e:
            print('SEARCHING_DIALOG set_page_finish:', e)

    def set_finish_search(self):
        try:
            self.ui.progressBar.setValue(self.ui.progressBar.maximum())
            sleep(1)
            self.done(0)
        except Exception as e:
            print('SEARCHING_DIALOG set_finish_search:', e)

    def closeEvent(self, event):
        try:
            if self.worker is not None:
                self.worker.canclose = 1
                self.ui.progressBar.setFormat('Cancelando...')
                event.ignore()
        except Exception as e:
            print('SEARCHING_DIALOG closeEvent:', e)
