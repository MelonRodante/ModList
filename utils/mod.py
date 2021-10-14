from datetime import datetime
from typing import Union

import PyQt5
import requests
from PyQt5 import QtSql
from PyQt5.QtCore import QByteArray, Qt
from qtpy import QtGui


class Mod:
    def __init__(self, arg: Union[QtSql.QSqlQuery, list]):
        try:
            if isinstance(arg, QtSql.QSqlQuery):

                if isinstance(arg.value(0), PyQt5.QtCore.QByteArray):
                    pixmap = QtGui.QPixmap()
                    pixmap.loadFromData(arg.value(0))
                else:
                    pixmap = QtGui.QPixmap(':/widgets/widgets/noicon.png')

                pixmap = pixmap.scaled(32, 32, Qt.KeepAspectRatio)

                self.icon = pixmap
                self.name = arg.value(1)

                # self.categories = arg.value(2)
                cat = arg.value(2).split(',')
                cat.sort()
                self.categories = ",".join(cat)

                self.loader = arg.value(3)
                self.update_date = arg.value(4)
                self.path = arg.value(5)
                self.installed = arg.value(6)
                self.ignored = arg.value(7)
                self.updated = arg.value(8)
                self.favorite = arg.value(9)
                self.blocked = arg.value(10)
                self.projectid = arg.value(11)

            else:
                self.loader = arg[0].loader
                self.categories = arg[0].categories
                self.update_date = arg[0].update_date
                self.installed = arg[0].installed
                self.ignored = arg[0].ignored
                self.updated = arg[0].updated
                self.favorite = arg[0].favorite
                self.blocked = arg[0].blocked
                self.compare_states(arg)
        except Exception as e:
            print('MOD: ', str(e))

    def compare_states(self, mods: list):

        for mod in mods[1:]:
            if self.loader != mod.loader:
                self.loader = None

            if self.categories != mod.categories:
                self.categories = None

            if self.update_date != mod.update_date:
                self.update_date = None

            if self.installed != mod.installed:
                self.installed = None

            if self.ignored != mod.ignored:
                self.ignored = None

            if self.updated != mod.updated:
                self.updated = None

            if self.favorite != mod.favorite:
                self.favorite = None

            if self.blocked != mod.blocked:
                self.blocked = None


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
            self.dependencies = mod.get('latestFiles')

            self.error = 0
            self.newmod = 0
            self.update = 0
            self.addlist = 0

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
            else:
                self.update_date = QByteArray()
        except:
            self.update_date = QByteArray()

    def setDependencies(self):
        try:
            dependencies = set()
            if self.dependencies is not None:
                for file in self.dependencies:
                    if file.get('dependencies') is not None:
                        for dep in file.get('dependencies'):
                            if dep.get('addonId') is not None:
                                dependencies.add(dep.get('addonId'))
            self.dependencies = list(dependencies)
        except Exception as e:
            print('ModIndex setDependencies:', e)
            self.dependencies = []

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
                return 'Forge / Fabric'
            elif forge:
                return 'Forge'
            elif fabric:
                return 'Fabric'
            else:
                return 'Sin Loader'
        except Exception as e:
            print('ModIndex getLoader:', e)
            return 'error'
