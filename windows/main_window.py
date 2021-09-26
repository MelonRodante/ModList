import time
import requests
from typing import Union

from PyQt5 import QtWidgets, QtCore, QtSql
from PyQt5.QtCore import QByteArray, QSize, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QAbstractItemView

from database import Database
from mod import Mod
from pyqt_widgets.labelbutton import ButtonLabel
from pyqt_widgets.delegates import TableStyleItemDelegate
from pyqt_widgets.labelicons import LabelWithIcons
from pyqt_windows.main_window import Ui_ModList
from windows.admin_list_dialog import AdminListDialog
from windows.searching_dialog import SearchingDialog


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_ModList()
        self.ui.setupUi(self)

        self.selectedMods = []

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

            self.ui.tableMods.setMouseTracking(True)
            self.ui.tableMods.setItemDelegate(TableStyleItemDelegate(self.ui.tableMods))

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
                model.setData(model.index(i, 0), QSize(0, 20), Qt.SizeHintRole)
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
                model.setData(model.index(i, 0), QSize(0, 20), Qt.SizeHintRole)
        except Exception as e:
            print('MAIN_WINDOW create_cmb_values_lists: ', str(e))

    def create_cmb_values_category(self):
        try:
            self.ui.cmbCategory.clear()
            self.ui.cmbCategoryConfig.clear()

            self.ui.cmbCategory.addItem('Todas')
            self.ui.cmbCategoryConfig.addItem('')
            for cat in self.categories:
                self.ui.cmbCategory.addItem(cat)
                self.ui.cmbCategoryConfig.addItem(cat)

            self.ui.cmbCategory.insertSeparator(2)
            self.ui.cmbCategoryConfig.insertSeparator(2)

            model = self.ui.cmbCategoryConfig.model()
            for i in range(model.rowCount()):
                model.setData(model.index(i, 0), QSize(0, 20), Qt.SizeHintRole)

            model = self.ui.cmbCategory.model()
            for i in range(model.rowCount()):
                model.setData(model.index(i, 0), QSize(0, 20), Qt.SizeHintRole)
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

            self.ui.actionMultiselection.triggered.connect(self.action_table_multiselection)

            self.ui.actionShowUpdated.triggered.connect(lambda: self.change_action_chk_show(self.ui.actionShowUpdated))
            self.ui.actionShowInstalled.triggered.connect(lambda: self.change_action_chk_show(self.ui.actionShowInstalled))
            self.ui.actionShowIgnored.triggered.connect(lambda: self.change_action_chk_show(self.ui.actionShowIgnored))
        except Exception as e:
            print('MAIN_WINDOW setupEvents: ', str(e))

    def action_table_multiselection(self):
        if self.ui.actionMultiselection.isChecked():
            self.ui.tableMods.setSelectionMode(QAbstractItemView.ExtendedSelection)
        else:
            self.ui.tableMods.setSelectionMode(QAbstractItemView.SingleSelection)

    def change_cmb_list(self):
        try:
            self.fill_table()

            islist = self.is_list()
            self.ui.actionShowUpdated.setEnabled(islist)
            self.ui.actionShowInstalled.setEnabled(islist)
            self.ui.actionShowIgnored.setEnabled(islist)
            self.ui.actionShowNoFindFavorites.setEnabled(islist)

        except Exception as e:
            print('MAIN_WINDOW change_cmb_list: ', str(e))

    def clicked_table(self):
        try:
            self.selectedMods = []

            if len(self.ui.tableMods.selectedIndexes()) > 0:

                self.ui.editNameConfig.setEnabled(True)
                self.ui.cmbLoaderConfig.setEnabled(True)
                self.ui.cmbCategoryConfig.setEnabled(True)
                self.ui.chkFavoriteConfig.setEnabled(True)
                self.ui.chkBlockedConfig.setEnabled(True)

                islist = self.is_list()
                self.ui.chkInstalledConfig.setTristate(False)
                self.ui.chkIgnoredConfig.setTristate(False)
                self.ui.chkUpdated.setTristate(False)
                self.ui.chkInstalledConfig.setEnabled(islist)
                self.ui.chkIgnoredConfig.setEnabled(islist)
                self.ui.chkUpdated.setEnabled(islist)

                self.ui.chkFavoriteConfig.setTristate(False)
                self.ui.chkBlockedConfig.setTristate(False)

                if len(self.ui.tableMods.selectedIndexes()) == 5:
                    mod = self.ui.tableMods.indexWidget(self.ui.tableMods.selectedIndexes()[0]).mod

                    self.selectedMods.append(mod)
                    self.ui.editNameConfig.setText(mod.name)
                    self.ui.cmbCategoryConfig.setCurrentIndex(self.ui.cmbCategoryConfig.findText(mod.category))
                    self.ui.cmbLoaderConfig.setCurrentIndex(self.ui.cmbLoaderConfig.findText(mod.loader))

                    if islist:
                        self.ui.chkInstalledConfig.setChecked(bool(mod.installed))
                        self.ui.chkIgnoredConfig.setChecked(bool(mod.ignored))

                        self.ui.chkUpdated.setEnabled(bool(mod.updated))
                        self.ui.chkUpdated.setChecked(not bool(mod.updated))
                    else:
                        self.ui.chkInstalledConfig.setChecked(False)
                        self.ui.chkIgnoredConfig.setChecked(False)
                        self.ui.chkUpdated.setChecked(False)

                    self.ui.chkFavoriteConfig.setChecked(bool(mod.favorite))
                    self.ui.chkBlockedConfig.setChecked(bool(mod.blocked))

                else:
                    for r in self.ui.tableMods.selectedRanges():
                        for i in range(r.topRow(), r.bottomRow()+1):
                            self.selectedMods.append(self.ui.tableMods.cellWidget(i, 0).mod)

                    state = Mod(self.selectedMods)

                    self.ui.editNameConfig.setText(' - VARIOS - ')

                    if state.loader is not None:
                        self.ui.cmbLoaderConfig.setCurrentIndex(self.ui.cmbLoaderConfig.findText(state.loader))
                    else:
                        self.ui.cmbLoaderConfig.setCurrentIndex(0)

                    if state.category is not None:
                        self.ui.cmbCategoryConfig.setCurrentIndex(self.ui.cmbCategoryConfig.findText(state.category))
                    else:
                        self.ui.cmbCategoryConfig.setCurrentIndex(0)

                    if islist:
                        if state.installed is not None:
                            self.ui.chkInstalledConfig.setChecked(bool(state.installed))
                        else:
                            self.ui.chkInstalledConfig.setTristate(True)
                            self.ui.chkInstalledConfig.setCheckState(Qt.PartiallyChecked)

                        if state.ignored is not None:
                            self.ui.chkIgnoredConfig.setChecked(bool(state.ignored))
                        else:
                            self.ui.chkIgnoredConfig.setTristate(True)
                            self.ui.chkIgnoredConfig.setCheckState(Qt.PartiallyChecked)

                        if state.updated is not None:
                            self.ui.chkUpdated.setEnabled(bool(state.updated))
                            self.ui.chkUpdated.setChecked(not bool(state.updated))
                        else:
                            self.ui.chkUpdated.setTristate(True)
                            self.ui.chkUpdated.setCheckState(Qt.PartiallyChecked)
                    else:
                        self.ui.chkInstalledConfig.setChecked(False)
                        self.ui.chkIgnoredConfig.setChecked(False)
                        self.ui.chkUpdated.setChecked(False)


                    if state.favorite is not None:
                        self.ui.chkFavoriteConfig.setChecked(bool(state.favorite))
                    else:
                        self.ui.chkFavoriteConfig.setTristate(True)
                        self.ui.chkFavoriteConfig.setCheckState(Qt.PartiallyChecked)
                        print(self.ui.chkFavoriteConfig.checkState())

                    if state.blocked is not None:
                        self.ui.chkBlockedConfig.setChecked(bool(state.blocked))
                    else:
                        self.ui.chkBlockedConfig.setTristate(True)
                        self.ui.chkBlockedConfig.setCheckState(Qt.PartiallyChecked)
            else:
                self.ui.editNameConfig.setEnabled(False)
                self.ui.cmbLoaderConfig.setEnabled(False)
                self.ui.cmbCategoryConfig.setEnabled(False)
                self.ui.chkFavoriteConfig.setEnabled(False)
                self.ui.chkBlockedConfig.setEnabled(False)
                self.ui.chkInstalledConfig.setEnabled(False)
                self.ui.chkIgnoredConfig.setEnabled(False)
                self.ui.chkUpdated.setEnabled(False)

        except Exception as e:
            print('MAIN_WINDOW clicked_table:', e)

    def save_mod_config(self):
        try:
            if len(self.selectedMods) > 0:
                q = QtSql.QSqlQuery()

                for mod in self.selectedMods:
                    q.prepare('UPDATE Mods SET  loader = :loader, category = :category, favorite = :favorite, blocked = :blocked WHERE path == :path;')
                    q.bindValue(':path', mod.path)

                    if self.ui.cmbLoaderConfig.currentIndex() != 0:
                        q.bindValue(':loader', self.ui.cmbLoaderConfig.currentText())
                    else:
                        q.bindValue(':loader', mod.loader)

                    if self.ui.cmbCategoryConfig.currentIndex() != 0:
                        q.bindValue(':category', self.ui.cmbCategoryConfig.currentText())
                    else:
                        q.bindValue(':category', mod.category)

                    if self.ui.chkFavoriteConfig.checkState() != Qt.PartiallyChecked:
                        q.bindValue(':favorite', int(self.ui.chkFavoriteConfig.isChecked()))
                    else:
                        q.bindValue(':favorite', mod.favorite)

                    if self.ui.chkBlockedConfig.checkState() != Qt.PartiallyChecked:
                        q.bindValue(':blocked', int(self.ui.chkBlockedConfig.isChecked()))
                    else:
                        q.bindValue(':blocked', mod.blocked)

                    self.exec(q)

                    if self.ui.chkBlockedConfig.checkState() == Qt.Checked:
                        q.prepare('DELETE FROM ModsLists WHERE mod == :mod;')
                        q.bindValue(':mod', mod.path)
                        self.exec(q)
                    elif self.is_list():
                        q.prepare('UPDATE ModsLists SET  installed = :installed, ignored = :ignored, updated = :updated WHERE list == :list AND mod == :mod;')
                        q.bindValue(':list', self.ui.cmbModList.currentText())

                        q.bindValue(':mod', mod.path)

                        if self.ui.chkInstalledConfig.checkState() != Qt.PartiallyChecked:
                            q.bindValue(':installed', int(self.ui.chkInstalledConfig.isChecked()))
                        else:
                            q.bindValue(':installed', mod.installed)

                        if self.ui.chkIgnoredConfig.checkState() != Qt.PartiallyChecked:
                            q.bindValue(':ignored', int(self.ui.chkIgnoredConfig.isChecked()))
                        else:
                            q.bindValue(':ignored', mod.ignored)

                        if self.ui.chkUpdated.checkState() != Qt.PartiallyChecked and mod.updated == 1:
                            q.bindValue(':updated', int(not self.ui.chkUpdated.isChecked()))
                        else:
                            q.bindValue(':updated', mod.updated)

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
            if self.ui.chkInstalledConfig.checkState() == Qt.Checked:
                if self.ui.chkIgnoredConfig.isChecked():
                    self.ui.chkIgnoredConfig.setChecked(False)
                if self.ui.chkBlockedConfig.isChecked():
                    self.ui.chkBlockedConfig.setChecked(False)
        except Exception as e:
            print('MAIN_WINDOW change_chk_installed: ', str(e))

    def change_chk_ignored(self):
        try:
            if self.ui.chkIgnoredConfig.checkState() == Qt.Checked:
                if self.ui.chkInstalledConfig.isChecked():
                    self.ui.chkInstalledConfig.setChecked(False)
                if self.ui.chkBlockedConfig.isChecked():
                    self.ui.chkBlockedConfig.setChecked(False)
        except Exception as e:
            print('MAIN_WINDOW change_chk_ignored: ', str(e))

    def change_chk_favorite(self):
        try:
            if self.ui.chkFavoriteConfig.checkState() == Qt.Checked:
                if self.ui.chkBlockedConfig.isChecked():
                    self.ui.chkBlockedConfig.setChecked(False)
        except Exception as e:
            print('MAIN_WINDOW change_chk_favorite: ', str(e))

    def change_chk_blocked(self):
        try:
            if self.ui.chkBlockedConfig.checkState() == Qt.Checked:
                if self.ui.chkInstalledConfig.isChecked():
                    self.ui.chkInstalledConfig.setChecked(False)
                if self.ui.chkIgnoredConfig.isChecked():
                    self.ui.chkIgnoredConfig.setChecked(False)
                if self.ui.chkFavoriteConfig.isChecked():
                    self.ui.chkFavoriteConfig.setChecked(False)
        except Exception as e:
            print('MAIN_WINDOW change_chk_blocked: ', str(e))

    def change_action_chk_show(self, action):
        if self.ui.actionShowUpdated != action:
            self.ui.actionShowUpdated.setChecked(False)

        if self.ui.actionShowInstalled != action:
            self.ui.actionShowInstalled.setChecked(False)

        if self.ui.actionShowIgnored != action:
            self.ui.actionShowIgnored.setChecked(False)

        self.fill_table()

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


            if self.ui.actionShowUpdated.isChecked():
                opfilter += ' AND installed == 0 AND ignored == 0 OR installed == 1 AND updated == 1 '
            elif self.ui.actionShowInstalled.isChecked():
                opfilter += ' AND installed == 1 '
            elif self.ui.actionShowIgnored.isChecked():
                opfilter += ' AND ignored == 1 '
            else:
                opfilter += ' AND installed == 0 AND ignored == 0 '

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
    def prepare_fill_table_query_modslists(self, q):
        try:
            modlist = self.ui.cmbModList.currentText()
            category = self.ui.cmbCategory.currentText()
            name = self.ui.editName.text()

            opfilter = ''
            opfilter += self.optional_filter('list',     modlist,  opfilter, tableas='ML')
            opfilter += self.optional_filter('category', category, opfilter, tableas='M', novalue='Todas')
            opfilter += self.optional_filter('name',     name,     opfilter, tableas='M', like=True)


            if self.ui.actionShowUpdated.isChecked():
                opfilter += ' AND installed == 0 AND ignored == 0 OR installed == 1 AND updated == 1 '
            elif self.ui.actionShowInstalled.isChecked():
                opfilter += ' AND installed == 1 '
            elif self.ui.actionShowIgnored.isChecked():
                opfilter += ' AND ignored == 1 '
            else:
                opfilter += ' AND installed == 0 AND ignored == 0 '

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
            self.clear_selected()

            q = QtSql.QSqlQuery()
            self.prepare_fill_table_query(q)

            self.ui.tableMods.setRowCount(0)

            if self.exec(q):
                while q.next():
                    i = self.ui.tableMods.rowCount()
                    self.ui.tableMods.insertRow(i)

                    mod = Mod(q)

                    self.ui.tableMods.setCellWidget(i, 0, ButtonLabel(q.value(0), mod))
                    self.ui.tableMods.setCellWidget(i, 1, LabelWithIcons(mod))

                    self.ui.tableMods.setItem(i, 2, QtWidgets.QTableWidgetItem('  ' + mod.category + '  '))
                    self.ui.tableMods.setItem(i, 3, QtWidgets.QTableWidgetItem('  ' + mod.loader + '  '))
                    date = time.strftime('%d/%m/%Y', time.localtime(mod.update_date))
                    self.ui.tableMods.setItem(i, 4, QtWidgets.QTableWidgetItem('  ' + date + '  '))

                    self.ui.tableMods.item(i, 2).setTextAlignment(QtCore.Qt.AlignCenter)
                    self.ui.tableMods.item(i, 3).setTextAlignment(QtCore.Qt.AlignCenter)
                    self.ui.tableMods.item(i, 4).setTextAlignment(QtCore.Qt.AlignCenter)

        except Exception as e:
            print('MAIN_WINDOW fill_table: ', str(e))

    def clear_selected(self):
        try:
            self.selectedMods = []
            self.ui.editNameConfig.setText('')
            self.ui.cmbCategoryConfig.setCurrentIndex(0)
            self.ui.cmbLoaderConfig.setCurrentIndex(0)
            self.ui.chkInstalledConfig.setChecked(False)
            self.ui.chkIgnoredConfig.setChecked(False)
            self.ui.chkUpdated.setChecked(False)
            self.ui.chkFavoriteConfig.setChecked(False)
            self.ui.chkBlockedConfig.setChecked(False)

            self.ui.btnSaveConfig.setEnabled(False)
            self.ui.editNameConfig.setEnabled(False)
            self.ui.cmbLoaderConfig.setEnabled(False)
            self.ui.cmbCategoryConfig.setEnabled(False)
            self.ui.chkInstalledConfig.setEnabled(False)
            self.ui.chkIgnoredConfig.setEnabled(False)
            self.ui.chkUpdated.setEnabled(False)
            self.ui.chkFavoriteConfig.setEnabled(False)
            self.ui.chkBlockedConfig.setEnabled(False)
        except Exception as e:
            print('MAIN_WINDOW clear_selected: ', str(e))

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

    def is_list(self):
        return 1 < self.ui.cmbModList.currentIndex() < self.ui.cmbModList.count()-7

    def exec(self, q):
        try:
            b = q.exec_()
            if b is False:
                print(q.lastError().text())
            return b
        except Exception as e:
            print('MAIN_WINDOW exec', e)

    '''def setupTestData(self):
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
            q.bindValue(':filter', 'filter-game-version=2020709689%3A8203')
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
                print('MAIN_WINDOW setupTestData', e)'''


