import sys

from PyQt5 import QtSql, QtWidgets
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QMessageBox

tablelists = '''CREATE TABLE IF NOT EXISTS Lists (
                    list    TEXT NOT NULL,
                    filter  TEXT NOT NULL,
                    loader  TEXT NOT NULL DEFAULT 'Sin Loader',
                    PRIMARY KEY(list));'''

tablemods = '''CREATE TABLE IF NOT EXISTS Mods (
                    path        TEXT NOT NULL,
                    name	    TEXT NOT NULL,
                    categories  TEXT NOT NULL DEFAULT 'without-category',
                    loader	    TEXT NOT NULL DEFAULT 'Sin Loader',
                    update_date INT NOT NULL,
                    icon	    BLOB,
                    favorite    INTEGER NOT NULL DEFAULT 0,
                    blocked	    INTEGER NOT NULL DEFAULT 0,
                    PRIMARY KEY(path));'''

tablemodslists = '''CREATE TABLE IF NOT EXISTS ModsLists (
                    list        TEXT NOT NULL,
                    mod	        TEXT NOT NULL,
                    installed   INTEGER NOT NULL DEFAULT 0,
                    ignored     INTEGER NOT NULL DEFAULT 0,
                    updated     INTEGER NOT NULL DEFAULT 0,
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
            QMessageBox.critical(None, "DataBase Error:", db.lastError().databaseText(), QtWidgets.QMessageBox.Close)
            sys.exit(1)
        else:
            db.exec("PRAGMA foreign_keys = ON;")
            db = QSqlQuery()
            Database.exec(db, tablelists)
            Database.exec(db, tablemods)
            Database.exec(db, tablemodslists)

    @staticmethod
    def get_thread_sqlquery():
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE', connectionName='thread')
        db.setDatabaseName(Database.filename)
        if db.open():
            return db
        else:
            QMessageBox.critical(None, "DataBase Error:", db.lastError().databaseText(), QtWidgets.QMessageBox.Close)
            sys.exit(1)


    @staticmethod
    def exec(db, sql):
        if not db.exec(sql):
            print(db.lastError().text())

    @staticmethod
    def execq(q):
        b = q.exec()
        if not b:
            print(q.lastError().text())
        return b
