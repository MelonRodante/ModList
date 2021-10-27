import os
import sys

from PyQt5 import QtSql, QtWidgets, QtCore
from PyQt5.QtCore import QByteArray
from PyQt5.QtGui import QPixmap
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QMessageBox

from utils.icon_utils import IconUtils

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
                    loader	        TEXT NOT NULL DEFAULT 'No Loader',
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

tablecategories = '''CREATE TABLE IF NOT EXISTS Categories (
                        cat_id	    TEXT NOT NULL,
                        cat_name	TEXT NOT NULL,
                        grp	        INTEGER NOT NULL DEFAULT 0,
                        ord	        INTEGER NOT NULL DEFAULT 0,
                        icon	    BLOB,
                        PRIMARY KEY("cat_id"));'''


class Database:
    # filename = os.getenv('LOCALAPPDATA') + '/MelonRodante/ModList/modlist.db'
    # os.makedirs(os.path.dirname(filename), exist_ok=True)
    filename = './modlist.db'
    db = None

    categories = [
        ['without-category', 'Without Category', 1, 1],
        ['world-gen', 'World Gen', 2, 1],
        ['world-biomes', 'Biomas', 2, 1],
        ['world-ores-resources', 'Ores and Resources', 2, 1],
        ['world-structures', 'Structures', 2, 1],
        ['world-dimensions', 'Dimensiones', 2, 1],
        ['world-mobs', 'Mobs', 2, 1],
        ['technology', 'Technology', 2, 1],
        ['technology-processing', 'Processing', 2, 1],
        ['technology-player-transport', 'Player Transport', 2, 1],
        ['technology-item-fluid-energy-transport', 'I/F/E Transport', 2, 1],
        ['technology-farming', 'Farming', 2, 1],
        ['technology-energy', 'Energy', 2, 1],
        ['technology-genetics', 'Genetics', 2, 1],
        ['technology-automation', 'Automation', 2, 1],
        ['magic', 'Magic', 2, 1],
        ['storage', 'Storage', 2, 1],
        ['library-api', 'API and Library', 2, 1],
        ['adventure-rpg', 'Adventure and RPG', 2, 1],
        ['map-information', 'Map and Information', 2, 1],
        ['cosmetic', 'Cosmetic', 2, 1],
        ['mc-miscellaneous', 'Miscellaneous', 2, 1],
        ['mc-addons', 'Addon', 2, 1],
        ['armor-weapons-tools', 'Armor / Tools / Weapons', 2, 1],
        ['server-utility', 'Server Utility', 2, 1],
        ['mc-food', 'Food', 2, 1],
        ['redstone', 'Redstone', 2, 1],
        ['twitch-integration', 'Twitch Integration', 2, 1]
    ]

    @staticmethod
    def connect_db():
        Database.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        Database.db.setDatabaseName(Database.filename)

        if not Database.db.open():
            QMessageBox.critical(None, "DataBase Error:", Database.db.lastError().databaseText(),
                                 QtWidgets.QMessageBox.Close)
            sys.exit(1)
        else:
            Database.db.exec("PRAGMA foreign_keys = ON;")
            db = QSqlQuery()
            Database.exec(db, tablelists)
            Database.exec(db, tablemods)
            Database.exec(db, tablemodslists)
            Database.exec(db, tablecategories)
            Database.__create_default_categories(db)
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

    @staticmethod
    def __create_default_categories(db):
        q = QtSql.QSqlQuery(db)
        q.prepare('SELECT count(cat_id) FROM Categories WHERE grp <= 100;')

        if Database.execq(q):
            q.next()

            if q.value(0) != len(Database.categories):
                for cat in Database.categories:
                    q.prepare('INSERT OR IGNORE INTO Categories (cat_id, cat_name, grp, ord, icon) VALUES (:cat_id, :cat_name, :grp, :ord, :icon)')
                    q.bindValue(':cat_id', cat[0])
                    q.bindValue(':cat_name', cat[1])
                    q.bindValue(':grp', cat[2])
                    q.bindValue(':ord', cat[3])
                    q.bindValue(':icon', IconUtils.pixmap_to_qbytearray(cat[0]))

                    Database.execq(q)


