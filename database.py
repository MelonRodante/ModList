import sys

from PyQt5 import QtSql, QtWidgets
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QMessageBox

tablemods = '''CREATE TABLE Mods (
                    path	TEXT NOT NULL UNIQUE,
                    name	TEXT NOT NULL,
                    category	TEXT NOT NULL DEFAULT 'unidentified',
                    loader	TEXT NOT NULL DEFAULT 'unidentified',
                    version	TEXT NOT NULL,
                    update_date	TEXT NOT NULL,
                    icon	BLOB NOT NULL,
                    PRIMARY KEY(path));'''

tablelists = '''CREATE TABLE Lists (
                    list  TEXT NOT NULL UNIQUE,
                    search    TEXT NOT NULL,
                    PRIMARY KEY(list));'''

tablemodlists = '''CREATE TABLE ModsLists (
                    list  TEXT NOT NULL,
                    mod	TEXT NOT NULL,
                    PRIMARY KEY(list, mod),
                    FOREIGN KEY(list) REFERENCES Lists(list) ON DELETE CASCADE
                    FOREIGN KEY(mod) REFERENCES Mods(path) ON DELETE CASCADE
                    );'''

tablefavorites = '''CREATE TABLE Favorites (
                        path	TEXT NOT NULL UNIQUE,
                        PRIMARY KEY(path),
                        FOREIGN KEY(path) REFERENCES Mods(path) ON DELETE CASCADE);'''

tableblocked = '''CREATE TABLE Blocked (
                    path	TEXT NOT NULL UNIQUE,
                    PRIMARY KEY(path),
                    FOREIGN KEY(path) REFERENCES Mods(path) ON DELETE CASCADE);'''

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
            db.exec(tablemods)
            db.exec(tablelists)
            db.exec(tablefavorites)
            db.exec(tableblocked)
            db.exec(tablemodlists)