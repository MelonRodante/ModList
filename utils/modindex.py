from datetime import datetime

import requests
from PyQt5 import QtWidgets, QtSql
from PyQt5.QtCore import QByteArray
from PyQt5.QtWidgets import QMessageBox


class ModIndex:
    cat_id = {
        406:  "world-gen",
        407:  "world-biomes",
        408:  "world-ores-resources",
        409:  "world-structures",
        410:  "world-dimensions",
        411:  "world-mobs",

        412:  "technology",
        413:  "technology-processing",
        414:  "technology-player-transport",
        415:  "technology-item-fluid-energy-transport",
        416:  "technology-farming",
        417:  "technology-energy",
        418:  "technology-genetics",
        4843: "technology-automation",

        419:  "magic",
        420:  "storage",
        421:  "library-api",
        422:  "adventure-rpg",
        423:  "map-information",
        424:  "cosmetic",
        425:  "mc-miscellaneous",

        426:  "mc-addons",
        427:  "mc-addons",  # "addons-thermalexpansion",
        428:  "mc-addons",  # "addons-tinkers-construct",
        429:  "mc-addons",  # "addons-industrialcraft",
        430:  "mc-addons",  # "addons-thaumcraft",
        432:  "mc-addons",  # "addons-buildcraft",
        433:  "mc-addons",  # "addons-forestry",
        4485: "mc-addons",  # "blood-magic",
        4486: "mc-addons",  # "[4486]lucky-blocks",
        4545: "mc-addons",  # "applied-energistics-2",
        4773: "mc-addons",  # "crafttweaker",

        434:  "armor-weapons-tools",
        435:  "server-utility",
        436:  "mc-food",
        4558: "redstone",
        4671: "twitch-integration",
        4906: None,  # "mc-creator",
        4780: None,  # "[4780]fabric",
    }

    ignore_cat = ('mc-addons',
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

    def __init__(self, mod: dict):
        try:
            self.projectid = mod.get('id')
            self.path = mod.get('websiteUrl')
            self.name = mod.get('name')
            self.loader = ModIndex.getLoader(mod)
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
            print('ModIndex __init__:', e)

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
                self.categories = 'without-category'
        except:
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
        except:
            self.update_date = -1

    def setIcon(self):
        try:
            if isinstance(self.icon, list):
                for attach in self.icon:
                    if attach.get('isDefault') is True:
                        self.icon = QByteArray(requests.get(attach.get('thumbnailUrl')).content)
            elif not isinstance(self.icon, QByteArray):
                self.update_date = QByteArray()
        except:
            self.update_date = QByteArray()

    @staticmethod
    def getLoader(mod):
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
                return 'Sin Loader'
        except Exception as e:
            print('ModIndex getLoader:', e)
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

    def check_mod(self, db, valid_loaders):
        try:
            q = QtSql.QSqlQuery(db)
            q.prepare('SELECT M.update_date, M.blocked, M.loader, M.autoinstall, M.autoignore FROM Mods AS M WHERE M.projectid == :projectid')
            q.bindValue(':projectid', self.projectid)

            self.setDate()

            if q.exec():
                if q.next():
                    self.setDate()
                    if q.value(0) < self.update_date:
                        self.update = 1

                    if q.value(1) == 0:
                        self.addlist = int(q.value(2) in valid_loaders)
                        self.autoinstall = q.value(3)
                        self.autoignore = q.value(4)

                else:
                    self.newmod = 1
                    self.addlist = int(self.loader in valid_loaders)

                return True

            else:
                self.error = 1
                QMessageBox.critical(None, "Searching DB Error 1:", q.lastError().text(), QtWidgets.QMessageBox.Close)
                print("Searching DB Error 1:", q.lastError().text())
                return False

        except Exception as e:
            print('SEARCH_THREAD check_mod:', e)

    def process_mod(self, db, modlist=None):
        try:
            if self.error != 1:
                db.transaction()

                q = QtSql.QSqlQuery(db)

                if self.newmod:
                    self.setCategories()
                    self.setIcon()
                    q.prepare('INSERT OR IGNORE INTO Mods(path, name, loader, categories, update_date, icon, projectid) '
                              'VALUES (:path, :name, :loader, :categories, :update_date, :icon, :projectid)')
                    q.bindValue(':path',        self.path)
                    q.bindValue(':name',        self.name)
                    q.bindValue(':loader',      self.loader)
                    q.bindValue(':categories',  self.categories)
                    q.bindValue(':update_date', self.update_date)
                    q.bindValue(':icon',        self.icon)
                    q.bindValue(':projectid',   self.projectid)
                    if not q.exec():
                        print('MOD_INDEX DB NewMod:', q.lastError().text(), self.projectid, self.name)

                if self.update:
                    q.prepare('UPDATE ModsLists SET updated = 1 WHERE mod == :mod;')
                    q.bindValue(':mod', self.projectid)
                    if not q.exec():
                        print('MOD_INDEX DB Update ML:', q.lastError().text(), self.projectid, self.name)

                    q.prepare('UPDATE Mods SET update_date = :update_date WHERE projectid == :projectid;')
                    q.bindValue(':projectid', self.projectid)
                    q.bindValue(':update_date', self.update_date)
                    if not q.exec():
                        print('MOD_INDEX DB Update M:', q.lastError().text(), self.projectid, self.name)

                if self.addlist and modlist is not None:
                    q.prepare('INSERT OR IGNORE INTO ModsLists(list, mod, installed, ignored)' 'VALUES (:list, :mod, :installed, :ignored)')
                    q.bindValue(':list',    modlist)
                    q.bindValue(':mod',     self.projectid)
                    q.bindValue(':installed', self.autoinstall)
                    q.bindValue(':ignored', self.autoignore)
                    if not q.exec():
                        print('MOD_INDEX DB AddList:', q.lastError().text(), self.projectid, self.name)
                elif modlist is None:
                    self.setIcon()
                    q.prepare('UPDATE Mods SET icon = :icon, name = :name, newmod = 1 WHERE projectid == :projectid;')
                    q.bindValue(':projectid', self.projectid)
                    q.bindValue(':icon', self.icon)
                    q.bindValue(':name', self.name)
                    if not q.exec():
                        print('MOD_INDEX DB ReIndex M:', q.lastError().text(), self.projectid, self.name)

                db.commit()
        except Exception as e:
            print('MOD_INDEX process_mod:', e)
            print('     ', self.projectid)
            print('     ', self.path)
            print('     ', self.name)
            print('     ', self.loader)
            print('     ', self.categories)
            print('     ', self.update_date)
            print('     ', self.icon)
            print()
