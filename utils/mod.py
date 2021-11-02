from PyQt5 import QtSql
from PyQt5.QtSql import QSqlQuery
from utils.icon_utils import IconUtils
from utils.utils import Utils


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
            Utils.print_exception('MOD init' + str(self.projectid), e)

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
            Utils.print_exception('MOD insert_in_list' + str(self.projectid), e)
