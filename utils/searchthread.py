import json
import sys
import traceback

import requests
from PyQt5 import QtSql, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QMessageBox, QWidget

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

    def __init__(self, modlist, searchnewupdate):
        super(SearchThread, self).__init__()

        self.modlist = modlist
        self.searchnewupdate = searchnewupdate

        self.list_version = ''
        self.valid_loaders = ''
        self.last_update_date = 0
        self.canclose = False

        self.mods = []

    def run(self):
        try:
            self.search_mods()
        except Exception as e:
            print('SEARCH_THREAD run:', e)

    # ------------------------------------------------------------------------------------------------------------------

    def getListInfo(self, db):
        try:
            q = QtSql.QSqlQuery(db)

            q.prepare('SELECT L.version, L.loader FROM Lists as L WHERE L.listname == :listname;')
            q.bindValue(':listname', self.modlist)
            if q.exec():
                if q.next():
                    self.list_version = q.value(0)
                    self.valid_loaders = [q.value(1), 'Sin Loader', 'Forge / Fabric']
                else:
                    QMessageBox.critical(None, "Searching DB Error:", 'No hay una lista seleccionada', QtWidgets.QMessageBox.Close)
                    print("Searching DB Error:", 'No hay una lista seleccionada')
                    sys.exit(1)
            else:
                QMessageBox.critical(QWidget(), "Searching DB Error:", q.lastError().databaseText(),
                                     QtWidgets.QMessageBox.Close)
                sys.exit(1)

            q.prepare('SELECT MAX(M.update_date) FROM ModsLists AS ML LEFT JOIN Mods AS M ON M.projectid = ML.mod WHERE ML.list = :listname;')
            q.bindValue(':listname', self.modlist)
            if q.exec():
                if q.next():
                    if q.value(0):
                        self.last_update_date = q.value(0)
                    else:
                        self.last_update_date = 0
                else:
                    QMessageBox.critical(None, "Searching DB Error:", 'No hay una lista seleccionada', QtWidgets.QMessageBox.Close)
                    print("Searching DB Error:", 'No hay una lista seleccionada')
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
            self.getListInfo(db)

            i = 0
            while self.get_mods_from_page(i):
                i += 1
                self.sig_max_pages.emit(len(self.mods))
                if self.canclose:
                    break

            if not self.canclose:
                self.sig_max_pages.emit(len(self.mods))
                self.sig_page_finish.emit(0)

            for i, mod in enumerate(self.mods):
                if self.canclose:
                    break
                else:
                    self.check_mod(db, mod)
                    self.process_mod(db, mod)
                    self.sig_page_finish.emit(i)

            if self.canclose:
                self.sig_finish_code.emit(1)
            else:
                self.sig_finish_code.emit(0)

        except Exception as e:
            print('SEARCH_THREAD search_modslist:', e)

    def get_mods_from_page(self, i):
        try:
            url = SearchThread.url + SearchThread.filter + self.list_version + self.index + str(SearchThread.pagesize * i)
            mods = requests.get(url, headers=SearchThread.header).json()
            for mod in mods:
                m = ModIndex(mod)
                if self.searchnewupdate:
                    m.setDate()
                    if m.update_date < self.last_update_date:
                        return 0
                self.mods.append(m)
            return len(mods)
        except json.decoder.JSONDecodeError:
            QMessageBox.critical(None, 'API ERROR:', 'API ERROR:\n\nLa consulta a la API no ha regresado ningun valor.', QtWidgets.QMessageBox.Close)
            return 0
        except Exception as e:
            print('SEARCH_THREAD get_mods_from_page:', e) #, traceback.format_exc())

    def check_mod(self, db, mod):
        q = QtSql.QSqlQuery(db)
        q.prepare('SELECT M.update_date, M.blocked, M.preignore FROM Mods AS M WHERE M.projectid == :projectid')
        q.bindValue(':projectid', mod.projectid)

        mod.setDate()

        if q.exec():
            if q.next():
                mod.setDate()
                if q.value(0) < mod.update_date:
                    mod.update = 1

                if q.value(1) == 0:
                    mod.addlist = 1

                mod.preignore = q.value(2)
            else:
                mod.newmod = 1
                mod.addlist = 1

            if mod.loader not in self.valid_loaders:
                mod.addlist = 0

        else:
            mod.error = 1
            QMessageBox.critical(None, "Searching DB Error 1:", q.lastError().text(), QtWidgets.QMessageBox.Close)
            print("Searching DB Error 1:", q.lastError().text())
            sys.exit(1)

    def process_mod(self, db, mod):
        try:
            if mod.error != 1:
                db.transaction()

                q = QtSql.QSqlQuery(db)

                if mod.newmod:
                    mod.setCategories()
                    mod.setIcon()
                    q.prepare('INSERT OR IGNORE INTO Mods(path, name, loader, categories, update_date, icon, projectid) VALUES (:path, :name, :loader, :categories, :update_date, :icon, :projectid)')
                    q.bindValue(':path',        mod.path)
                    q.bindValue(':name',        mod.name)
                    q.bindValue(':loader',      mod.loader)
                    q.bindValue(':categories',  mod.categories)
                    q.bindValue(':update_date', mod.update_date)
                    q.bindValue(':icon',        mod.icon)
                    q.bindValue(':projectid',   mod.projectid)
                    if not q.exec():
                        print('DB NewMod:', q.lastError().text(), mod.projectid, mod.name)

                    mod.setDependencies()
                    if len(mod.dependencies) > 0:
                        for dep in mod.dependencies:
                            q.prepare('INSERT OR IGNORE INTO Dependencies(mod, dependency) VALUES (:mod, :dependency)')
                            q.bindValue(':mod', mod.projectid)
                            q.bindValue(':dependency', dep)
                            if not q.exec():
                                print('DB NewMod:', q.lastError().text(), mod.projectid, mod.name)

                if mod.update:
                    q.prepare('UPDATE ModsLists SET updated = 1 WHERE mod == :mod;')
                    q.bindValue(':mod', mod.projectid)
                    if not q.exec():
                        print('DB Update:', q.lastError().text(), mod.projectid, mod.name)

                if mod.addlist:
                    q.prepare('INSERT OR IGNORE INTO ModsLists(list, mod, ignored)' 'VALUES (:list, :mod, :ignored)')
                    q.bindValue(':list',    self.modlist)
                    q.bindValue(':mod',     mod.projectid)
                    q.bindValue(':ignored', mod.preignore)
                    if not q.exec():
                        print('DB AddList:', q.lastError().text(), mod.projectid, mod.name)

                db.commit()
        except Exception as e:
            print('SEARCH_THREAD process_mod:', e)  # , traceback.format_exc())
            print('     ', mod.projectid)
            print('     ', mod.path)
            print('     ', mod.name)
            print('     ', mod.loader)
            print('     ', mod.categories)
            print('     ', mod.update_date)
            print('     ', mod.icon)
            print()

    def set_close(self):
        try:
            self.canclose = True
        except Exception as e:
            print('SEARCH_THREAD set_close:', e)
