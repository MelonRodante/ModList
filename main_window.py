import os
import requests

from PyQt5 import QtWidgets, QtCore, QtSql, QtGui

from PyQt5.QtCore import QByteArray, QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QPushButton, QComboBox, QFrame, QToolButton, QAction, QMenu

from database import Database
from pyqt_widgets.customwidgets import CustomQMenu
from pyqt_windows.main_window import Ui_ModList


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_ModList()
        self.ui.setupUi(self)

        self.url = 'https://www.curseforge.com'

        self.categories = ['Bioma',
                           'Estructuras',
                           'Dimensiones',
                           'Mobs',
                           'Decoracion',
                           'Comida',
                           'Herramientas',
                           'Magia',
                           'RPG',
                           'Maquinaria',
                           'Almacenamiento',
                           'Redstone',
                           'Variado',
                           'Transporte',
                           'Basico',
                           'Utilidad',
                           'Utilidad Server',
                           'Addon',
                           'API'
                           ]

        self.bold_font = self.create_bold_font()
        self.cmbModList = self.create_cmd_list()

        Database.connect_db()
        self.setupTestData()

        self.setupWidgets()
        self.setupEvents()

    @staticmethod
    def create_bold_font():
        f = QFont()
        f.setBold(True)
        f.setPixelSize(14)
        return f

    def create_cmd_list(self):
        lbl = QLabel('Lista actual:')
        f = lbl.font()
        f.setBold(True)
        lbl.setFont(f)

        cmbModList = QComboBox()
        cmbModList.setContentsMargins(0, 5, 0, 5)
        cmbModList.setMinimumSize(QtCore.QSize(150, 0))

        m = self.ui.statusbar.contentsMargins()
        m.setLeft(9)
        self.ui.statusbar.setContentsMargins(m)

        self.ui.statusbar.addWidget(lbl)
        self.ui.statusbar.addWidget(cmbModList)

        return cmbModList

    # ------------------------------------------------------------------------------------------------------------------

    def setupWidgets(self):

        self.modify_css()
        self.resize_table()
        self.create_cmb_values_category()
        self.create_cmb_values_lists()
        self.fill_table()

    def modify_css(self):

        f = self.ui.tableMods.horizontalHeader().font()
        f.setBold(True)
        self.ui.tableMods.horizontalHeader().setFont(f)

        f = self.ui.menubar.font()
        f.setBold(True)
        self.ui.menubar.setFont(f)

        self.ui.menubar.setStyleSheet('QMenuBar {'
                                      'background-color: #0F1A25;'
                                      'border-color: #0F1A25; '
                                      'border-bottom-color: #F0651F;}')

        self.ui.statusbar.setStyleSheet('QStatusBar {'
                                        'background-color: #0F1A25; '
                                        'border-color: #0F1A25; '
                                        'border-top-color: #F0651F;}')

    def resize_table(self):
        header = self.ui.tableMods.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)

    def create_cmb_values_lists(self):
        self.cmbModList.clear()
        self.cmbModList.addItem('')

        q = QtSql.QSqlQuery()
        q.prepare('select list from Lists')

        if q.exec_():
            while q.next():
                self.cmbModList.addItem(q.value(0))

    def create_cmb_values_category(self):
        self.ui.cmbCategory.clear()
        self.ui.cmbCategory.addItem('')

        for cat in self.categories:
            self.ui.cmbCategory.addItem(cat)

    # ------------------------------------------------------------------------------------------------------------------

    def setupEvents(self):
        self.cmbModList.currentIndexChanged.connect(self.change_filter)
        self.ui.cmbCategory.currentIndexChanged.connect(self.change_filter)
        self.ui.editName.textChanged.connect(self.change_filter)

    def change_filter(self):
        self.fill_table(self.cmbModList.currentText(), self.ui.cmbCategory.currentText(), self.ui.editName.text().strip())

    # ------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def optional_filter(field, value, tableas='', prefix='', posfix='', like=False):

        value.strip()
        field = field.strip()

        if tableas:
            tableas = tableas.strip() + '.'

        if prefix:
            prefix = ' ' + prefix.strip() + ' '

        if posfix:
            posfix = ' ' + posfix.strip() + ' '

        if value:
            if like:
                return prefix + tableas + field + ' LIKE :' + field + posfix
            else:
                return prefix + tableas + field + ' == :' + field + posfix
        else:
            return prefix + ' True ' + posfix

    def fill_table(self, modlist='', category='', name=''):
        self.ui.tableMods.setRowCount(0)
        q = QtSql.QSqlQuery()

        opcional_filters = self.optional_filter('category', category, prefix='WHERE') + self.optional_filter('name', name, prefix='AND', like=True)

        if modlist:
            obligatory_filter = opcional_filters + self.optional_filter('list', modlist, tableas='ML', prefix='AND')
            q.prepare('SELECT M.icon, M.path, M.name, M.category, M.loader, M.version, M.update_date FROM ModsLists as ML LEFT JOIN Mods as M ON ML.mod = M.path ' +
                      obligatory_filter +
                      ' ORDER BY M.category asc, M.name ASC;')
        else:
            q.prepare('SELECT icon, path, name, category, loader, version, update_date FROM Mods ' +
                      opcional_filters +
                      ' ORDER BY loader desc, category asc, name ASC;')

        q.bindValue(':list', modlist)
        q.bindValue(':category', category)
        q.bindValue(':name', '%' + name + '%')

        if self.exec(q):
            while q.next():
                i = self.ui.tableMods.rowCount()
                self.ui.tableMods.insertRow(i)

                self.ui.tableMods.setCellWidget(i, 0, self.create_table_item_icon_btn(q.value(0), q.value(1)))
                self.ui.tableMods.setItem(i, 1, QtWidgets.QTableWidgetItem('  ' + q.value(2) + '  '))
                self.ui.tableMods.setItem(i, 2, QtWidgets.QTableWidgetItem('  ' + q.value(3) + '  '))
                self.ui.tableMods.setItem(i, 3, QtWidgets.QTableWidgetItem('  ' + q.value(4) + '  '))
                self.ui.tableMods.setItem(i, 4, QtWidgets.QTableWidgetItem('  ' + q.value(5) + '  '))
                self.ui.tableMods.setItem(i, 5, QtWidgets.QTableWidgetItem('  ' + q.value(6) + '  '))

                self.ui.tableMods.item(i, 1).setFont(self.bold_font)

                self.ui.tableMods.item(i, 2).setTextAlignment(QtCore.Qt.AlignCenter)
                self.ui.tableMods.item(i, 3).setTextAlignment(QtCore.Qt.AlignCenter)
                self.ui.tableMods.item(i, 4).setTextAlignment(QtCore.Qt.AlignCenter)
                self.ui.tableMods.item(i, 5).setTextAlignment(QtCore.Qt.AlignCenter)

    def create_table_item_icon_btn(self, image, path):
        p = QtGui.QPixmap()
        p.loadFromData(image)
        btn = QPushButton()
        btn.setIcon(QtGui.QIcon(p))
        btn.setStyleSheet('background-color: rgba(255, 255, 255, 0);')

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

        lists = ['1.17.1', '1.16.6', '1.15.2', '1.14.3', '1.14.1']

        for l in lists:
            q.prepare('insert into Lists(list, search, loader)' 'VALUES (:list, :search, "Forge")')
            q.bindValue(':list', l)
            q.bindValue(':search', 'filter-game-version=2020709689%3A8203')
            self.exec(q)

        for mod in mods:
            icon = requests.get(mod[2]).content

            q.prepare('INSERT INTO Mods(path, name, loader, version, update_date, icon)' 'VALUES (:path, :name, :loader, :version, :update_date, :icon)')
            q.bindValue(':path', mod[0])
            q.bindValue(':name', mod[1])
            q.bindValue(':loader', 'Forge')
            q.bindValue(':version', '1.16')
            q.bindValue(':update_date', '3/12/2020')
            q.bindValue(':icon', QByteArray(icon))
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

