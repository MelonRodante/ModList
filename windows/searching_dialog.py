import sys
import time
from time import sleep

import cloudscraper
import requests
from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize, Qt, QThread, pyqtSignal, QByteArray
from PyQt5.QtWidgets import QMessageBox
from bs4 import BeautifulSoup
from cloudscraper import CloudflareChallengeError
from qtpy import QtSql

from database import Database
from pyqt_windows.searching_dialog import Ui_SearchingDialog


class ModIndex:
    def __init__(self, path, name, update_date, icon):
        self.path = path
        self.name = name
        self.update_date = int(update_date)
        self.icon = icon

        self.error = 0
        self.newmod = 0
        self.update = 0
        self.addlist = 0
        self.ignore = 0

    def print(self):
        print('error:', self.error, '| newmod:', self.newmod, '| update:', self.update, '| addlist:', self.addlist, '| ignore:', self.ignore)


class SearchThread(QThread):

    url = 'https://www.curseforge.com'
    search_url = url + '/minecraft/mc-mods'
    posfix_url = '&filter-sort=2&page='

    sig_max_pages = pyqtSignal(int)
    sig_page_finish = pyqtSignal(int)
    sig_finish_code = pyqtSignal(int)

    def __init__(self, modlist, max_pages):
        super(SearchThread, self).__init__()
        self.modlist = modlist
        self.filter = ''
        self.max_pages = max_pages
        self.canclose = False

    def run(self):
        try:
            db = Database.get_thread_sqlquery()
            self.set_filter(db)
            scraper = self.get_scrapper()
            self.sig_page_finish.emit(0)
            for i in range(1, self.max_pages+1):
                if self.canclose:
                    self.sig_finish_code.emit(1)
                    break
                self.task(db, i, scraper)
                self.sig_page_finish.emit(i)
            self.sig_finish_code.emit(0)
        except Exception as e:
            print('SEARCHING_DIALOG run:', e)

    def set_filter(self, db):
        try:
            q = QtSql.QSqlQuery(db)
            q.prepare('SELECT filter FROM Lists WHERE list == :list')
            q.bindValue(':list', self.modlist)
            if q.exec():
                if q.next():
                    self.filter = q.value(0)
                else:
                    QMessageBox.critical(None, "Searching DB Error:", 'No hay una lista seleccionada', QtWidgets.QMessageBox.Close)
                    sys.exit(1)
            else:
                QMessageBox.critical(None, "Searching DB Error:", q.lastError().databaseText(), QtWidgets.QMessageBox.Close)
                sys.exit(1)
        except Exception as e:
            print('SEARCHING_DIALOG set_filter:', e)

    def get_scrapper(self):
        try:
            maxpages = ''
            scraper = None
            while not maxpages:
                try:
                    time.sleep(1)
                    scraper = cloudscraper.create_scraper(delay=1)

                    soup = BeautifulSoup(scraper.get(SearchThread.search_url + self.filter + SearchThread.posfix_url + '1').text, 'html.parser')
                    maxpages = soup.find_all('a', class_="pagination-item").pop().find('span').text
                except CloudflareChallengeError as e:
                    print('SEARCHING_DIALOG CloudflareChallengeError')

            if self.max_pages == 0:
                self.max_pages = int(maxpages)
            self.sig_max_pages.emit(self.max_pages)

            return scraper
        except Exception as e:
            print('SEARCHING_DIALOG get_scrapper:', e)
            QMessageBox.critical(None, "DataBase Error:", str(e), QtWidgets.QMessageBox.Close)

    def task(self, db, i, scrapper):
        try:
            for mod in self.get_mods(i, scrapper):
                self.check_mod(db, mod)
                self.process_mod(db, mod)
        except Exception as e:
            print('SEARCHING_DIALOG task:', e)

    def get_mods(self, i, scrapper):
        try:
            mods = []
            soup = BeautifulSoup(scrapper.get(SearchThread.search_url + self.filter + SearchThread.posfix_url + str(i)).text, 'html.parser')
            for div in soup.find_all('div', class_='my-2'):
                mods.append(ModIndex(
                    path=SearchThread.url + div.find('a', class_="my-auto").get_attribute_list('href').pop(),
                    name=div.find('h3', class_="font-bold text-lg").text,
                    update_date=div.find('abbr', class_="tip standard-date standard-datetime").get_attribute_list('data-epoch').pop(),
                    icon=div.find('img', class_="mx-auto").get_attribute_list('src').pop()))
            return mods
        except Exception as e:
            print('SEARCHING_DIALOG get_mods:', e)

    def check_mod(self, db, mod):
        try:
            q = QtSql.QSqlQuery(db)
            q.prepare('SELECT M.update_date, M.blocked, M.loader, L.loader FROM Mods AS M INNER JOIN Lists AS L ON L.list = :list WHERE M.path == :path')
            q.bindValue(':path', mod.path)
            q.bindValue(':list', self.modlist)

            if q.exec():

                if q.next():

                    if q.value(0) != mod.update_date:
                        mod.update = 1

                    if q.value(1) == 0:

                        if q.value(2) not in (q.value(3), 'Sin Loader'):
                            mod.ignore = 1

                        q.prepare('SELECT 1 FROM ModsLists WHERE list == :list and mod == :mod')
                        q.bindValue(':list', self.modlist)
                        q.bindValue(':mod', mod.path)
                        if q.exec():
                            if not q.next():
                                mod.addlist = 1
                        else:
                            mod.error = 2
                            QMessageBox.critical(None, "Searching DB Error:", q.lastError().databaseText(), QtWidgets.QMessageBox.Close)
                            sys.exit(1)

                else:
                    mod.newmod = 1
                    mod.addlist = 1

            else:
                mod.error = 1
                QMessageBox.critical(None, "Searching DB Error:", q.lastError().databaseText(), QtWidgets.QMessageBox.Close)
                sys.exit(1)
        except Exception as e:
            print('SEARCHING_DIALOG check_mod:', e)

    def process_mod(self, db, mod):
        try:
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

                if mod.update:
                    q.prepare('UPDATE ModsLists SET updated = 1 WHERE mod == :mod;')
                    q.bindValue(':mod', mod.path)
                    q.exec()

                if mod.addlist:
                    q.prepare('INSERT INTO ModsLists(list, mod, ignored)' 'VALUES (:list, :mod, :ignored)')
                    q.bindValue(':list', self.modlist)
                    q.bindValue(':mod', mod.path)
                    q.bindValue(':ignored', mod.ignore)
                    q.exec()

                db.commit()
        except Exception as e:
            print('SEARCHING_DIALOG preocess_mod:', e)

    def set_close(self):
        try:
            self.canclose = True
        except Exception as e:
            print('SEARCHING_DIALOG set_close:', e)


