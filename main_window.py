import os
import threading
import time
from typing import Union

import requests

from PyQt5 import QtWidgets, QtCore, QtSql, QtGui
from PyQt5.QtCore import QByteArray, QSize, QThread
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel

from database import Database
from other_windows.admin_list_dialog import AdminListDialog
from other_windows.searching_dialog import SearchingDialog
from pyqt_widgets.customwidgets import CustomButton, Mod
from pyqt_windows.main_window import Ui_ModList


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_ModList()
        self.ui.setupUi(self)

        self.url = 'https://www.curseforge.com'
        self.selectedMod = ''

        self.categories = ['Sin categoria',
                           'Biomas',
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

        Database.connect_db()
        #self.setupTestData()

        self.setupWidgets()
        self.setupEvents()

        self.ui.cmbModList.setCurrentIndex(5)

    @staticmethod
    def create_bold_font():
        try:
            f = QFont()
            f.setBold(True)
            f.setPixelSize(14)
            return f
        except Exception as e:
            print('MAIN_WINDOW create_bold_font: ', str(e))

    # ------------------------------------------------------------------------------------------------------------------

    def setupWidgets(self):
        try:
            self.modify_css()
            self.create_cmb_values_category()
            self.create_cmb_values_lists()
            self.resize_table()
            self.resize_combobox_loader()
            self.fill_table()
        except Exception as e:
            print('MAIN_WINDOW setupWidgets: ', str(e))

    def modify_css(self):
        try:
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

            self.ui.btnSaveConfig.setStyleSheet('QPushButton {border: 1px solid #F0651F; background-color: #0F1A25;} '
                                                'QPushButton:hover {background-color: #19232D;}'
                                                'QPushButton:pressed {background-color: #54687A;}'
                                                'QPushButton:disabled {border: 1px solid #000000;}')
        except Exception as e:
            print('MAIN_WINDOW modify_css: ', str(e))

    def resize_table(self):
        try:
            header = self.ui.tableMods.horizontalHeader()
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
            header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        except Exception as e:
            print('MAIN_WINDOW resize_table: ', str(e))

    def resize_combobox_loader(self):
        try:
            model = self.ui.cmbLoaderConfig.model()
            for i in range(model.rowCount()):
                model.setData(model.index(i, 0), QSize(0, 20), QtCore.Qt.SizeHintRole)
        except Exception as e:
            print('MAIN_WINDOW resize_combobox_loader: ', str(e))

    def create_cmb_values_lists(self):
        try:
            q = QtSql.QSqlQuery()
            q.prepare('select list from Lists')

            self.ui.cmbModList.clear()

            self.ui.cmbModList.addItem('Todos')
            self.ui.cmbModList.insertSeparator(self.ui.cmbModList.count())

            if q.exec_():
                while q.next():
                    self.ui.cmbModList.addItem(q.value(0))

            if self.ui.cmbModList.count() > 2:
                self.ui.cmbModList.insertSeparator(self.ui.cmbModList.count())
            self.ui.cmbModList.addItem('Favoritos')
            self.ui.cmbModList.addItem('Bloqueados')
            self.ui.cmbModList.insertSeparator(self.ui.cmbModList.count())
            self.ui.cmbModList.addItem('Forge')
            self.ui.cmbModList.addItem('Fabric')
            self.ui.cmbModList.addItem('Sin Loader')

            model = self.ui.cmbModList.model()
            for i in range(model.rowCount()):
                model.setData(model.index(i, 0), QSize(0, 20), QtCore.Qt.SizeHintRole)
        except Exception as e:
            print('MAIN_WINDOW create_cmb_values_lists: ', str(e))

    def create_cmb_values_category(self):
        try:
            self.ui.cmbCategory.clear()
            self.ui.cmbCategoryConfig.clear()

            self.ui.cmbCategory.addItem('Todas')
            for cat in self.categories:
                self.ui.cmbCategory.addItem(cat)
                self.ui.cmbCategoryConfig.addItem(cat)

            self.ui.cmbCategory.insertSeparator(2)
            self.ui.cmbCategoryConfig.insertSeparator(1)

            model = self.ui.cmbCategoryConfig.model()
            for i in range(model.rowCount()):
                model.setData(model.index(i, 0), QSize(0, 20), QtCore.Qt.SizeHintRole)

            model = self.ui.cmbCategory.model()
            for i in range(model.rowCount()):
                model.setData(model.index(i, 0), QSize(0, 20), QtCore.Qt.SizeHintRole)
        except Exception as e:
            print('MAIN_WINDOW create_cmb_values_category: ', str(e))

    # ------------------------------------------------------------------------------------------------------------------

    def setupEvents(self):
        try:
            self.ui.btnSaveConfig.clicked.connect(self.save_mod_config)
            self.ui.editNameConfig.textChanged.connect(self.change_edit_name_config)
            self.ui.chkInstalledConfig.clicked.connect(self.change_chk_installed)
            self.ui.chkIgnoredConfig.clicked.connect(self.change_chk_ignored)
            self.ui.chkFavoriteConfig.clicked.connect(self.change_chk_favorite)
            self.ui.chkBlockedConfig.clicked.connect(self.change_chk_blocked)

            self.ui.cmbModList.currentIndexChanged.connect(self.change_cmb_list)
            self.ui.cmbCategory.currentIndexChanged.connect(self.fill_table)
            self.ui.editName.textChanged.connect(self.fill_table)
            self.ui.tableMods.itemSelectionChanged.connect(self.clicked_table)

            self.ui.actionAdminLists.triggered.connect(self.show_admin_list_dialog)
            self.ui.actionSearchingNewMods.triggered.connect(self.show_searching_dialog)

            self.ui.actionShowUpdated.triggered.connect(self.fill_table)
            self.ui.actionShowInstalled.triggered.connect(self.fill_table)
            self.ui.actionShowIgnored.triggered.connect(self.fill_table)
        except Exception as e:
            print('MAIN_WINDOW setupEvents: ', str(e))

    # ---------------------------------------

    def change_cmb_list(self):
        try:
            all_list = 0 < self.ui.cmbModList.currentIndex() < (self.ui.cmbModList.count() - 7)
            self.ui.chkInstalledConfig.setEnabled(all_list)
            self.ui.chkIgnoredConfig.setEnabled(all_list)
            self.ui.chkUpdated.setEnabled(False)
            self.clear_selected()
            self.fill_table()
        except Exception as e:
            print('MAIN_WINDOW change_cmb_list: ', str(e))

    def clicked_table(self):
        try:
            if len(self.ui.tableMods.selectedIndexes()) > 0:

                mod = self.ui.tableMods.indexWidget(self.ui.tableMods.selectedIndexes()[0]).mod

                self.selectedMod = mod.path

                self.ui.editNameConfig.setText(mod.name)
                self.ui.cmbCategoryConfig.setCurrentIndex(self.ui.cmbCategoryConfig.findText(mod.category))
                self.ui.cmbLoaderConfig.setCurrentIndex(self.ui.cmbLoaderConfig.findText(mod.loader))

                self.ui.chkInstalledConfig.setChecked(bool(mod.installed))
                self.ui.chkIgnoredConfig.setChecked(bool(mod.ignored))
                self.ui.chkUpdated.setChecked(not bool(mod.updated))

                self.ui.chkFavoriteConfig.setChecked(bool(mod.favorite))
                self.ui.chkBlockedConfig.setChecked(bool(mod.blocked))

                if 0 < self.ui.cmbModList.currentIndex() < self.ui.cmbModList.count() - 7:
                    self.ui.chkUpdated.setEnabled(bool(mod.updated))

        except Exception as e:
            print('MAIN_WINDOW clicked_table:', e)

    # ---------------------------------------

    def save_mod_config(self):
        try:
            if self.ui.editNameConfig.text():
                q = QtSql.QSqlQuery()
                q.prepare('UPDATE Mods SET  loader = :loader, category = :category, favorite = :favorite, blocked = :blocked WHERE path == :path;')
                q.bindValue(':path', self.selectedMod)
                q.bindValue(':loader', self.ui.cmbLoaderConfig.currentText())
                q.bindValue(':category', self.ui.cmbCategoryConfig.currentText())
                q.bindValue(':favorite', int(self.ui.chkFavoriteConfig.isChecked()))
                q.bindValue(':blocked', int(self.ui.chkBlockedConfig.isChecked()))
                self.exec(q)

                if self.ui.chkBlockedConfig.isChecked():
                    q.prepare('DELETE FROM ModsLists WHERE mod == :mod;')
                    q.bindValue(':list', self.ui.cmbModList.currentText())
                    q.bindValue(':mod', self.selectedMod)
                    self.exec(q)
                elif 0 < self.ui.cmbModList.currentIndex() < self.ui.cmbModList.count() - 7:
                    q.prepare('UPDATE ModsLists SET  installed = :installed, ignored = :ignored, updated = :updated WHERE list == :list AND mod == :mod;')
                    q.bindValue(':list', self.ui.cmbModList.currentText())
                    q.bindValue(':mod', self.selectedMod)
                    q.bindValue(':installed', int(self.ui.chkInstalledConfig.isChecked()))
                    q.bindValue(':ignored', int(self.ui.chkIgnoredConfig.isChecked()))
                    q.bindValue(':updated', int(not self.ui.chkUpdated.isChecked()))
                    self.exec(q)

                self.fill_table()
        except Exception as e:
            print('MAIN_WINDOW save_mod_config: ', str(e))

    def change_edit_name_config(self):
        try:
            if self.ui.editNameConfig.text():
                self.ui.btnSaveConfig.setEnabled(True)
            else:
                self.ui.btnSaveConfig.setEnabled(False)
        except Exception as e:
            print('MAIN_WINDOW change_edit_name_config: ', str(e))

    def change_chk_installed(self):
        try:
            if self.ui.chkInstalledConfig.isChecked():
                if self.ui.chkIgnoredConfig.isChecked():
                    self.ui.chkIgnoredConfig.setChecked(False)
                if self.ui.chkBlockedConfig.isChecked():
                    self.ui.chkBlockedConfig.setChecked(False)
        except Exception as e:
            print('MAIN_WINDOW change_chk_installed: ', str(e))

    def change_chk_ignored(self):
        try:
            if self.ui.chkIgnoredConfig.isChecked():
                if self.ui.chkInstalledConfig.isChecked():
                    self.ui.chkInstalledConfig.setChecked(False)
                if self.ui.chkBlockedConfig.isChecked():
                    self.ui.chkBlockedConfig.setChecked(False)
        except Exception as e:
            print('MAIN_WINDOW change_chk_ignored: ', str(e))

    def change_chk_favorite(self):
        try:
            if self.ui.chkFavoriteConfig.isChecked():
                if self.ui.chkBlockedConfig.isChecked():
                    self.ui.chkBlockedConfig.setChecked(False)
        except Exception as e:
            print('MAIN_WINDOW change_chk_favorite: ', str(e))

    def change_chk_blocked(self):
        try:
            if self.ui.chkBlockedConfig.isChecked():
                if self.ui.chkInstalledConfig.isChecked():
                    self.ui.chkInstalledConfig.setChecked(False)
                if self.ui.chkIgnoredConfig.isChecked():
                    self.ui.chkIgnoredConfig.setChecked(False)
                if self.ui.chkFavoriteConfig.isChecked():
                    self.ui.chkFavoriteConfig.setChecked(False)
        except Exception as e:
            print('MAIN_WINDOW change_chk_blocked: ', str(e))

    # ------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def optional_filter(field, value: Union[str, bool], previus_sql, tableas='', novalue='', like=False):
        try:
            field = field.strip()

            if 'WHERE' not in previus_sql.upper():
                prefix = ' WHERE '
            else:
                prefix = ' AND '

            if tableas:
                tableas = tableas + '.'

            if like:
                condition = ' LIKE :'
            else:
                condition = ' == :'

            if isinstance(value, str) and value.strip() != novalue:
                return prefix + tableas + field + condition + field + ' '
            elif isinstance(value, bool) and value:
                return prefix + tableas + field + condition + field + ' '
            else:
                return ' '
        except Exception as e:
            print('MAIN_WINDOW optional_filter: ', str(e))

    def create_table_item_icon_btn(self, icon, mod):
        try:
            p = QtGui.QPixmap()
            p.loadFromData(icon)
            btn = CustomButton(mod)
            btn.setIcon(QtGui.QIcon(p))
            btn.setStyleSheet('background-color: rgba(255, 255, 255, 0);')

            btn.setMinimumSize(40, 40)
            btn.setMaximumSize(40, 40)
            btn.setIconSize(QSize(36, 36))
            btn.setFlat(True)

            btn.clicked.connect(lambda: os.startfile(self.url + mod.path))

            return btn
        except Exception as e:
            print('MAIN_WINDOW create_table_item_icon_btn: ', str(e))

    @staticmethod
    def create_table_item_lbl(mod):
        try:
            text = ' <b style="text-align: center; font-family: MS Shell Dlg 2; color: #FFFFFF; font-size:15px;"> ' + mod.name + '</b> '

            if mod.installed and mod.favorite:
                icon = ' <img src=:/table_icons/installed_favorite.png>'
            elif mod.installed and not mod.favorite:
                icon = ' <img src=:/table_icons/installed.png>'
            elif mod.ignored and mod.favorite:
                icon = ' <img src=:/table_icons/ignored_favorite.png>'
            elif mod.ignored and not mod.favorite:
                icon = ' <img src=:/table_icons/ignored.png>'
            elif mod.favorite:
                icon = ' <img src=:/table_icons/favorite.png>'
            elif mod.blocked:
                icon = ' <img src=:/table_icons/blocked.png>'
            else:
                icon = ''

            if mod.updated:
                icon = '<img src=:/table_icons/updated.png>' + icon

            lbl = QLabel('<table width=\"100%\"><td width=\"50%\" align=\"left\">' + text + '</td> <td width=\"50%\" align=\"right\">' + icon + '</td></table>')
            lbl.setStyleSheet('background-color: #00000000')

            return lbl
        except Exception as e:
            print('MAIN_WINDOW create_table_item_lbl: ', str(e))

    # ---------------------------------------

    def clear_selected(self):
        try:
            self.selectedMod = ''
            self.ui.editNameConfig.setText('')
            self.ui.cmbCategoryConfig.setCurrentIndex(0)
            self.ui.cmbLoaderConfig.setCurrentIndex(0)
            self.ui.chkInstalledConfig.setChecked(False)
            self.ui.chkIgnoredConfig.setChecked(False)
            self.ui.chkUpdated.setChecked(False)
            self.ui.chkFavoriteConfig.setChecked(False)
            self.ui.chkBlockedConfig.setChecked(False)
        except Exception as e:
            print('MAIN_WINDOW clear_selected: ', str(e))

    def prepare_fill_table_query(self, q):
        try:
            if 0 < self.ui.cmbModList.currentIndex() < self.ui.cmbModList.count() - 7:
                self.prepare_fill_table_query_modslists(q)
            else:
                self.prepare_fill_table_query_mods(q)
        except Exception as e:
            print('MAIN_WINDOW prepare_fill_table_query: ', str(e))

    def prepare_fill_table_query_mods(self, q):
        try:
            loader = self.ui.cmbModList.currentText()
            category = self.ui.cmbCategory.currentText()
            name = self.ui.editName.text()

            opfilter = ''
            opfilter += self.optional_filter('category', category, opfilter, novalue='Todas')
            opfilter += self.optional_filter('name',     name,     opfilter, like=True)

            opfilter += self.optional_filter('favorite', self.ui.cmbModList.currentIndex() == self.ui.cmbModList.count() - 6, opfilter)
            opfilter += self.optional_filter('blocked',  self.ui.cmbModList.currentIndex() == self.ui.cmbModList.count() - 5, opfilter)
            opfilter += self.optional_filter('loader',   self.ui.cmbModList.currentIndex() >= self.ui.cmbModList.count() - 3, opfilter)

            q.prepare('SELECT icon, name, category, loader, update_date, path, 0, 0, 0, favorite, blocked '
                      'FROM Mods'
                      + opfilter +
                      'ORDER BY loader desc, category asc, name ASC;')

            q.bindValue(':category', category)
            q.bindValue(':name', '%' + name + '%')

            q.bindValue(':favorite', 1)
            q.bindValue(':blocked', 1)
            q.bindValue(':loader', loader)
        except Exception as e:
            print('MAIN_WINDOW prepare_fill_table_query_mods: ', str(e))

    def prepare_fill_table_query_modslists(self, q):
        try:
            modlist = self.ui.cmbModList.currentText()
            category = self.ui.cmbCategory.currentText()
            name = self.ui.editName.text()

            opfilter = ''
            opfilter += self.optional_filter('list',     modlist,  opfilter, tableas='ML')
            opfilter += self.optional_filter('category', category, opfilter, tableas='M', novalue='Todas')
            opfilter += self.optional_filter('name',     name,     opfilter, tableas='M', like=True)

            opfilter += self.optional_filter('updated', not self.ui.actionShowUpdated.isChecked(), opfilter, tableas='ML')
            opfilter += self.optional_filter('installed', not self.ui.actionShowInstalled.isChecked(), opfilter, tableas='ML')
            opfilter += self.optional_filter('ignored', not self.ui.actionShowIgnored.isChecked(), opfilter, tableas='ML')


            q.prepare('SELECT M.icon, M.name, M.category, M.loader, M.update_date, M.path, ML.installed, ML.ignored, ML.updated, M.favorite, M.blocked '
                      'FROM ModsLists as ML LEFT JOIN Mods as M ON ML.mod = M.path'
                      + opfilter +
                      'ORDER BY M.category asc, M.name ASC;')

            q.bindValue(':list', modlist)
            q.bindValue(':category', category)
            q.bindValue(':name', '%' + name + '%')

            q.bindValue(':installed', int(self.ui.actionShowInstalled.isChecked()))
            q.bindValue(':ignored', int(self.ui.actionShowIgnored.isChecked()))
        except Exception as e:
            print('MAIN_WINDOW prepare_fill_table_query_modslists: ', str(e))

    def fill_table(self):
        try:
            q = QtSql.QSqlQuery()
            self.prepare_fill_table_query(q)

            self.ui.tableMods.setRowCount(0)

            if self.exec(q):
                while q.next():
                    i = self.ui.tableMods.rowCount()
                    self.ui.tableMods.insertRow(i)

                    mod = Mod(q)
                    self.ui.tableMods.setCellWidget(i, 0, self.create_table_item_icon_btn(q.value(0), mod))
                    self.ui.tableMods.setCellWidget(i, 1, self.create_table_item_lbl(mod))

                    self.ui.tableMods.setItem(i, 2, QtWidgets.QTableWidgetItem('  ' + mod.category + '  '))
                    self.ui.tableMods.setItem(i, 3, QtWidgets.QTableWidgetItem('  ' + mod.loader + '  '))
                    date = time.strftime('%d/%m/%Y', time.localtime(mod.update_date))
                    self.ui.tableMods.setItem(i, 4, QtWidgets.QTableWidgetItem('  ' + date + '  '))

                    self.ui.tableMods.item(i, 2).setTextAlignment(QtCore.Qt.AlignCenter)
                    self.ui.tableMods.item(i, 3).setTextAlignment(QtCore.Qt.AlignCenter)
                    self.ui.tableMods.item(i, 4).setTextAlignment(QtCore.Qt.AlignCenter)
        except Exception as e:
            print('MAIN_WINDOW fill_table: ', str(e))

    # ------------------------------------------------------------------------------------------------------------------

    def show_admin_list_dialog(self):
        try:
            dialog = AdminListDialog()
            code = dialog.exec()

            if code == 1:
                self.create_cmb_values_lists()
        except Exception as e:
            print('MAIN_WINDOW show_admin_list_dialog: ', str(e))

    def show_searching_dialog(self):
        try:
            dialog = SearchingDialog()
            code = dialog.exec()
        except Exception as e:
            print('MAIN_WINDOW show_searching_dialog: ', str(e))

    # ------------------------------------------------------------------------------------------------------------------

    def setupTestData(self):
        mods = [('/minecraft/mc-mods/jei', 'Just Enough Items (JEI)', 'https://media.forgecdn.net/avatars/thumbnails/29/69/64/64/635838945588716414.jpeg'),
                ('/minecraft/mc-mods/journeymap', 'JourneyMap', 'https://media.forgecdn.net/avatars/thumbnails/9/144/64/64/635421614078544069.png'),
                ('/minecraft/mc-mods/appleskin', 'AppleSkin', 'https://media.forgecdn.net/avatars/thumbnails/47/527/64/64/636066936394500688.png'),
                ('/minecraft/mc-mods/biomes-o-plenty', 'Biomes O\' Plenty', 'https://media.forgecdn.net/avatars/thumbnails/419/178/64/64/637645786053192247.png')]

        q = QtSql.QSqlQuery()

        lists = ['1.17.1', '1.16.5', '1.15.2', '1.14.3', '1.14.1']
        loader = ['Forge', 'Forge', 'Fabric', 'Fabric', 'Sin Loader']

        for i in range(len(lists)):
            q.prepare('INSERT INTO Lists(list, search, loader)' 'VALUES (:list, :search, :loader)')
            q.bindValue(':list', lists[i])
            q.bindValue(':search', 'filter-game-version=2020709689%3A8203')
            q.bindValue(':loader', loader[i])
            self.exec(q)

        for mod in mods:
            try:
                icon = requests.get(mod[2]).content

                q.prepare('INSERT INTO Mods(path, name, loader, update_date, icon)' 'VALUES (:path, :name, :loader, :update_date, :icon)')
                q.bindValue(':path', mod[0])
                q.bindValue(':name', mod[1])
                q.bindValue(':loader', 'Forge')
                q.bindValue(':update_date', 1632062031)
                q.bindValue(':icon', QByteArray(icon))
                self.exec(q)

                q.prepare('INSERT INTO ModsLists(list, mod)' 'VALUES (:list, :mod)')
                q.bindValue(':list', '1.16.5')
                q.bindValue(':mod', mod[0])
                self.exec(q)
            except Exception as e:
                print('MAIN_WINDOW setupTestData', e)

    def exec(self, q):
        try:
            b = q.exec_()
            if b is False:
                print(q.lastError().text())
            return b
        except Exception as e:
            print('MAIN_WINDOW modify_css', e)

