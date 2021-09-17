import sys

from PyQt5 import QtSql, QtWidgets
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QMessageBox

tablelists = '''CREATE TABLE IF NOT EXISTS Lists (
                    list    TEXT NOT NULL,
                    search  TEXT NOT NULL,
                    loader  TEXT NOT NULL,
                    PRIMARY KEY(list));'''

tablemods = '''CREATE TABLE IF NOT EXISTS Mods (
                    path        TEXT NOT NULL,
                    name	    TEXT NOT NULL,
                    category    TEXT NOT NULL DEFAULT 'Sin categoria',
                    loader	    TEXT NOT NULL DEFAULT 'No especificado',
                    version	    TEXT NOT NULL,
                    update_date TEXT NOT NULL,
                    icon	    BLOB NOT NULL,
                    favorite    INTEGER NOT NULL DEFAULT 0,
                    blocked	    INTEGER NOT NULL DEFAULT 0,
                    PRIMARY KEY(path));'''

tablemodslists = '''CREATE TABLE IF NOT EXISTS ModsLists (
                    list        TEXT NOT NULL,
                    mod	        TEXT NOT NULL,
                    installed   INTEGER NOT NULL DEFAULT 0,
                    ignored     INTEGER NOT NULL DEFAULT 0,
                    PRIMARY KEY(list, mod),
                    FOREIGN KEY(list) REFERENCES Lists(list) ON DELETE CASCADE
                    FOREIGN KEY(mod) REFERENCES Mods(path) ON DELETE CASCADE
                    );'''

class Database:

    filename = 'modlist.db'

    @staticmethod
    def connect_db():
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(Database.filename)

        if not db.open():
            QMessageBox.critical(None, "ModList Error:", "Database Error: %s" % db.lastError().databaseText(), QtWidgets.QMessageBox.Cancel)
            sys.exit(1)
        else:
            db.exec("PRAGMA foreign_keys = ON;")
            db = QSqlQuery()
            Database.exec(db, tablelists)
            Database.exec(db, tablemods)
            Database.exec(db, tablemodslists)

    @staticmethod
    def exec(db, sql):
        if not db.exec(sql):
            print(db.lastError().text())