class SearchingDialog(QtWidgets.QDialog):

    def __init__(self):
        super(SearchingDialog, self).__init__()
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
        self.ui = Ui_SearchingDialog()
        self.ui.setupUi(self)

        self.exit_code = 0
        self.search_thread = None

        self.setupWidgets()
        self.setupEvents()
        self.show()

    def setupWidgets(self):
        try:
            self.create_cmb_values_lists()
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
            self.ui.btnSearchNewMods.clicked.connect(self.btn_search_mods)
        except Exception as e:
            print('SEARCHING_DIALOG setupEvents:', e)

    def change_cmb_modlist(self):
        try:
            self.ui.btnSearchNewMods.setEnabled(self.ui.cmbModList.currentIndex() > 1)
        except Exception as e:
            print('SEARCHING_DIALOG change_cmb_modlist:', e)

    def btn_search_mods(self):
        try:
            self.ui.progressBar.setEnabled(True)
            self.ui.progressBar.setMaximum(0)

            self.ui.cmbModList.setEnabled(False)
            self.ui.spinPages.setEnabled(False)
            self.ui.btnSearchNewMods.setEnabled(False)

            self.search_thread = SearchThread(self.ui.cmbModList.currentText().strip(), self.ui.spinPages.value())

            self.search_thread.sig_max_pages.connect(self.set_max_pages)
            self.search_thread.sig_page_finish.connect(self.set_page_finish)
            self.search_thread.sig_finish_code.connect(self.set_finish_code)
            self.search_thread.finished.connect(self.set_finish_search)

            self.search_thread.start()
        except Exception as e:
            print('SEARCHING_DIALOG search_mods:', e)

    def set_max_pages(self, max_pages):
        try:
            self.ui.progressBar.setValue(0)
            self.ui.progressBar.setMaximum(max_pages)
            self.ui.progressBar.setFormat('%v/%m Procesados')
        except Exception as e:
            print('SEARCHING_DIALOG set_max_pages:', e)

    def set_page_finish(self, page_finish):
        try:
            self.ui.progressBar.setValue(page_finish)
        except Exception as e:
            print('SEARCHING_DIALOG set_page_finish:', e)

    def set_finish_search(self):
        try:
            if self.exit_code == 0:
                self.ui.progressBar.setValue(self.ui.progressBar.maximum())
                sleep(1)
                self.done(1)
            else:
                self.done(2)
        except Exception as e:
            print('SEARCHING_DIALOG set_finish_search:', e)

    def set_finish_code(self, code):
        self.exit_code = code

    def closeEvent(self, event):
        try:
            if self.search_thread is not None:
                self.search_thread.set_close()
                self.ui.progressBar.setFormat('Cancelando...')
                event.ignore()
        except Exception as e:
            print('SEARCHING_DIALOG closeEvent:', e)
