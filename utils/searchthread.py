import sys
import time

import cloudscraper
import requests
from PyQt5 import QtSql, QtWidgets
from PyQt5.QtCore import QThread, QByteArray, pyqtSignal
from PyQt5.QtWidgets import QMessageBox, QWidget
from bs4 import BeautifulSoup
from cloudscraper import CloudflareChallengeError

from utils.database import Database
from utils.mod import ModIndex


class SearchThread(QThread):
    url = 'https://www.curseforge.com'
    search_url = url + '/minecraft/mc-mods'
    posfix_url = '&filter-sort=2&page='

    filter_forge = ''
    filter_fabric = ''

    sig_max_pages = pyqtSignal(int)
    sig_page_finish = pyqtSignal(int)
    sig_finish_code = pyqtSignal(int)

    def __init__(self, modlist, max_pages):
        super(SearchThread, self).__init__()
        self.cscraper = None

        self.max_pages = max_pages
        self.maxpages_forge = max_pages
        self.maxpages_fabric = max_pages
        self.modlist = modlist

        self.filter = ''
        self.canclose = False

    # ------------------------------------------------------------------------------------------------------------------

    def setFilter(self, db):
        try:
            q = QtSql.QSqlQuery(db)
            q.prepare('SELECT filter FROM Lists WHERE list == :list')
            q.bindValue(':list', self.modlist)
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
            print('SEARCHING_DIALOG set_filter:', e)

    def setCscraper(self):
        try:
            while True:
                try:
                    cscraper = cloudscraper.create_scraper(delay=1)
                    cscraper.get(SearchThread.search_url)
                    self.cscraper = cscraper
                except CloudflareChallengeError as e:
                    # print('ERROR: ' + str(e))
                    time.sleep(1)
        except Exception as e:
            print('SEARCHING_DIALOG setCscraper:', e)

    def execCscraper(self, url):
        try:
            while True:
                try:
                    return self.cscraper.get(url).text
                except CloudflareChallengeError:
                    self.setCscraper()
        except Exception as e:
            print('SEARCHING_DIALOG execCscraper:', e)

    # noinspection PyUnresolvedReferences
    def setMaxpages(self):
        try:
            if self.max_pages == 0:
                soup = BeautifulSoup(
                    self.execCscraper(SearchThread.search_url + self.filter + SearchThread.posfix_url + '1'), 'html.parser')
                maxpages = soup.find_all('a', class_="pagination-item").pop().find('span').text
                self.max_pages = int(maxpages)
            self.sig_max_pages.emit(self.max_pages)
        except Exception as e:
            print('SEARCHING_DIALOG set_maxpages:', e)

    # noinspection PyUnresolvedReferences
    def setMaxpagesForgeFabric(self):
        try:
            if self.max_pages == 0:
                soup = BeautifulSoup(self.execCscraper(SearchThread.search_url + SearchThread.filter_forge + SearchThread.posfix_url + '1'), 'html.parser')
                self.maxpages_forge = int(soup.find_all('a', class_="pagination-item").pop().find('span').text)
                soup = BeautifulSoup(self.execCscraper(SearchThread.search_url + SearchThread.filter_fabric + SearchThread.posfix_url + '1'), 'html.parser')
                self.maxpages_fabric = int(soup.find_all('a', class_="pagination-item").pop().find('span').text)
            self.sig_max_pages.emit(self.maxpages_forge + self.maxpages_fabric)
        except Exception as e:
            print('SEARCHING_DIALOG set_maxpages:', e)

    # ------------------------------------------------------------------------------------------------------------------

    def get_mods_from_page(self, i):
        try:
            mods = []
            soup = BeautifulSoup(self.execCscraper(SearchThread.search_url + self.filter + SearchThread.posfix_url + str(i)), 'html.parser')
            for div in soup.find_all('div', class_='my-2'):
                mods.append(ModIndex(
                    path=SearchThread.get_path(div),
                    name=SearchThread.get_name(div),
                    categories=SearchThread.get_categories(div),
                    update_date=SearchThread.get_date(div),
                    icon=SearchThread.get_icon(div)
                ))
            return mods
        except Exception as e:
            print('SEARCHING_DIALOG get_mods_from_page:', e)

    @staticmethod
    def get_path(div):
        try:
            return div.find('a', class_="my-auto").get_attribute_list('href').pop()
        except Exception:
            return 'PATH'

    @staticmethod
    def get_name(div):
        try:
            return div.find('h3', class_="font-bold text-lg").text
        except Exception:
            return 'NAME'

    @staticmethod
    def get_date(div):
        try:
            fechas = div.find_all('abbr', class_="tip standard-date standard-datetime")
            update_date = fechas.pop().get_attribute_list('data-epoch').pop()
            # create_date = fechas.pop().get_attribute_list('data-epoch').pop()
            return update_date
        except Exception:
            return 0

    @staticmethod
    def get_icon(div):
        try:
            url = div.find('img', class_="mx-auto").get_attribute_list('src').pop()
            return QByteArray(requests.get(url).content)
        except Exception:
            return 'ICON'

    @staticmethod
    def get_categories(div):
        try:
            categories = []
            ignore = ('mc-addons',
                      'addons-thermalexpansion',
                      'addons-tinkers-construct',
                      'addons-industrialcraft',
                      'addons-thaumcraft',
                      'addons-buildcraft',
                      'addons-forestry',
                      'blood-magic',
                      'lucky-blocks',
                      'applied-energistics-2',
                      'crafttweaker')

            for div in div.find_all('div', class_='px-1')[1:]:
                addon = False
                cat = div.find('a').get_attribute_list('href').pop().split('/')[-1]

                if cat != 'mc-creator':
                    if cat in ignore:
                        if addon is False:
                            addon = True
                            categories.append('mc-addons')
                    else:
                        categories.append(cat)

            if len(categories) == 0:
                categories = 'without-category'
            else:
                categories.sort()
                categories = ','.join(categories)

            return categories
        except Exception:
            return 'without-category'

    # ------------------------------------------------------------------------------------------------------------------

    # noinspection PyUnresolvedReferences
    def run(self):
        try:
            if self.modlist is None:
                self.search_mods()
            else:
                self.search_modslist()
        except Exception as e:
            print('SEARCHING_DIALOG run:', e)

    def search_mods(self):
        db = Database.get_thread_sqlquery()
        self.setCscraper()
        self.setMaxpagesForgeFabric()
        self.sig_page_finish.emit(0)


    def search_modslist(self):
        try:
            db = Database.get_thread_sqlquery()
            self.setFilter(db)
            self.setCscraper()
            self.setMaxpages()
            self.sig_page_finish.emit(0)
            for i in range(1, self.max_pages + 1):
                if self.canclose:
                    self.sig_finish_code.emit(1)
                    break
                else:
                    self.process_page(db, i)
                    self.sig_page_finish.emit(i)
            self.sig_finish_code.emit(0)
        except Exception as e:
            print('SEARCHING_DIALOG search_modslist:', e)

    def process_page(self, db, i):
        try:
            for mod in self.get_mods_from_page(i):
                self.check_mod(db, mod)
                self.process_mod(db, mod)
        except Exception as e:
            print('SEARCHING_DIALOG process_page:', e)

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
