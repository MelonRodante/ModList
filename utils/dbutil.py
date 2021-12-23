import json

import requests
from PyQt5 import QtSql, QtWidgets

from utils.curseapilinks import CurseAPI
from utils.database import Database
from utils.icon_utils import IconUtils
from utils.modindex import ModIndex
from utils.utils import Utils


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


def reasign_Category():
    app = QtWidgets.QApplication([])

    db = QtSql.QSqlDatabase.addDatabase('QSQLITE', connectionName='prueba')
    db.setDatabaseName(Database.filename)
    db.open()
    q = QtSql.QSqlQuery(db)

    version = '1.17.1'
    target_category_id = 4906
    target_category_name = '-cc-mc-creator'

    #target_category_id = 4780
    #target_category_name = '-cc-fabric'

    #target_category_id = 5129
    #target_category_name = '-cc-vanilla-plus'

    page = 0
    mods_found = 1
    url = ''
    while mods_found > 0:
        try:
            url = CurseAPI.search_base_query + CurseAPI.search_filter_version + version + CurseAPI.search_offset + str(CurseAPI.pagesize * page) + '&categoryId=' + str(target_category_id)
            mods = requests.get(url, headers=CurseAPI.header).json()

            print('page: ' + str(page))
            for mod in mods:

                projectid = mod.get('id')

                q.prepare('SELECT categories FROM Mods WHERE projectid == :projectid;')
                q.bindValue(':projectid', projectid)

                if q.exec():
                    if q.next():
                        categories = q.value(0).split(',')

                        modified = False
                        for cat in categories:
                            if cat == target_category_name or cat.startswith('-mlc-'):
                                modified = True
                                break

                        if not modified:
                            if len(categories) >= 5:
                                categories = setCategories(projectid, mod.get('categories'))
                            else:
                                categories.append(target_category_name)
                                categories.sort()

                            q.prepare('UPDATE Mods SET categories = :categories WHERE projectid == :projectid;')
                            q.bindValue(':projectid', projectid)
                            q.bindValue(':categories', ",".join(categories))

                            if not q.exec():
                                print(' id:' + str(projectid) + ' | Query Error 2: ' + q.lastError().text())
                else:
                    print(' id:' + str(projectid) + ' | Query Error 1: ' + q.lastError().text())

            page += 1
            mods_found = len(mods)

        except json.decoder.JSONDecodeError:
            print('API ERROR: La consulta a la API no ha regresado ningun valor. | ' + url)
            return 0

    print('FINISH')


def setCategories(projectid, cate):
    try:
        categories = set()
        if isinstance(cate, list):
            for cat in cate:
                cat = ModIndex.cat_id.get(cat.get('categoryId'))
                if cat is not None:
                    categories.add(cat)
        categories = list(categories)
        categories.sort()

        if len(categories) > 0:
            return ','.join(categories)
        else:
            return '-cc-without-category'
    except Exception as e:
        Utils.print_exception('MOD setCategories' + str(projectid), e)
        return 'error'

def search_versions():
    app = QtWidgets.QApplication([])

    db = QtSql.QSqlDatabase.addDatabase('QSQLITE', connectionName='prueba')
    db.setDatabaseName(Database.filename)
    db.open()
    q = QtSql.QSqlQuery(db)

    mods = []
    valid_versions = ('1.16.5', '1.17.1', '1.17', '1.18', '1.18.1')


    q.prepare('SELECT projectid FROM Mods AS M LEFT JOIN ModsVersions AS ML ON M.projectid = ML.mod WHERE ML.mod IS NULL;')
    if q.exec():
        while q.next():
            mods.append(q.value(0))
    else:
        print('ERROR 1:' + q.lastError().text())

    i = 0
    for mod in mods:
        m = requests.get(CurseAPI.minecraft_modid + str(mod), headers=CurseAPI.header).json()
        for file in m.get('gameVersionLatestFiles'):
            if file.get('gameVersion') in valid_versions:
                q.prepare('INSERT OR IGNORE INTO ModsVersions(version, mod)' 'VALUES (:version, :mod)')
                q.bindValue(':version', file.get('gameVersion'))
                q.bindValue(':mod', mod)
                i += 1
                if i % 500 == 0:
                    print(i)
                if not q.exec():
                    print('ERROR 2:' + q.lastError().text() + ' ' + str(mod))



        '''q.prepare('UPDATE Mods SET icon = :icon WHERE projectid == :projectid;')
        q.bindValue(':projectid', mod[0])
        q.bindValue(':icon', IconUtils.pixmap_to_qbytearray(mod[1]))
        i+=1
        if i % 500 == 0:
            print(i)
        if not q.exec():
            print('ERROR 2:' + q.lastError().text() + ' ' + str(mod[0]))'''


def copy_versions():
    app = QtWidgets.QApplication([])

    db = QtSql.QSqlDatabase.addDatabase('QSQLITE', connectionName='prueba')
    db.setDatabaseName(Database.filename)
    db.open()
    q = QtSql.QSqlQuery(db)

    mods = []

    q.prepare("select ml.mod, ml.installed, ml.ignored from modslists as ml where list == 'Forge 1.18.1' and mod in (select mod from modslists where list == 'Forge 1.18.1 Simple');")
    if q.exec():
        while q.next():
            mods.append([q.value(0), q.value(1), q.value(2)])
    else:
        print('ERROR 1:' + q.lastError().text())

    i = 0
    for mod in mods:
        q.prepare("UPDATE Modslists SET installed = :installed, ignored = :ignored WHERE mod == :mod and list == 'Forge 1.18.1 Simple';")
        q.bindValue(':mod', mod[0])
        q.bindValue(':installed', mod[1])
        q.bindValue(':ignored', mod[2])

        i += 1
        if i % 10 == 0:
            print(i)
        if not q.exec():
            print('ERROR 2:' + q.lastError().text() + ' ' + str(mod))



# INSERT INTO ModsVersions(version, mod) SELECT "1.18.1", M.projectid FROM Mods AS M INNER JOIN ModsLists AS ML ON M.projectid = ML.mod WHERE ML.list == "Forge 1.18.1";