from datetime import datetime

import requests
from PyQt5 import QtWidgets, QtSql, Qt
from PyQt5.QtCore import QByteArray, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox

from utils.icon_utils import IconUtils
from utils.utils import Utils


class ModIndex:
    cat_id = {
        406: "-cc-world-gen",
        407: "-cc-world-biomes",
        408: "-cc-world-ores-resources",
        409: "-cc-world-structures",
        410: "-cc-world-dimensions",
        411: "-cc-world-mobs",

        412: "-cc-technology",
        413: "-cc-technology-processing",
        414: "-cc-technology-player-transport",
        415: "-cc-technology-item-fluid-energy-transport",
        416: "-cc-technology-farming",
        417: "-cc-technology-energy",
        418: "-cc-technology-genetics",
        4843: "-cc-technology-automation",

        419: "-cc-magic",
        420: "-cc-storage",
        421: "-cc-library-api",
        422: "-cc-adventure-rpg",
        423: "-cc-map-information",
        424: "-cc-cosmetic",
        425: "-cc-mc-miscellaneous",

        426: "-cc-mc-addons",
        427: "-cc-mc-addons",  # "addons-thermalexpansion",
        428: "-cc-mc-addons",  # "addons-tinkers-construct",
        429: "-cc-mc-addons",  # "addons-industrialcraft",
        430: "-cc-mc-addons",  # "addons-thaumcraft",
        432: "-cc-mc-addons",  # "addons-buildcraft",
        433: "-cc-mc-addons",  # "addons-forestry",
        4485: "-cc-mc-addons",  # "blood-magic",
        4486: "-cc-mc-addons",  # "[4486]lucky-blocks",
        4545: "-cc-mc-addons",  # "applied-energistics-2",
        4773: "-cc-mc-addons",  # "crafttweaker",

        434: "-cc-armor-weapons-tools",
        435: "-cc-server-utility",
        436: "-cc-mc-food",
        4558: "-cc-redstone",
        4671: "-cc-twitch-integration",

        4906: "-cc-mc-creator",
        4780: "-cc-fabric",

        5129: "-cc-vanilla-plus",
        5191: "-cc-utility-qol"
    }

    def __init__(self, mod: dict):
        try:
            self.projectid = mod.get('id')
            self.path = mod.get('links').get('websiteUrl')
            self.name = mod.get('name')
            self.loader = self.getLoader(mod.get('latestFilesIndexes'))
            self.description = mod.get('summary')
            self.categories = mod.get('categories')
            self.update_date = mod.get('dateModified')
            self.icon = mod.get('logo')

            self.error = 0
            self.newmod = 0
            self.update = 0
            self.addlist = 0
            self.autoinstall = 0
            self.autoignore = 0

        except Exception as e:
            Utils.print_exception('ModIndex init ' + str(self.projectid), e)

    def setCategories(self):
        try:
            categories = set()
            if isinstance(self.categories, list):
                for cat in self.categories:
                    cat = ModIndex.cat_id.get(cat.get('id'))
                    if cat is not None:
                        categories.add(cat)
            categories = list(categories)
            categories.sort()

            if len(categories) > 0:
                self.categories = ','.join(categories)
            else:
                self.categories = '-cc-without-category'
        except Exception as e:
            Utils.print_exception('MOD setCategories' + str(self.projectid), e)
            self.categories = 'error'

    def setDate(self):
        try:
            if isinstance(self.update_date, str):
                if self.update_date.__contains__('.'):
                    self.update_date = int(datetime.strptime(self.update_date, '%Y-%m-%dT%H:%M:%S.%f%z').replace(
                        microsecond=0).timestamp())
                else:
                    self.update_date = int(
                        datetime.strptime(self.update_date, '%Y-%m-%dT%H:%M:%S%z').replace(microsecond=0).timestamp())
            elif not isinstance(self.update_date, int):
                self.update_date = 0
        except Exception as e:
            Utils.print_exception('MOD setDate' + str(self.projectid), e)
            self.update_date = -1

    def setIcon(self):
        try:
            if self.icon:
                pix = QPixmap()
                pix.loadFromData(requests.get(self.icon.get('url')).content)
                pix.scaled(48, 48, Qt.KeepAspectRatio)
                self.icon = IconUtils.pixmap_to_qbytearray(pix)
            elif not isinstance(self.icon, QByteArray):
                self.icon = QByteArray()
        except Exception as e:
            Utils.print_exception('MOD setIcon' + str(self.projectid), e)
            self.icon = QByteArray()

    '''
    0 = Any
    1 = Forge
    2 = Cauldron
    3 = LiteLoader
    4 = Fabric
    5 = Quilt
    6 = NeoForge
    '''
    def getLoader(self, files):
        try:
            forge = False
            fabric = False

            for file in files:
                modloader = file.get('modLoader')
                if modloader in [1, 6]:
                    forge = True
                elif modloader in [4, 5]:
                    fabric = True

            if forge and fabric:
                return 'Forge | Fabric'
            elif forge:
                return 'Forge'
            elif fabric:
                return 'Fabric'
            else:
                return 'No Loader'
        except Exception as e:
            Utils.print_exception('MOD getLoader' + str(self.projectid), e)
            return 'error'

    def load_data(self):
        self.setCategories()
        self.setDate()
        self.setIcon()

    def print_data(self):
        print(self.icon)
        print('URL:         ' + self.path)
        print('ProjectID:   ' + str(self.projectid))
        print('Name:        ' + self.name)
        print('Loader:      ' + self.loader)
        print('Update date: ' + str(self.update_date))
        for cat in self.categories.split(','):
            print('     ' + cat)
        print('')

    # ----------------------------------------------------------------------------

    def check_mod(self, db, valid_loaders):
        try:
            q = QtSql.QSqlQuery(db)
            q.prepare(
                'SELECT M.update_date, M.blocked, M.loader, M.autoinstall, M.autoignore FROM Mods AS M WHERE M.projectid == :projectid')
            q.bindValue(':projectid', self.projectid)

            if q.exec():

                self.setDate()
                if q.next():  # Mod exist in DB

                    if q.value(0) < self.update_date:
                        self.update = 1

                    if q.value(1) == 0:
                        self.addlist = int(q.value(2) in valid_loaders)
                        self.autoinstall = q.value(3)
                        self.autoignore = q.value(4)

                else:  # Mod NO exist in DB
                    self.newmod = 1
                    self.addlist = int(self.loader in valid_loaders)

                return True

            else:
                self.error = 1
                QMessageBox.critical(None, "Searching DB Error 1:", q.lastError().text(), QtWidgets.QMessageBox.Close)
                print("MOD_INDEX DB Error 1:", q.lastError().text())
                return False

        except Exception as e:
            Utils.print_exception('MOD_INDEX check_mod' + str(self.projectid), e)
            return False

    def process_mod(self, db, modlist=None, version=None):
        try:
            if self.error != 1:
                db.transaction()

                q = QtSql.QSqlQuery(db)

                if self.newmod:
                    self.newmod_db(q)

                if self.update:
                    self.update_db(q)

                if version is not None:
                    self.version_db(q, version)

                if self.addlist:
                    self.addlist_db(q, modlist)

                db.commit()

        except Exception as e:
            Utils.print_exception('SEARCH_THREAD process_mod ' + str(self.projectid), e)

    def newmod_db(self, q):
        self.setCategories()
        self.setIcon()
        q.prepare(
            'INSERT OR IGNORE INTO Mods(projectid, name, description, categories, loader, update_date, icon, path) '
            'VALUES (:projectid, :name, :description, :categories, :loader, :update_date, :icon, :path)')
        q.bindValue(':projectid', self.projectid)
        q.bindValue(':name', self.name)
        q.bindValue(':description', self.description)
        q.bindValue(':categories', self.categories)
        q.bindValue(':loader', self.loader)
        q.bindValue(':update_date', self.update_date)
        q.bindValue(':icon', self.icon)
        q.bindValue(':path', self.path)

        if not q.exec():
            print('MOD_INDEX DB NewMod:', q.lastError().text(), self.projectid, self.name)

    def update_db(self, q):
        q.prepare('UPDATE ModsLists SET updated = 1 WHERE mod == :mod;')
        q.bindValue(':mod', self.projectid)
        if not q.exec():
            print('MOD_INDEX DB Update ML:', q.lastError().text(), self.projectid, self.name)

        q.prepare('UPDATE Mods SET update_date = :update_date WHERE projectid == :projectid;')
        q.bindValue(':projectid', self.projectid)
        q.bindValue(':update_date', self.update_date)
        if not q.exec():
            print('MOD_INDEX DB Update M:', q.lastError().text(), self.projectid, self.name)

    def version_db(self, q, version):
        q.prepare('INSERT OR IGNORE INTO ModsVersions(version, mod)' 'VALUES (:version, :mod)')
        q.bindValue(':version', version)
        q.bindValue(':mod', self.projectid)
        if not q.exec():
            print('MOD_INDEX DB Update MV:', q.lastError().text(), self.projectid, self.name)

    def addlist_db(self, q, modlist):
        q.prepare(
            'INSERT OR IGNORE INTO ModsLists(list, mod, installed, ignored)' 'VALUES (:list, :mod, :installed, :ignored)')
        q.bindValue(':list', modlist)
        q.bindValue(':mod', self.projectid)
        q.bindValue(':installed', self.autoinstall)
        q.bindValue(':ignored', self.autoignore)
        if not q.exec():
            print('MOD_INDEX DB AddList:', q.lastError().text(), self.projectid, self.name)


