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
        self.projectid = mod.get('id')
        self.path = mod.get('websiteUrl')
        self.name = mod.get('name')
        self.loader = mod.get('modLoaders')
        self.categories = mod.get('categories')
        self.update_date = mod.get('dateModified')
        self.icon = mod.get('attachments')

        self.error = 0
        self.newmod = 0
        self.update = 0
        self.addlist = 0
        self.ignore = 0

    def setCategories(self):
        categories = set()
        if isinstance(self.categories, list):
            for cat in self.categories:
                cat = cat.get('slug')
                if cat != 'mc-creator':
                    if cat in ModIndex.ignore_cat:
                        categories.add('mc-addons')
                    else:
                        categories.add(cat)
        categories = list(categories)
        categories.sort()

        if len(categories) > 0:
            self.categories = ','.join(categories)
        else:
            self.categories = 'without-category'

    def setDate(self):
        if isinstance(self.update_date, str):
            try:
                self.update_date = int(datetime.strptime(self.update_date, '%Y-%m-%dT%H:%M:%S.%f%z').timestamp())
            except:
                self.update_date = 0
        else:
            self.update_date = 0

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

    def setLoader(self):
        if isinstance(self.loader, list):
            i = 0
            for loa in self.loader:
                if loa == 'Forge':
                    i+=1
                elif loa == 'Fabric':
                    i+=10

            if i == 0:
                self.loader = 'Sin Loader'
            elif i == 1:
                self.loader = 'Forge'
            elif i == 10:
                self.loader = 'Fabric'
            elif i == 11:
                self.loader = 'Forge / Fabric'

        else:
            self.loader = 'Sin Loader'