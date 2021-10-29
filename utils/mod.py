from datetime import datetime
from typing import Union

import PyQt5
import requests
from PyQt5 import QtSql
from PyQt5.QtCore import QByteArray, Qt
from PyQt5.QtSql import QSqlQuery
from qtpy import QtGui

from utils.icon_utils import IconUtils


class Mod:

    categories = None

    def __init__(self, arg: QtSql.QSqlQuery):
        try:
            self.icon = IconUtils.qbytearray_to_pixmap(arg.value(0), size=64)
            self.name = arg.value(1)

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

        except Exception as e:
            print('MOD init: ', str(e))

    def insert_in_list(self, q: QSqlQuery, listname: str):
        try:
            q.prepare('INSERT OR IGNORE INTO ModsLists(list, mod, installed, ignored)' 'VALUES (:list, :mod, :installed, :ignored)')
            q.bindValue(':list', listname)
            q.bindValue(':mod', self.projectid)
            q.bindValue(':installed', self.autoinstall)
            q.bindValue(':ignored', self.autoignore)
            if not q.exec():
                print('MOD_INDEX DB AddList:', q.lastError().text(), self.projectid, self.name)

        except Exception as e:
            print('MOD insert_in_list: ', str(e))