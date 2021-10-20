import os
import sys

from PyQt5 import QtSql, QtWidgets
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QMessageBox

tablelists = '''CREATE TABLE IF NOT EXISTS Lists (
                    listname TEXT NOT NULL,
                    version  TEXT NOT NULL,
                    loader   TEXT NOT NULL DEFAULT 'Sin Loader',
                    PRIMARY KEY(listname));'''

tablemods = '''CREATE TABLE IF NOT EXISTS Mods (
                    projectid       INTEGER NOT NULL, 
                    path            TEXT NOT NULL DEFAULT 'no-path',
                    name	        TEXT NOT NULL DEFAULT 'no-name',
                    categories      TEXT NOT NULL DEFAULT 'without-category',
                    loader	        TEXT NOT NULL DEFAULT 'Sin Loader',
                    update_date     INTEGER NOT NULL,
                    icon	        BLOB,
                    favorite        INTEGER NOT NULL DEFAULT 0,
                    blocked	        INTEGER NOT NULL DEFAULT 0,
                    newmod          INTEGER NOT NULL DEFAULT 1,
                    autoinstall    INTEGER NOT NULL DEFAULT 0,
                    autoignore       INTEGER NOT NULL DEFAULT 0,
                    PRIMARY KEY(projectid));'''

tablemodslists = '''CREATE TABLE IF NOT EXISTS ModsLists (
                    list        TEXT NOT NULL,
                    mod	        INTEGER NOT NULL,
                    installed   INTEGER NOT NULL DEFAULT 0,
                    ignored     INTEGER NOT NULL DEFAULT 0,
                    updated     INTEGER NOT NULL DEFAULT 0,
                    PRIMARY KEY(list, mod),
                    FOREIGN KEY(list) REFERENCES Lists(listname) ON DELETE CASCADE ON UPDATE CASCADE,
                    FOREIGN KEY(mod) REFERENCES Mods(projectid) ON DELETE CASCADE ON UPDATE CASCADE
                    );'''


class Database:
    # filename = os.getenv('LOCALAPPDATA') + '/MelonRodante/ModList/modlist.db'
    # os.makedirs(os.path.dirname(filename), exist_ok=True)
    filename = './modlist.db'

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
            Database.exec(db, 'CREATE INDEX IF NOT EXISTS "OrderMods" ON "Mods" ("favorite"	DESC, "blocked"	ASC, "name"	ASC);')
            Database.exec(db, 'CREATE INDEX IF NOT EXISTS "OrderModsLists" ON "Mods" ("installed" DESC, "updated" DESC, "name" ASC);')

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
