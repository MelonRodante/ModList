import os

import requests
from PyQt5 import QtWidgets, QtSql, QtGui, QtCore
from PyQt5.QtCore import QByteArray, QSize
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtWidgets import QLabel, QPushButton

import images_rc

from database import Database
from pyqt_windows.main_window import Ui_ModList


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_ModList()
        self.ui.setupUi(self)

        self.url = 'https://www.curseforge.com'

        self.bold_font = self.create_bold_font()

        Database.connect_db()
        # self.setupTestData()

        self.setupWidgets()
        self.setupEvents()

        self.fill_table('1.16.5')

    def setupWidgets(self):
        self.resize_table()
        self.create_cmb_values_lists()

    def resize_table(self):
        self.ui.tableMods.setIconSize(QSize(32, 32))
        header = self.ui.tableMods.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

    def create_bold_font(self):
        f = QFont()
        f.setBold(True)
        f.setPixelSize(14)
        return f

    def create_cmb_values_lists(self):
        self.ui.cmbModList.clear()
        self.ui.cmbModList.addItem(' ')

        q = QtSql.QSqlQuery()
        q.prepare('select list from Lists')

        if q.exec_():
            while q.next():
                self.ui.cmbModList.addItem(q.value(0))

    # ------------------------------------------------------------------------------------------------------------------

    def setupEvents(self):
        self.ui.cmbModList.currentIndexChanged.connect(self.change_cmb_list)

    def change_cmb_list(self):
        self.fill_table(self.ui.cmbModList.currentText())

    # ------------------------------------------------------------------------------------------------------------------

    def fill_table(self, list):
        self.ui.tableMods.setRowCount(0)

        q = QtSql.QSqlQuery()
        q.prepare('SELECT M.icon, M.name, M.path FROM ModsLists as ML LEFT JOIN Mods as M ON ML.mod = M.path WHERE ML.list == :list ORDER BY M.name asc')
        q.bindValue(':list', list)

        if self.exec(q):
            while q.next():
                i = self.ui.tableMods.rowCount()
                self.ui.tableMods.insertRow(i)
                # self.ui.tableMods.setItem(i, 0, self.create_table_item_icon(q.value(0)))
                self.ui.tableMods.setCellWidget(i, 0, self.create_table_item_icon_btn(q.value(0), q.value(2)))
                self.ui.tableMods.setItem(i, 1, QtWidgets.QTableWidgetItem('  ' + q.value(1) + '  '))
                self.ui.tableMods.setItem(i, 2, QtWidgets.QTableWidgetItem(q.value(2)))

                #self.ui.tableMods.item(i, 0).setTextAlignment(QtCore.Qt.AlignCenter)
                self.ui.tableMods.item(i, 1).setFont(self.bold_font)

    @staticmethod
    def create_table_item_icon(image):
        p = QtGui.QPixmap()
        p.loadFromData(image)
        cell = QtWidgets.QTableWidgetItem()
        cell.setIcon(QtGui.QIcon(p))
        return cell

    def create_table_item_icon_btn(self, image, path):
        p = QtGui.QPixmap()
        p.loadFromData(image)
        btn = QPushButton()
        btn.setIcon(QtGui.QIcon(p))

        btn.setMinimumSize(40, 40)
        btn.setMaximumSize(40, 40)
        btn.setIconSize(QSize(40, 40))
        btn.setFlat(True)

        btn.clicked.connect(lambda: os.startfile(self.url + path))

        return btn


    # ------------------------------------------------------------------------------------------------------------------

    def setupTestData(self):
        mods = [('/minecraft/mc-mods/jei', 'Just Enough Items (JEI)', 'https://media.forgecdn.net/avatars/thumbnails/29/69/64/64/635838945588716414.jpeg'),
                ('/minecraft/mc-mods/journeymap', 'JourneyMap', 'https://media.forgecdn.net/avatars/thumbnails/9/144/64/64/635421614078544069.png'),
                ('/minecraft/mc-mods/appleskin', 'AppleSkin', 'https://media.forgecdn.net/avatars/thumbnails/47/527/64/64/636066936394500688.png'),
                ('/minecraft/mc-mods/biomes-o-plenty', 'Biomes O\' Plenty', 'https://media.forgecdn.net/avatars/thumbnails/419/178/64/64/637645786053192247.png')]

        q = QtSql.QSqlQuery()

        q.prepare('insert into Lists(list, search)' 'VALUES (:list, :search)')
        q.bindValue(':list', '1.16.5')
        q.bindValue(':search', 'filter-game-version=2020709689%3A8203')
        self.exec(q)

        for mod in mods:
            icon = requests.get(mod[2]).content

            a = QByteArray(icon)

            q.prepare('insert into Mods(path, name, loader, version, update_date, icon)' 'VALUES (:path, :name, :loader, :version, :update_date, :icon)')
            q.bindValue(':path', mod[0])
            q.bindValue(':name', mod[1])
            q.bindValue(':loader', 'Forge')
            q.bindValue(':version', '1.16')
            q.bindValue(':update_date', '3/12/2020')
            q.bindValue(':icon', a)
            self.exec(q)

            q.prepare('insert into ModsLists(list, mod)' 'VALUES (:list, :mod)')
            q.bindValue(':list', '1.16.5')
            q.bindValue(':mod', mod[0])
            self.exec(q)

    def exec(self, q):
        b = q.exec_()
        if b is False:
            print(q.lastError().text())
        return b