'''
class ModIndex:
    cat_id = {
        406:  "-cc-world-gen",
        407:  "-cc-world-biomes",
        408:  "-cc-world-ores-resources",
        409:  "-cc-world-structures",
        410:  "-cc-world-dimensions",
        411:  "-cc-world-mobs",

        412:  "-cc-technology",
        413:  "-cc-technology-processing",
        414:  "-cc-technology-player-transport",
        415:  "-cc-technology-item-fluid-energy-transport",
        416:  "-cc-technology-farming",
        417:  "-cc-technology-energy",
        418:  "-cc-technology-genetics",
        4843: "-cc-technology-automation",

        419:  "-cc-magic",
        420:  "-cc-storage",
        421:  "-cc-library-api",
        422:  "-cc-adventure-rpg",
        423:  "-cc-map-information",
        424:  "-cc-cosmetic",
        425:  "-cc-mc-miscellaneous",

        426:  "-cc-mc-addons",
        427:  "-cc-mc-addons",  # "addons-thermalexpansion",
        428:  "-cc-mc-addons",  # "addons-tinkers-construct",
        429:  "-cc-mc-addons",  # "addons-industrialcraft",
        430:  "-cc-mc-addons",  # "addons-thaumcraft",
        432:  "-cc-mc-addons",  # "addons-buildcraft",
        433:  "-cc-mc-addons",  # "addons-forestry",
        4485: "-cc-mc-addons",  # "blood-magic",
        4486: "-cc-mc-addons",  # "[4486]lucky-blocks",
        4545: "-cc-mc-addons",  # "applied-energistics-2",
        4773: "-cc-mc-addons",  # "crafttweaker",

        434:  "-cc-armor-weapons-tools",
        435:  "-cc-server-utility",
        436:  "-cc-mc-food",
        4558: "-cc-redstone",
        4671: "-cc-twitch-integration",

        4906: "-cc-mc-creator",
        4780: "-cc-fabric",

        5129: "-cc-vanilla-plus",
        5191: "-cc-utility-qol"
    }

    def __init__(self, mod: dict):
        try:
            self.projectid = mod.get('id')
            self.path = mod.get('websiteUrl')
            self.name = mod.get('name')
            self.loader = self.getLoader(mod)
            self.description = mod.get('summary')
            self.categories = mod.get('categories')
            self.update_date = mod.get('dateModified')
            self.icon = mod.get('attachments')

            self.error = 0
            self.newmod = 0
            self.update = 0
            self.addlist = 0
            self.autoinstall = 0
            self.autoignore = 0

        except Exception as e:
            Utils.print_exception('ModIndex init', e)

    def setCategories(self):
        try:
            categories = set()
            if isinstance(self.categories, list):
                for cat in self.categories:
                    cat = ModIndex.cat_id.get(cat.get('categoryId'))
                    if cat is not None:
                        categories.add(cat)
            categories = list(categories)
            categories.sort()

            if len(categories) > 0:
                self.categories = ','.join(categories)
            else:
                self.categories = '-cc-without-category'
        except Exception as e:
            Utils.print_exception('MOD setCategories' + str(self.projectid), e)
            self.categories = 'error'

    def setDate(self):
        try:
            if isinstance(self.update_date, str):
                if self.update_date.__contains__('.'):
                    self.update_date = int(datetime.strptime(self.update_date, '%Y-%m-%dT%H:%M:%S.%f%z').replace(microsecond=0).timestamp())
                else:
                    self.update_date = int(datetime.strptime(self.update_date, '%Y-%m-%dT%H:%M:%S%z').replace(microsecond=0).timestamp())
            elif not isinstance(self.update_date, int):
                self.update_date = 0
        except Exception as e:
            Utils.print_exception('MOD setDate' + str(self.projectid), e)
            self.update_date = -1

    def setIcon(self):
        try:
            if isinstance(self.icon, list):
                for attach in self.icon:
                    if attach.get('isDefault') is True:
                        pix = QPixmap()
                        pix.loadFromData(requests.get(attach.get('thumbnailUrl')).content)
                        pix.scaled(48, 48, Qt.KeepAspectRatio)
                        self.icon = IconUtils.pixmap_to_qbytearray(pix)
            elif not isinstance(self.icon, QByteArray):
                self.icon = QByteArray()
        except Exception as e:
            Utils.print_exception('MOD setIcon' + str(self.projectid), e)
            self.icon = QByteArray()

    def getLoader(self, mod):
        try:
            forge = False
            fabric = False


            if mod.get('modLoaders') is not None:
                for loader in mod.get('modLoaders'):
                    if loader == 'Forge':
                        forge = True
                    elif loader == 'Fabric':
                        fabric = True

            elif mod.get('gameVersionLatestFiles') is not None:
                for file in mod.get('gameVersionLatestFiles'):
                    if file.get('modLoader') == 1:
                        forge = True
                    elif file.get('modLoader') == 4:
                        fabric = True

            if forge and fabric:
                return 'Forge | Fabric'
            elif forge:
                return 'Forge'
            elif fabric:
                return 'Fabric'
            else:
                return 'No Loader'
        except Exception as e:
            Utils.print_exception('MOD getLoader' + str(self.projectid), e)
            return 'error'

    def load_data(self):
        self.setCategories()
        self.setDate()
        self.setIcon()

    def print_data(self):
        print(self.icon)
        print('URL:         ' + self.path)
        print('ProjectID:   ' + str(self.projectid))
        print('Name:        ' + self.name)
        print('Loader:      ' + self.loader)
        print('Update date: ' + str(self.update_date))
        for cat in self.categories.split(','):
            print('     ' + cat)
        print('')

# ----------------------------------------------------------------------------

    def check_mod(self, db, valid_loaders):
        try:
            q = QtSql.QSqlQuery(db)
            q.prepare(
                'SELECT M.update_date, M.blocked, M.loader, M.autoinstall, M.autoignore FROM Mods AS M WHERE M.projectid == :projectid')
            q.bindValue(':projectid', self.projectid)

            if q.exec():

                self.setDate()
                if q.next():  # Mod exist in DB

                    if q.value(0) < self.update_date:
                        self.update = 1

                    if q.value(1) == 0:
                        self.addlist = int(q.value(2) in valid_loaders)
                        self.autoinstall = q.value(3)
                        self.autoignore = q.value(4)

                else:  # Mod NO exist in DB
                    self.newmod = 1
                    self.addlist = int(self.loader in valid_loaders)

                return True

            else:
                self.error = 1
                QMessageBox.critical(None, "Searching DB Error 1:", q.lastError().text(), QtWidgets.QMessageBox.Close)
                print("MOD_INDEX DB Error 1:", q.lastError().text())
                return False

        except Exception as e:
            Utils.print_exception('MOD_INDEX check_mod' + str(self.projectid), e)
            return False

    def process_mod(self, db, modlist=None, version=None):
        try:
            if self.error != 1:
                db.transaction()

                q = QtSql.QSqlQuery(db)

                if self.newmod:
                    self.newmod_db(q)

                if self.update:
                    self.update_db(q)

                if version is not None:
                    self.version_db(q, version)

                if self.addlist:
                    self.addlist_db(q, modlist)

                db.commit()

        except Exception as e:
            Utils.print_exception('SEARCH_THREAD process_mod' + str(self.projectid), e)

    def newmod_db(self, q):
        self.setCategories()
        self.setIcon()
        q.prepare(
            'INSERT OR IGNORE INTO Mods(projectid, name, description, categories, loader, update_date, icon, path) '
            'VALUES (:projectid, :name, :description, :categories, :loader, :update_date, :icon, :path)')
        q.bindValue(':projectid', self.projectid)
        q.bindValue(':name', self.name)
        q.bindValue(':description', self.description)
        q.bindValue(':categories', self.categories)
        q.bindValue(':loader', self.loader)
        q.bindValue(':update_date', self.update_date)
        q.bindValue(':icon', self.icon)
        q.bindValue(':path', self.path)

        if not q.exec():
            print('MOD_INDEX DB NewMod:', q.lastError().text(), self.projectid, self.name)

    def update_db(self, q):
        q.prepare('UPDATE ModsLists SET updated = 1 WHERE mod == :mod;')
        q.bindValue(':mod', self.projectid)
        if not q.exec():
            print('MOD_INDEX DB Update ML:', q.lastError().text(), self.projectid, self.name)

        q.prepare('UPDATE Mods SET update_date = :update_date WHERE projectid == :projectid;')
        q.bindValue(':projectid', self.projectid)
        q.bindValue(':update_date', self.update_date)
        if not q.exec():
            print('MOD_INDEX DB Update M:', q.lastError().text(), self.projectid, self.name)

    def version_db(self, q, version):
        q.prepare('INSERT OR IGNORE INTO ModsVersions(version, mod)' 'VALUES (:version, :mod)')
        q.bindValue(':version', version)
        q.bindValue(':mod', self.projectid)
        if not q.exec():
            print('MOD_INDEX DB Update MV:', q.lastError().text(), self.projectid, self.name)

    def addlist_db(self, q, modlist):
        q.prepare(
            'INSERT OR IGNORE INTO ModsLists(list, mod, installed, ignored)' 'VALUES (:list, :mod, :installed, :ignored)')
        q.bindValue(':list', modlist)
        q.bindValue(':mod', self.projectid)
        q.bindValue(':installed', self.autoinstall)
        q.bindValue(':ignored', self.autoignore)
        if not q.exec():
            print('MOD_INDEX DB AddList:', q.lastError().text(), self.projectid, self.name)
'''