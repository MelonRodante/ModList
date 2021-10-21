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
                self.autoinstall = arg.value(12)
                self.autoignore = arg.value(13)

            else:
                self.loader = arg[0].loader
                self.categories = arg[0].categories
                self.update_date = arg[0].update_date

                self.installed = arg[0].installed
                self.ignored = arg[0].ignored
                self.updated = arg[0].updated

                self.autoinstall = arg[0].autoinstall
                self.autoignore = arg[0].autoignore
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

            if self.autoinstall != mod.autoinstall:
                self.autoinstall = None

            if self.autoignore != mod.autoignore:
                self.autoignore = None

            if self.favorite != mod.favorite:
                self.favorite = None

            if self.blocked != mod.blocked:
                self.blocked = None

    def insert_in_list(self, q, listname):
        q.prepare('INSERT OR IGNORE INTO ModsLists(list, mod, installed, ignored)' 'VALUES (:list, :mod, :installed, :ignored)')
        q.bindValue(':list', listname)
        q.bindValue(':mod', self.projectid)
        q.bindValue(':installed', self.autoinstall)
        q.bindValue(':ignored', self.autoignore)
        if not q.exec():
            print('MOD_INDEX DB AddList:', q.lastError().text(), self.projectid, self.name)