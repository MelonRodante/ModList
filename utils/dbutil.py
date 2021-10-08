from PyQt5 import QtSql

from utils.database import Database


def modify_categories():
    db = QtSql.QSqlDatabase.addDatabase('QSQLITE', connectionName='prueba')
    db.setDatabaseName(Database.filename)
    db.open()
    q = QtSql.QSqlQuery(db)

    mods = []
    q.prepare('SELECT path, categories FROM Mods')
    if q.exec():
        while q.next():
            categories = q.value(1)
            categories = categories.split(',')
            categories = list(set(categories))
            try: categories.remove('mc-creator')
            except Exception: pass
            categories.sort()
            mods.append([q.value(0), ','.join(categories)])
    else:
        print('ERROR 1:' + q.lastError().text())

    i = 0
    q.prepare('INSERT INTO Mods (path, name, categories, loader, update_date, icon, favorite, blocked) '
              'VALUES (?, ?, ?, ?, ?, ?, ?, ?) '
              'ON CONFLICT(path) DO UPDATE SET categories = excluded.categories;')
    for mod in mods:
        q.addBindValue(mod[0])
        q.addBindValue('')
        q.addBindValue(mod[1])
        q.addBindValue('')
        q.addBindValue(0)
        q.addBindValue(None)
        q.addBindValue(0)
        q.addBindValue(0)
        i+=1
        if i % 500 == 0:
            print(i)
        if not q.exec():
            print('ERROR 2:' + q.lastError().text())

    print(q.lastQuery())