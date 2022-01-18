import json

import requests
from PyQt5 import QtSql, QtWidgets
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QMessageBox

from utils.curseapilinks import CurseAPI
from utils.icon_utils import IconUtils
from utils.modindex import ModIndex
from utils.utils import Utils
from windows.warning_dialog import WarningDialog


class Mod:

    categories = None

    select_modslist = 'SELECT M.projectid, M.name, M.description, M.categories, M.loader, M.update_date, M.icon, M.path, M.favorite, M.blocked, M.autoinstall, M.autoignore,  ML.installed, ML.ignored, ML.updated '
    select_mods =     'SELECT M.projectid, M.name, M.description, M.categories, M.loader, M.update_date, M.icon, M.path, M.favorite, M.blocked, M.autoinstall, M.autoignore,             0,          0,          0 '

    from_modslist = 'FROM ModsLists as ML LEFT JOIN Mods as M ON ML.mod = M.projectid'
    from_mods =     'FROM Mods as M'

    def __init__(self, arg: QtSql.QSqlQuery):
        try:
            self.projectid = arg.value(0)
            self.name = arg.value(1)
            self.description = arg.value(2)
            self.categories = arg.value(3)
            self.loader = arg.value(4)
            self.update_date = arg.value(5)

            self.icon = IconUtils.qbytearray_to_pixmap(arg.value(6), size=48)
            self.path = arg.value(7)

            self.favorite = arg.value(8)
            self.blocked = arg.value(9)

            self.autoinstall = arg.value(10)
            self.autoignore = arg.value(11)

            self.installed = arg.value(12)
            self.ignored = arg.value(13)
            self.updated = arg.value(14)

        except Exception as e:
            Utils.print_exception('MOD init ' + str(self.projectid), e)

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
            Utils.print_exception('MOD insert_in_list ' + str(self.projectid), e)

    def update_basic_info(self, q: QSqlQuery):
        try:
            try:
                # mod = ModIndex(requests.get(CurseAPI.minecraft_modid + str(self.projectid), headers=CurseAPI.header).json())
                mod = ModIndex(requests.get(CurseAPI.minecraft_modid + str(self.projectid), headers=CurseAPI.header).json().get('data'))
                mod.setIcon()

                q.prepare('UPDATE Mods SET icon = :icon, path = :path, name = :name, description = :description WHERE projectid == :projectid;')
                q.bindValue(':projectid', self.projectid)
                q.bindValue(':icon', mod.icon)
                q.bindValue(':path', mod.path)
                q.bindValue(':name', mod.name)
                q.bindValue(':description', mod.description)

                if not q.exec():
                    print('MOD DB Update:', q.lastError().text(), self.projectid, self.name)

            except json.decoder.JSONDecodeError:
                WarningDialog('API ERROR:\n\nLa consulta a la API no ha regresado ningun valor.', confirmation_dialog=False).exec()

        except Exception as e:
            Utils.print_exception('MOD update_basic_info ' + str(self.projectid), e)

    def delete_from_db(self, q: QSqlQuery):
        try:
            q.prepare('DELETE FROM Mods WHERE projectid == :projectid;')
            q.bindValue(':projectid', self.projectid)

            if not q.exec():
                print('MOD DB Delete:', q.lastError().text(), self.projectid, self.name)

        except Exception as e:
            Utils.print_exception('MOD delete_from_db ' + str(self.projectid), e)