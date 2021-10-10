import sys

import requests
from PyQt5 import QtSql, QtWidgets
from PyQt5.QtCore import QThread, QByteArray, pyqtSignal
from PyQt5.QtWidgets import QMessageBox, QWidget
from bs4 import BeautifulSoup

from utils.database import Database
from utils.mod import ModIndex


class SearchThread(QThread):
    pagesize = 50
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}
    url = 'http://addons-ecs.forgesvc.net/api/v2/addon/search' \
          '?gameId=432' \
          '&sectionId=6' \
          '&categoryId=0' \
          '&sort=2' \
          '&pageSize=' + str(pagesize)

    filter = '&gameVersion='

    index = '&index='

    sig_max_pages = pyqtSignal(int)
    sig_page_finish = pyqtSignal(int)
    sig_finish_code = pyqtSignal(int)

    def __init__(self, modlist):
        super(SearchThread, self).__init__()

        self.modlist = modlist
        self.filter = ''
        self.canclose = False

        self.mods = []

    def run(self):
        try:
            self.search_mods()
        except Exception as e:
            print('SEARCH_THREAD run:', e)

    # ------------------------------------------------------------------------------------------------------------------

    def setFilter(self, db):
        try:
            q = QtSql.QSqlQuery(db)
            q.prepare('SELECT version FROM Lists WHERE listname == :listname')
            q.bindValue(':listname', self.modlist)
            if q.exec():
                if q.next():
                    self.filter = q.value(0)
                else:
                    QMessageBox.critical(QWidget(), "Searching DB Error:", 'No hay una lista seleccionada',
                                         QtWidgets.QMessageBox.Close)
                    sys.exit(1)
            else:
                QMessageBox.critical(QWidget(), "Searching DB Error:", q.lastError().databaseText(),
                                     QtWidgets.QMessageBox.Close)
                sys.exit(1)
        except Exception as e:
            print('SEARCH_THREAD set_filter:', e)

    # noinspection PyUnresolvedReferences
    def search_mods(self):
        try:
            db = Database.get_thread_sqlquery()
            self.setFilter(db)

            i = 0
            returned_mods = 1
            while returned_mods > 0:
                returned_mods = self.get_mods_from_page(i)
                i+= SearchThread.pagesize
            self.sig_max_pages.emit(len(self.mods))
            self.sig_page_finish.emit(0)

            for i, mod in enumerate(self.mods):
                if self.canclose:
                    self.sig_finish_code.emit(1)
                    break
                else:
                    self.check_mod(db, mod)
                    self.process_mod(db, mod)
                    self.sig_page_finish.emit(i)
            self.sig_finish_code.emit(0)
        except Exception as e:
            print('SEARCH_THREAD search_modslist:', e)

    def get_mods_from_page(self, i):
        try:
            url = SearchThread.url + SearchThread.filter + self.filter + self.index + str(SearchThread.pagesize * i)
            mods = requests.get(url, headers=SearchThread.header).json()
            for mod in mods:
                self.mods.append(ModIndex(mod))
            print(len(mods))
            return len(mods)

        except Exception as e:
            print('SEARCHING_DIALOG get_mods_from_page:', e)

    def check_mod(self, db, mod):
        try:
            q = QtSql.QSqlQuery(db)
            q.prepare('SELECT M.update_date, M.blocked, M.loader, L.loader FROM Mods AS M INNER JOIN Lists AS L ON L.listname = :listname WHERE M.path == :path')
            q.bindValue(':path', mod.path)
            q.bindValue(':listname', self.modlist)

            mod.setDate()
            if q.exec():
                if q.next():
                    if q.value(0) != mod.update_date:
                        mod.update = 1
                    if q.value(1) == 0:
                        if q.value(2) not in (q.value(3), 'Sin Loader', 'Forge / Fabric'):
                            mod.ignore = 1
                        q.prepare('SELECT 1 FROM ModsLists WHERE list == :list and mod == :mod')
                        q.bindValue(':list', self.modlist)
                        q.bindValue(':mod', mod.path)
                        if q.exec():
                            if not q.next():
                                mod.addlist = 1
                        else:
                            mod.error = 2
                            QMessageBox.critical(QWidget(), "Searching DB Error 2:", q.lastError().databaseText(), QtWidgets.QMessageBox.Close)
                            sys.exit(1)
                else:
                    mod.newmod = 1
                    mod.addlist = 1

            else:
                mod.error = 1
                QMessageBox.critical(QWidget(), "Searching DB Error 1:", q.lastError().databaseText(), QtWidgets.QMessageBox.Close)
                sys.exit(1)
        except Exception as e:
            print('SEARCH_THREAD check_mod:', e)

    def process_mod(self, db, mod):
        try:
            if mod.error != 1:
                db.transaction()

                q = QtSql.QSqlQuery(db)
                if mod.newmod:
                    mod.setLoader()
                    mod.setCategories()
                    mod.setIcon()

                    q.prepare('INSERT INTO Mods(path, name, loader, categories, update_date, icon) VALUES (:path, :name, :loader, :categories, :update_date, :icon)')
                    q.bindValue(':path', mod.path)
                    q.bindValue(':name', mod.name)
                    q.bindValue(':loader', mod.loader)
                    q.bindValue(':categories', mod.categories)
                    q.bindValue(':update_date', mod.update_date)
                    q.bindValue(':icon', mod.icon)
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
            print('SEARCH_THREAD preocess_mod:', e)

    def set_close(self):
        try:
            self.canclose = True
        except Exception as e:
            print('SEARCH_THREAD set_close:', e)
