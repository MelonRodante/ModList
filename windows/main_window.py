
import math
import time

from typing import Union

from PyQt5 import QtWidgets, QtCore, QtSql
from PyQt5.QtCore import QSize, Qt, QCoreApplication
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QAbstractItemView

from database import Database
from mod import Mod
from pyqt_style import css
from pyqt_style.colors import ColorStrong, DarkBackground, Border
from pyqt_widgets.delegates import TableStyleItemDelegate
from pyqt_windows.main_window import Ui_ModList
from windows.admin_list_dialog import AdminListDialog
from windows.searching_dialog import SearchingDialog


class MainWindow(QtWidgets.QMainWindow):

    rows_per_page = 5000

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_ModList()
        self.ui.setupUi(self)

        self.bold_font = self.create_bold_font()

        self.categories = ['Sin categoria',
                           '-',
                           'Mecanica simple',
                           'Elemento simple',
                           'Utilidad Server',
                           'Crafteos',
                           'Variado',
                           '-',
                           'Herramientas',
                           'Comida',
                           'Encantamientos',
                           'Decoracion',
                           '-',
                           'Maquinaria',
                           'Almacenamiento',
                           'Redstone',
                           'Transporte',
                           'Magia',
                           'RPG',
                           '-',
                           'Mobs',
                           'Biomas',
                           'Estructuras',
                           'Dimensiones',
                           'Ores',
                           '-',
                           'API',
                           'Addon',
                           'Optimizacion',
                           '-',
                           'Client',
                           'Keybinding',
                           'Menu']
        self.showlist_state = (self.ui.actionShowUpdated, self.ui.actionShowInstalled, self.ui.actionShowIgnored)
        self.showlist_loader = (self.ui.actionWithoutLoader, self.ui.actionForgeLoader, self.ui.actionFabricLoader, self.ui.actionBothLoader)

        self.current_page = 0
        self.maxpages = 0
        self.found_results = 0
        self.tableMods = []

        self.selectedMods = []

        Database.connect_db()

        self.setupWidgets()
        self.setupEvents()

        self.load_pages()
        self.show()

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
        except Exception as e:
            print('MAIN_WINDOW setupWidgets: ', str(e))

    def modify_css(self):
        try:
            self.setStyleSheet(css.style)

            f = self.ui.tableMods.horizontalHeader().font()
            f.setBold(True)
            self.ui.tableMods.horizontalHeader().setFont(f)

            f = self.ui.menubar.font()
            f.setBold(True)
            self.ui.menubar.setFont(f)

            self.ui.tableMods.setMouseTracking(True)
            self.ui.tableMods.setItemDelegate(TableStyleItemDelegate(self.ui.tableMods))

            self.ui.lblActualPages.setStyleSheet('QLabel {border: 1px solid ' + ColorStrong + '; background-color: ' + DarkBackground + ';} ' + 'QLabel:disabled {border: 1px solid ' + Border + '; color: ' + Border + ';}')

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
                if cat == '-':
                    self.ui.cmbCategory.insertSeparator(self.ui.cmbCategory.count())
                    self.ui.cmbCategoryConfig.insertSeparator(self.ui.cmbCategoryConfig.count())
                else:
                    self.ui.cmbCategory.addItem(cat)
                    self.ui.cmbCategoryConfig.addItem(cat)

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

            self.ui.cmbModList.currentIndexChanged.connect(self.change_cmb_list)
            self.ui.cmbCategory.currentIndexChanged.connect(self.filter_change)
            self.ui.editName.returnPressed.connect(self.filter_change)
            self.ui.editName.textEdited.connect(self.edit_name_clear)

            self.ui.tableMods.itemSelectionChanged.connect(self.clicked_table)
            self.ui.btnPageLeft.clicked.connect(self.left_page)
            self.ui.btnPageRight.clicked.connect(self.right_page)

            self.ui.btnSaveConfig.clicked.connect(self.save_mod_config)
            self.ui.editNameConfig.textChanged.connect(self.change_edit_name_config)
            self.ui.chkInstalledConfig.clicked.connect(self.change_chk_installed)
            self.ui.chkIgnoredConfig.clicked.connect(self.change_chk_ignored)
            self.ui.chkFavoriteConfig.clicked.connect(self.change_chk_favorite)
            self.ui.chkBlockedConfig.clicked.connect(self.change_chk_blocked)

            self.ui.actionAdminLists.triggered.connect(self.show_admin_list_dialog)
            self.ui.actionSearchingNewMods.triggered.connect(self.show_searching_dialog)
            self.ui.actionMultiselection.triggered.connect(self.action_table_multiselection)

            self.ui.actionShowUpdated.triggered.connect(lambda: self.change_action_chk_show_state(self.ui.actionShowUpdated))
            self.ui.actionShowInstalled.triggered.connect(lambda: self.change_action_chk_show_state(self.ui.actionShowInstalled))
            self.ui.actionShowIgnored.triggered.connect(lambda: self.change_action_chk_show_state(self.ui.actionShowIgnored))
            self.ui.actionLoaderAll.triggered.connect(lambda: self.change_action_chk_show_loader(self.ui.actionLoaderAll))
            self.ui.actionWithoutLoader.triggered.connect(lambda: self.change_action_chk_show_loader(self.ui.actionWithoutLoader))
            self.ui.actionForgeLoader.triggered.connect(lambda: self.change_action_chk_show_loader(self.ui.actionForgeLoader))
            self.ui.actionFabricLoader.triggered.connect(lambda: self.change_action_chk_show_loader(self.ui.actionFabricLoader))
            self.ui.actionBothLoader.triggered.connect(lambda: self.change_action_chk_show_loader(self.ui.actionBothLoader))

        except Exception as e:
            print('MAIN_WINDOW setupEvents: ', str(e))

    def action_table_multiselection(self):
        if self.ui.actionMultiselection.isChecked():
            self.ui.tableMods.setSelectionMode(QAbstractItemView.ExtendedSelection)
        else:
            self.ui.tableMods.setSelectionMode(QAbstractItemView.SingleSelection)

    def change_action_chk_show_loader(self, action):
        for chk in self.showlist_loader:
            if chk != action:
                chk.setChecked(False)

        if not self.ui.actionLoaderAll.isChecked() and not self.ui.actionWithoutLoader.isChecked() and not self.ui.actionForgeLoader.isChecked() and not self.ui.actionFabricLoader.isChecked() and not self.ui.actionBothLoader.isChecked():
            self.ui.actionLoaderAll.setChecked(True)


        self.load_data()

    def change_action_chk_show_state(self, action):
        for chk in self.showlist_state:
            if chk != action:
                chk.setChecked(False)

        self.load_data()

    # ------------------------------------------------------------------------------------------------------------------

    def filter_change(self):
        try:
            self.load_pages()
        except Exception as e:
            print('MAIN_WINDOW filter_change: ', str(e))

    def change_cmb_list(self):
        try:
            islist = self.is_list()
            self.ui.actionShowUpdated.setEnabled(islist)
            self.ui.actionShowInstalled.setEnabled(islist)
            self.ui.actionShowIgnored.setEnabled(islist)

            self.ui.actionLoaderAll.setEnabled(islist)
            self.ui.actionWithoutLoader.setEnabled(islist)
            self.ui.actionForgeLoader.setEnabled(islist)
            self.ui.actionFabricLoader.setEnabled(islist)
            self.ui.actionBothLoader.setEnabled(islist)

            self.ui.actionShowNoFindFavorites.setEnabled(islist)
            self.ui.actionIgnoreNoLoader.setEnabled(islist)

            self.filter_change()
        except Exception as e:
            print('MAIN_WINDOW change_cmb_list: ', str(e))

    def edit_name_clear(self):
        if self.ui.editName.text() == '':
            self.filter_change()

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
                    self.ui.cmbCategoryConfig.setCurrentIndex(self.ui.cmbCategoryConfig.findText(mod.categories))
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

                    self.ui.editNameConfig.setText(' - VARIOS (%d) - ' % len(self.selectedMods))

                    if state.loader is not None:
                        self.ui.cmbLoaderConfig.setCurrentIndex(self.ui.cmbLoaderConfig.findText(state.loader))
                    else:
                        self.ui.cmbLoaderConfig.setCurrentIndex(0)

                    if state.categories is not None:
                        self.ui.cmbCategoryConfig.setCurrentIndex(self.ui.cmbCategoryConfig.findText(state.categories))
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

    def left_page(self):
        if 0 < self.current_page:
            self.current_page -= 1
        self.fill_table()

    def right_page(self):
        if self.current_page < self.maxpages:
            self.current_page += 1
        self.fill_table()

    # ------------------------------------------------------------------------------------------------------------------

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
                        q.bindValue(':category', mod.categories)

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

                self.load_data()


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

    # ------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def optional_filter(field, value: Union[str, int], previus_sql, tableas='', novalue='', like=False):
        try:
            field = field.strip()

            if 'WHERE' not in previus_sql.upper():
                prefix = ' WHERE '
            else:
                prefix = ' AND '

            if tableas:
                tableas = tableas + '.'

            if like:
                condition = ' LIKE '
            else:
                condition = ' == '

            if isinstance(value, str) and value.strip() != novalue:
                return prefix + tableas + field + condition + ':' + field + ' '
            elif isinstance(value, int) and value:
                return prefix + tableas + field + condition + int(value) + ' '
            else:
                return ' '
        except Exception as e:
            print('MAIN_WINDOW optional_filter: ', str(e))

    def query_create_basic_where(self):
        try:
            where = ''
            where += self.optional_filter('loader', self.get_loader(), where, tableas='M')
            where += self.optional_filter('categories', self.ui.cmbCategory.currentText(), where, novalue='Todas', tableas='M')
            where += self.optional_filter('name', self.ui.editName.text(), where, like=True, tableas='M')
            return where
        except Exception as e:
            print('MAIN_WINDOW query_where_order: ', str(e))

    def query_bind_basic_where(self, q):
        q.bindValue(':loader', self.get_loader())
        q.bindValue(':categories', self.ui.cmbCategory.currentText())
        q.bindValue(':name', '%' + self.ui.editName.text() + '%')

        q.bindValue(':list', self.ui.cmbModList.currentText())

    def prepare_fill_table_query(self, q, count=False):
        try:
            where_q = self.query_create_basic_where()
            orderby_q = 'ORDER BY M.favorite DESC, M.blocked ASC, M.name ASC '

            if self.is_list():
                select_q = 'SELECT M.icon, M.name, M.categories, M.loader, M.update_date, M.path, ML.installed, ML.ignored, ML.updated, M.favorite, M.blocked '
                from_q = 'FROM ModsLists as ML LEFT JOIN Mods as M ON ML.mod = M.path'
                where_q += self.optional_filter('list', self.ui.cmbModList.currentText(), where_q, tableas='ML')
                if self.ui.actionShowUpdated.isChecked():
                    where_q += ' AND ((installed == 0 AND ignored == 0) OR (installed == 1 AND updated == 1)) '
                    orderby_q = 'ORDER BY ML.installed DESC, ML.updated DESC, M.favorite DESC, M.name ASC '
                elif self.ui.actionShowInstalled.isChecked():
                    where_q += ' AND installed == 1 '
                elif self.ui.actionShowIgnored.isChecked():
                    where_q += ' AND ignored == 1 '
                else:
                    where_q += ' AND installed == 0 AND ignored == 0 '

            else:
                select_q = 'SELECT M.icon, M.name, M.categories, M.loader, M.update_date, M.path, 0, 0, 0, M.favorite, M.blocked '
                from_q = 'FROM Mods as M'
                if self.ui.cmbModList.currentIndex() == self.ui.cmbModList.count() - 2:
                    where_q += self.optional_filter('favorite', 1, where_q)
                elif self.ui.cmbModList.currentIndex() == self.ui.cmbModList.count() - 1:
                    where_q += self.optional_filter('blocked', 1, where_q)

            offset_q = ';'
            if count:
                select_q = 'SELECT COUNT(M.path) '
            else:
                offset_q = 'LIMIT ' + str(MainWindow.rows_per_page) + ' OFFSET ' + str(self.current_page*MainWindow.rows_per_page) + ';'

            q.prepare(select_q + from_q + where_q + orderby_q + offset_q)
            self.query_bind_basic_where(q)

        except Exception as e:
            print('MAIN_WINDOW prepare_fill_table_query: ', str(e))

    def load_pages(self):
        try:
            q = QtSql.QSqlQuery()
            self.prepare_fill_table_query(q, count=True)
            if self.exec(q) and q.next():
                self.found_results = q.value(0)
                self.maxpages = math.ceil(q.value(0) / MainWindow.rows_per_page)
            else:
                self.found_results = 0
                self.maxpages = 0

            self.tableMods.clear()
            self.prepare_fill_table_query(q)
            if self.exec(q):
                while q.next():
                    self.tableMods.append(Mod(q))

            self.current_page = 0
            self.fill_table()

        except Exception as e:
            print('MAIN_WINDOW load_pages: ', str(e))

    def fill_table(self):
        try:
            self.clear_selected()
            self.check_table_buttons()
            self.ui.tableMods.setRowCount(0)
            QCoreApplication.processEvents()

            if self.found_results > 0:

                start = self.current_page * MainWindow.rows_per_page
                finish = (self.current_page+1) * MainWindow.rows_per_page
                if finish > self.found_results:
                    self.ui.lblActualPages.setText('%d - %d / %d' % (start + 1, self.found_results, self.found_results))
                    self.ui.tableMods.setRowCount(self.found_results - start)
                    finish = self.found_results+1
                else:
                    self.ui.lblActualPages.setText('%d - %d / %d' % (start + 1, finish, self.found_results))
                    self.ui.tableMods.setRowCount(finish - start)

                for i in range(start, finish):
                    self.ui.tableMods.setCellWidget(i, 0, self.tableMods[i].lblIcon)
                    self.ui.tableMods.setCellWidget(i, 1, self.tableMods[i].lblName)
                    self.ui.tableMods.setCellWidget(i, 2, self.tableMods[i].lblCategories)

                    self.ui.tableMods.setItem(i, 3, QtWidgets.QTableWidgetItem('  ' + self.tableMods[i].loader + '  '))
                    self.ui.tableMods.setItem(i, 4, QtWidgets.QTableWidgetItem('  ' + time.strftime('%d/%m/%Y', time.localtime(self.tableMods[i].update_date)) + '  '))

                    self.ui.tableMods.item(i, 3).setTextAlignment(QtCore.Qt.AlignCenter)
                    self.ui.tableMods.item(i, 4).setTextAlignment(QtCore.Qt.AlignCenter)

            else:
                self.ui.lblActualPages.setText('0 / 0')

        except Exception as e:
            print('MAIN_WINDOW load_data: ', str(e), str(e.__))

    def check_table_buttons(self):
        self.ui.btnPageLeft.setEnabled(0 < self.current_page)
        self.ui.btnPageRight.setEnabled(self.current_page < self.maxpages)
        self.ui.lblActualPages.setEnabled(self.maxpages > 0)

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
            if dialog.exec():
                loader = dialog.ui.cmbModList.currentText()
                if loader != self.ui.cmbModList.currentText():
                    self.ui.cmbModList.setCurrentIndex(self.ui.cmbModList.findText(loader))
                else:
                    self.load_data()
        except Exception as e:
            print('MAIN_WINDOW show_searching_dialog: ', str(e))

    # ------------------------------------------------------------------------------------------------------------------

    def is_list(self):
        return 1 < self.ui.cmbModList.currentIndex() < self.ui.cmbModList.count()-3

    def get_loader(self):
        for loader in self.showlist_loader:
            if loader.isChecked():
                return loader.text()
        return ''

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


