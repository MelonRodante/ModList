from typing import Union

from PyQt5 import QtSql


class Mod:
    def __init__(self, arg: Union[QtSql.QSqlQuery, list]):

        if isinstance(arg, QtSql.QSqlQuery):
            self.name = arg.value(1)
            self.category = arg.value(2)
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
            self.category = arg[0].category
            self.update_date = arg[0].update_date
            self.installed = arg[0].installed
            self.ignored = arg[0].ignored
            self.updated = arg[0].updated
            self.favorite = arg[0].favorite
            self.blocked = arg[0].blocked
            self.compare_states(arg)


    def compare_states(self, mods: list):

        for mod in mods[1:]:
            if self.loader != mod.loader:
                self.loader = None

            if self.category != mod.category:
                self.category = None

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
