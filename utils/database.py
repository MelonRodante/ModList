import sys

from PyQt5 import QtSql, QtWidgets
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QMessageBox

from utils.icon_utils import IconUtils
from utils.utils import Utils

tablecategories = '''CREATE TABLE IF NOT EXISTS Categories (
                        cat_id	    TEXT NOT NULL,
                        cat_name	TEXT NOT NULL,
                        grp	        INTEGER NOT NULL DEFAULT 0,
                        ord	        INTEGER NOT NULL DEFAULT 0,
                        icon	    BLOB,
                        PRIMARY KEY("cat_id"));'''

tablelists = '''CREATE TABLE IF NOT EXISTS Lists (
                    listname TEXT NOT NULL,
                    version  TEXT NOT NULL,
                    loader   TEXT NOT NULL DEFAULT 'Sin Loader',
                    PRIMARY KEY(listname));'''

tablemods = '''CREATE TABLE IF NOT EXISTS Mods (
                    projectid       INTEGER NOT NULL, 
                    name	        TEXT NOT NULL DEFAULT 'no-name',
                    description	    TEXT NOT NULL DEFAULT '',
                    categories      TEXT NOT NULL DEFAULT '-cc-without-category',
                    loader	        TEXT NOT NULL DEFAULT 'No Loader',
                    update_date     INTEGER NOT NULL,
                    icon	        BLOB,
                    path            TEXT NOT NULL DEFAULT 'no-path',    
                    favorite        INTEGER NOT NULL DEFAULT 0,
                    blocked	        INTEGER NOT NULL DEFAULT 0,
                    autoinstall    INTEGER NOT NULL DEFAULT 0,
                    autoignore       INTEGER NOT NULL DEFAULT 0,
                    newmod          INTEGER NOT NULL DEFAULT 1,
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

tablemodversions = '''CREATE TABLE IF NOT EXISTS ModsVersions (
                        version        TEXT NOT NULL,
                        mod	        INTEGER NOT NULL,
                        PRIMARY KEY(version, mod),
                        FOREIGN KEY(mod) REFERENCES Mods(projectid) ON DELETE CASCADE ON UPDATE CASCADE
                        );'''






class Database:
    # filename = os.getenv('LOCALAPPDATA') + '/MelonRodante/ModList/modlist.db'
    # os.makedirs(os.path.dirname(filename), exist_ok=True)
    filename = './modlist.db'
    db = None

    categories = [
        ['-cc-without-category', 'Without Category', 1, 1],
        ['-cc-world-gen', 'World Gen', 1, 2],
        ['-cc-world-biomes', 'Biomas', 1, 3],
        ['-cc-world-ores-resources', 'Ores and Resources', 1, 4],
        ['-cc-world-structures', 'Structures', 1, 5],
        ['-cc-world-dimensions', 'Dimensiones', 1, 6],
        ['-cc-world-mobs', 'Mobs', 1, 7],
        ['-cc-technology', 'Technology', 1, 8],
        ['-cc-technology-processing', 'Processing', 1, 9],
        ['-cc-technology-player-transport', 'Player Transport', 1, 10],
        ['-cc-technology-item-fluid-energy-transport', 'I/F/E Transport', 1, 11],
        ['-cc-technology-farming', 'Farming', 1, 12],
        ['-cc-technology-energy', 'Energy', 1, 13],
        ['-cc-technology-genetics', 'Genetics', 1, 14],
        ['-cc-technology-automation', 'Automation', 1, 15],
        ['-cc-redstone', 'Redstone', 1, 16],
        ['-cc-storage', 'Storage', 1, 17],
        ['-cc-cosmetic', 'Cosmetic', 1, 18],
        ['-cc-mc-food', 'Food', 1, 19],
        ['-cc-armor-weapons-tools', 'Armor / Tools / Weapons', 1, 20],
        ['-cc-magic', 'Magic', 1, 21],
        ['-cc-adventure-rpg', 'Adventure and RPG', 1, 22],
        ['-cc-map-information', 'Map and Information', 1, 23],
        ['-cc-mc-miscellaneous', 'Miscellaneous', 1, 24],
        ['-cc-server-utility', 'Server Utility', 1, 25],
        ['-cc-mc-addons', 'Addon', 1, 26],
        ['-cc-library-api', 'API and Library', 1, 27],
        ['-cc-vanilla-plus', 'Vanilla +', 1, 28],
        ['-cc-utility-qol', 'Utility & QoL', 1, 23],
        ['-cc-mc-creator', 'MC Creator', 1, 30],
        ['-cc-fabric', 'Fabric', 1, 31],
        ['-cc-twitch-integration', 'Twitch Integration', 1, 32]
    ]

    @staticmethod
    def connect_db():
        try:
            Database.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
            Database.db.setDatabaseName(Database.filename)

            if not Database.db.open():
                QMessageBox.critical(None, "DataBase Error:", Database.db.lastError().databaseText(), QtWidgets.QMessageBox.Close)
                sys.exit(1)
            else:
                Database.db.exec("PRAGMA foreign_keys = ON;")
                db = QSqlQuery()
                Database.exec(db, tablecategories)
                Database.exec(db, tablelists)
                Database.exec(db, tablemods)
                Database.exec(db, tablemodslists)
                Database.exec(db, tablemodversions)
                Database.__create_default_categories(db)
                Database.exec(db, 'CREATE INDEX IF NOT EXISTS "OrderMods" ON "Mods" ("favorite"	DESC, "blocked"	ASC, "name"	ASC);')
                Database.exec(db, 'CREATE INDEX IF NOT EXISTS "OrderModsLists" ON "Mods" ("installed" DESC, "updated" DESC, "name" ASC);')

        except Exception as e:
            Utils.print_exception('DATABASE connect_db', e)

    @staticmethod
    def get_thread_sqlquery():
        try:
            db = QtSql.QSqlDatabase.addDatabase('QSQLITE', connectionName='thread')
            db.setDatabaseName(Database.filename)
            if db.open():
                return db
            else:
                QMessageBox.critical(None, "DataBase Error:", db.lastError().databaseText(), QtWidgets.QMessageBox.Close)
                sys.exit(1)

        except Exception as e:
            Utils.print_exception('DATABASE get_thread_sqlquery', e)

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
        try:
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

        except Exception as e:
            Utils.print_exception('DATABASE __create_default_categories', e)


