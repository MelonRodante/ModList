import json
import sys

import requests
from PyQt5 import QtSql, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QMessageBox, QWidget

from utils.curseapilinks import CurseAPI
from utils.database import Database
from utils.modindex import ModIndex
from utils.utils import Utils
from windows.warning_dialog import WarningDialog


class SearchThread(QThread):

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
            Utils.print_exception('SEARCH_THREAD run', e)

    # ------------------------------------------------------------------------------------------------------------------

    # noinspection PyUnresolvedReferences
    def search_mods(self):
        try:
            db = Database.get_thread_sqlquery()
            self.getListInfo(db)

            if not self.canclose:
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
                        mod.check_mod(db, self.valid_loaders)
                        mod.process_mod(db, self.modlist, self.list_version)
                        self.sig_page_finish.emit(i)

                if self.canclose:
                    self.sig_finish_code.emit(1)
                else:
                    self.sig_finish_code.emit(0)

        except Exception as e:
            Utils.print_exception('SEARCH_THREAD search_mods', e)

    def getListInfo(self, db):
        try:
            q = QtSql.QSqlQuery(db)

            q.prepare('SELECT L.version, L.loader FROM Lists as L WHERE L.listname == :listname;')
            q.bindValue(':listname', self.modlist)
            if q.exec():
                if q.next():
                    self.list_version = q.value(0)
                    self.valid_loaders = [q.value(1), 'No Loader', 'Forge | Fabric']
                else:
                    QMessageBox.critical(QWidget(), "Searching Error:", 'No list selected', QtWidgets.QMessageBox.Close)
                    self.canclose = True
            else:
                QMessageBox.critical(QWidget(), "Searching DB Error:", q.lastError().databaseText(), QtWidgets.QMessageBox.Close)
                self.canclose = True

            q.prepare('SELECT MAX(M.update_date) FROM ModsLists AS ML LEFT JOIN Mods AS M ON M.projectid = ML.mod WHERE ML.list = :listname;')
            q.bindValue(':listname', self.modlist)
            if q.exec():
                if q.next():
                    if q.value(0):
                        self.last_update_date = q.value(0)
                    else:
                        self.last_update_date = 0
                else:
                    QMessageBox.critical(QWidget(), "Searching Error:", 'No list selected', QtWidgets.QMessageBox.Close)
                    self.canclose = True
            else:
                QMessageBox.critical(QWidget(), "Searching DB Error:", q.lastError().databaseText(), QtWidgets.QMessageBox.Close)
                self.canclose = True

        except Exception as e:
            Utils.print_exception('SEARCH_THREAD getListInfo', e)

    def get_mods_from_page(self, i):
        url = ''
        page = ''
        try:
            url = CurseAPI.search_base_query + CurseAPI.search_filter_version + self.list_version + CurseAPI.search_offset + str(int(CurseAPI.pageSize) * i)
            page = requests.get(url, headers=CurseAPI.header)
            # mods = page.json()
            print(url)
            mods = page.json().get('data')
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
            print(url)
            print(i)
            print('\n\n' + page.text)
            return 0

        except Exception as e:
            Utils.print_exception('SEARCH_THREAD get_mods_from_page', e)

    def set_close(self):
        try:
            self.canclose = True

        except Exception as e:
            Utils.print_exception('SEARCH_THREAD set_close', e)


