import requests
from PyQt5 import QtSql, QtWidgets

from utils.curseapilinks import CurseAPI
from utils.database import Database
from utils.icon_utils import IconUtils


def modify_categories():
    db = QtSql.QSqlDatabase.addDatabase('QSQLITE', connectionName='prueba')
    db.setDatabaseName(Database.filename)
    db.open()
    q = QtSql.QSqlQuery(db)

    mods = []
    q.prepare('SELECT projectid, categories FROM Mods;')
    if q.exec():
        while q.next():
            categories = q.value(1)
            categories = categories.split(',')
            newcats = []
            for cat in categories:
                if not cat.startswith('-mlc-') and not cat.startswith('-cc-'):
                    cat = '-cc-' + cat
                    newcats.append(cat)
                else:
                    newcats.append(cat)

            newcats.sort()
            mods.append([q.value(0), ','.join(newcats)])
    else:
        print('ERROR 1:' + q.lastError().text())

    i = 0
    for mod in mods:
        q.prepare('UPDATE Mods SET categories = :categories WHERE projectid == :projectid;')
        q.bindValue(':projectid', mod[0])
        q.bindValue(':categories', mod[1])
        i+=1
        if i % 500 == 0:
            print(i)
        if not q.exec():
            print('ERROR 2:' + q.lastError().text() + ' ' + str(mod[0]))


def add_description():
    db = QtSql.QSqlDatabase.addDatabase('QSQLITE', connectionName='prueba')
    db.setDatabaseName(Database.filename)
    db.open()
    q = QtSql.QSqlQuery(db)

    mods = []
    q.prepare('SELECT projectid, description FROM Mods;')
    if q.exec():
        while q.next():
            if not q.value(1):
                mods.append(q.value(0))
    else:
        print('ERROR 1:' + q.lastError().text())

    i = 0
    for mod in mods:
        modjson = requests.get(CurseAPI.minecraft_modid + str(mod), headers=CurseAPI.header).json()
        q.prepare('UPDATE Mods SET description = :description WHERE projectid == :projectid;')
        q.bindValue(':projectid', mod)
        q.bindValue(':description', modjson.get('summary'))
        i+=1
        if i % 500 == 0:
            print(i)
        if not q.exec():
            print('ERROR 2:' + q.lastError().text() + ' ' + str(mod))


def resize_icons():
    app = QtWidgets.QApplication([])

    db = QtSql.QSqlDatabase.addDatabase('QSQLITE', connectionName='prueba')
    db.setDatabaseName(Database.filename)
    db.open()
    q = QtSql.QSqlQuery(db)

    mods = []
    q.prepare('SELECT projectid, icon FROM Mods;')
    if q.exec():
        while q.next():
            mods.append([q.value(0), IconUtils.qbytearray_to_pixmap(q.value(1), size=48)])
    else:
        print('ERROR 1:' + q.lastError().text())

    i = 0
    for mod in mods:
        q.prepare('UPDATE Mods SET icon = :icon WHERE projectid == :projectid;')
        q.bindValue(':projectid', mod[0])
        q.bindValue(':icon', IconUtils.pixmap_to_qbytearray(mod[1]))
        i+=1
        if i % 500 == 0:
            print(i)
        if not q.exec():
            print('ERROR 2:' + q.lastError().text() + ' ' + str(mod[0]))
