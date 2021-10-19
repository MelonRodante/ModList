import time

from typing import Union

from PyQt5 import QtWidgets, QtCore, QtSql
from PyQt5.QtCore import QSize, Qt, QCoreApplication
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QAbstractItemView
from qtpy.QtWidgets import QButtonGroup

from utils.database import Database
from utils.icon_utils import IconUtils
from utils.mod import Mod
from pyqt_style import colors
from pyqt_widgets.delegates import TableStyleItemDelegate
from pyqt_widgets.tableitems import TableItemName, TableItemButton, TableItemCategories
from pyqt_windows.main_window import Ui_ModList
from windows.admin_list_dialog import AdminListDialog
from windows.searching_dialog import SearchingDialog


class MainWindow(QtWidgets.QMainWindow):
    rows_per_page = 50
    categories = [
        ['Sin categoria', 'without-category', None],
        ['World Gen', 'world-gen', None],
        ['Biomas', 'world-biomes', None],
        ['Ores and Resources', 'world-ores-resources', None],
        ['Structures', 'world-structures', None],
        ['Dimensiones', 'world-dimensions', None],
        ['Mobs', 'world-mobs', None],
        ['Technology', 'technology', None],
        ['Processing', 'technology-processing', None],
        ['Player Transport', 'technology-player-transport', None],
        ['I/F/E Transport', 'technology-item-fluid-energy-transport', None],
        ['Farming', 'technology-farming', None],
        ['Energy', 'technology-energy', None],
        ['Genetics', 'technology-genetics', None],
        ['Automation', 'technology-automation', None],
        ['Magic', 'magic', None],
        ['Storage', 'storage', None],
        ['API and Library', 'library-api', None],
        ['Adventure and RPG', 'adventure-rpg', None],
        ['Map and Information', 'map-information', None],
        ['Cosmetic', 'cosmetic', None],
        ['Miscellaneous', 'mc-miscellaneous', None],
        ['Addon', 'mc-addons', None],
        ['Armor / Tools / Weapons', 'armor-weapons-tools', None],
        ['Server Utility', 'server-utility', None],
        ['Food', 'mc-food', None],
        ['Redstone', 'redstone', None],
        ['Twitch Integration', 'twitch-integration', None]
    ]

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_ModList()
        self.ui.setupUi(self)

        self.bold_font = self.create_bold_font()
        self.state_icons = self.create_state_icons()

        self.showlist_state = (self.ui.actionShowUpdated, self.ui.actionShowInstalled, self.ui.actionShowIgnored)
        self.showlist_loader = (self.ui.actionWithoutLoader, self.ui.actionForgeLoader, self.ui.actionFabricLoader, self.ui.actionBothLoader)

        self.chks_categories = {}
        self.chks_categories_group = QButtonGroup()

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
            f.setPixelSize(15)
            return f
        except Exception as e:
            print('MAIN_WINDOW create_bold_font: ', str(e))

    @staticmethod
    def create_state_icons():
        return {
            'e': IconUtils.getNormalIcon(":/state/state/empty.png"),

            'f': IconUtils.getNormalIcon(":/states/states/favorite.png"),
            'b': IconUtils.getNormalIcon(":/states/states/blocked.png"),

            'u': IconUtils.getNormalIcon(":/states/states/updated.png"),
            'uf': IconUtils.getNormalIcon(":/states/states/updated_favorite.png"),

            'i': IconUtils.getNormalIcon(":/states/states/installed.png"),
            'ui': IconUtils.getNormalIcon(":/states/states/updated_installed.png"),
            'fi': IconUtils.getNormalIcon(":/states/states/favorite_installed.png"),
            'ufi': IconUtils.getNormalIcon(":/states/states/updated_favorite_installed.png"),

            'g': IconUtils.getNormalIcon(":/states/states/ignored.png"),
            'ug': IconUtils.getNormalIcon(":/states/states/updated_ignored.png"),
            'fg': IconUtils.getNormalIcon(":/states/states/favorite_ignored.png"),
            'ufg': IconUtils.getNormalIcon(":/states/states/updated_favorite_ignored.png")
        }

    # ------------------------------------------------------------------------------------------------------------------

    def setupWidgets(self):
        try:

            self.ui.chkInstalledConfig.setShortcut("<")

            self.modify_css()
            self.resize_table()
            self.create_cmb_values_lists()
            self.create_cmb_values_categories()
            self.create_chk_values_categories_config()
            self.resize_combobox_loader()
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

            self.ui.lblActualPages.setStyleSheet(
                'QLabel {border: 1px solid ' + colors.ColorStrong + '; background-color: ' + colors.DarkBackground + ';} '
                                                                                                                     'QLabel:disabled {border: 1px solid ' + colors.Border + '; color: ' + colors.Border + ';}')

            self.ui.tbtnCategoryConfig.setStyleSheet('''
                            QToolButton[popupMode="1"] {
                              color: ''' + colors.TextColor + ''';
                              border: 1px solid ''' + colors.Border + ''';
                              border-radius: 0;
                              background-color: ''' + colors.Background + ''';
                              selection-background-color: ''' + colors.Hover_and_SelectTable + ''';
                            }
                            
                            QToolButton[popupMode="1"]:focus {
                              border: 1px solid ''' + colors.Focus_and_HoverMenus + ''';
                            }
                            
                            QToolButton[popupMode="1"]:hover {
                              border: 1px solid ''' + colors.Hover_and_SelectTable + ''';
                            }
                            
                            QToolButton[popupMode="1"]:disabled {
                              color: ''' + colors.DeactivatedTextColor + ''';
                            }
                            
                            QToolButton[popupMode="1"]::menu-button {
                              border: none;
                              border-left: 1px solid ''' + colors.Border + ''';
                              border-radius: 0;
                            }
        
                            QToolButton[popupMode="1"]::menu-arrow {
                              image: url(":/qss_icons/dark/rc/arrow_down_disabled.png");
                            }
                            
                            QToolButton[popupMode="1"]::menu-arrow:hover {
                              image: url(":/qss_icons/dark/rc/arrow_down.png");
                            }
        
                            ''')

        except Exception as e:
            print('MAIN_WINDOW modify_css: ', str(e))

    def resize_table(self):
        try:
            header = self.ui.tableMods.horizontalHeader()
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
            header.setSectionResizeMode(2, QtWidgets.QHeaderView.Fixed)
            header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(5, QtWidgets.QHeaderView.Fixed)

            self.ui.tableMods.setColumnWidth(0, 33)
            self.ui.tableMods.setColumnWidth(2, 147)
            self.ui.tableMods.setColumnWidth(5, 23)
            self.ui.tableMods.setIconSize(QSize(64, 64))
        except Exception as e:
            print('MAIN_WINDOW resize_table: ', str(e))

    def resize_combobox_loader(self):
        try:
            self.ui.cmbLoaderConfig.insertSeparator(1)
            model = self.ui.cmbLoaderConfig.model()
            for i in range(model.rowCount()):
                model.setData(model.index(i, 0), QSize(0, 20), Qt.SizeHintRole)
        except Exception as e:
            print('MAIN_WINDOW resize_combobox_loader: ', str(e))

    def create_cmb_values_lists(self):
        try:
            q = QtSql.QSqlQuery()
            q.prepare('select listname from Lists')

            self.ui.cmbModList.clear()

            self.ui.cmbModList.addItem('Todos')
            self.ui.cmbModList.insertSeparator(self.ui.cmbModList.count())

            if q.exec_():
                while q.next():
                    self.ui.cmbModList.addItem(q.value(0))

            if self.ui.cmbModList.count() > 2:
                self.ui.cmbModList.insertSeparator(self.ui.cmbModList.count())
            self.ui.cmbModList.addItem('Nuevos Mods')
            self.ui.cmbModList.addItem('Pre-Ignorados')
            self.ui.cmbModList.addItem('Favoritos')
            self.ui.cmbModList.addItem('Bloqueados')

            model = self.ui.cmbModList.model()
            for i in range(model.rowCount()):
                model.setData(model.index(i, 0), QSize(0, 20), Qt.SizeHintRole)
        except Exception as e:
            print('MAIN_WINDOW create_cmb_values_lists: ', str(e))

    def create_cmb_values_categories(self):
        try:
            self.ui.cmbCategories.clear()

            self.ui.cmbCategories.addItem('Todas')
            self.ui.cmbCategories.insertSeparator(1)

            for cat in MainWindow.categories:
                self.ui.cmbCategories.addItem(IconUtils.getNormalIcon(':/categories/categories/' + cat[1] + '.png'),
                                              cat[0])

            model = self.ui.cmbCategories.model()
            for i in range(model.rowCount()):
                model.setData(model.index(i, 0), QSize(0, 20), Qt.SizeHintRole)

        except Exception as e:
            print('MAIN_WINDOW create_cmb_values_categories: ', str(e))

    # ------------------------------------------------------------------------------------------------------------------

    def create_chkbox_action(self, menu, cat, state=False):
        action = QtWidgets.QWidgetAction(menu)

        height = 26
        chk = QtWidgets.QCheckBox("{:<38}".format(cat[0]))
        chk.setStyleSheet(
            'QCheckBox {padding-top: 10px; padding-bottom: 10px; spacing: 5px; margin-top: -5px; margin-bottom: -5px; margin-right: -30px;}'
            'QCheckBox:hover {background-color: ' + colors.B30 + ';}'
                                                                 'QCheckBox::indicator:checked {image: url(":/qss_icons/dark/rc/checkbox_checked_focus.png");}'
                                                                 'QCheckBox::indicator {height: %dpx;}' % height
        )
        chk.setFixedHeight(height)
        chk.setChecked(state)
        chk.setFocusPolicy(Qt.NoFocus)
        if cat[1]:
            chk.setIcon(IconUtils.getNormalIcon(':/categories/categories/' + cat[1] + '.png'))
        else:
            f = chk.font()
            f.setBold(True)
            chk.setFont(f)

        self.chks_categories[cat[1]] = chk
        self.chks_categories_group.addButton(chk)
        action.setDefaultWidget(chk)
        return action

    def create_chk_values_categories_config(self):
        try:
            menu = QtWidgets.QMenu()
            menu.setStyleSheet('QMenu {border: 1px solid ' + colors.ColorStrong + ';}')

            menu.addAction(self.create_chkbox_action(menu, ['NO MODIFICAR', '', None], state=True))
            menu.addSeparator()
            for cat in MainWindow.categories:
                menu.addAction(self.create_chkbox_action(menu, cat))

            self.ui.tbtnCategoryConfig.setMenu(menu)
            self.ui.tbtnCategoryConfig.clicked.connect(self.ui.tbtnCategoryConfig.showMenu)

            self.chks_categories_group.setExclusive(False)
            self.chks_categories_group.buttonPressed.connect(self.change_chk_categories)

        except Exception as e:
            print('MAIN_WINDOW create_chk_values_categories_config: ', str(e))

    def change_chk_categories(self, chk):
        try:
            chk.nextCheckState()

            if chk == self.chks_categories['']:
                for c in self.chks_categories.values():
                    c.setChecked(False)
                chk.setChecked(True)
            else:
                i = 0
                for c in self.chks_categories.values():
                    if c.isChecked() and c != self.chks_categories['']:
                        i += 1
                if i == 0:
                    self.chks_categories[''].setChecked(i == 0)
                else:
                    if chk == self.chks_categories['without-category']:
                        if chk.isChecked:
                            for c in self.chks_categories.values():
                                c.setChecked(False)
                            chk.setChecked(True)
                    elif i >= 6:
                        chk.setChecked(False)
                    else:
                        self.chks_categories[''].setChecked(False)
                        self.chks_categories['without-category'].setChecked(False)

            self.change_state_categories_config()
            chk.nextCheckState()
        except Exception as e:
            print('MAIN_WINDOW change_chk_categories: ', str(e))

    def change_state_categories_config(self):
        try:
            if self.chks_categories[''].isChecked():
                self.ui.tbtnCategoryConfig.setToolButtonStyle(Qt.ToolButtonTextOnly)
                self.ui.tbtnCategoryConfig.setText('')
            else:
                self.ui.tbtnCategoryConfig.setToolButtonStyle(Qt.ToolButtonIconOnly)
                self.ui.tbtnCategoryConfig.setIcon(
                    IconUtils.getLargeIcon(self.get_categories_from_checks(), center=True))
        except Exception as e:
            print('MAIN_WINDOW change_state_categories_config: ', str(e))

    # ------------------------------------------------------------------------------------------------------------------

    def setupEvents(self):
        try:

            self.ui.cmbModList.currentIndexChanged.connect(self.change_cmb_list)
            self.ui.cmbCategories.currentIndexChanged.connect(self.filter_change)
            self.ui.editName.returnPressed.connect(self.filter_change)
            self.ui.editName.textEdited.connect(self.edit_name_clear)

            self.ui.tableMods.itemSelectionChanged.connect(self.change_table_selection)
            self.ui.tableMods.itemClicked.connect(TableItemButton.click_icon_table)

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

            self.ui.actionShowUpdated.triggered.connect(
                lambda: self.change_action_chk_show_state(self.ui.actionShowUpdated))
            self.ui.actionShowInstalled.triggered.connect(
                lambda: self.change_action_chk_show_state(self.ui.actionShowInstalled))
            self.ui.actionShowIgnored.triggered.connect(
                lambda: self.change_action_chk_show_state(self.ui.actionShowIgnored))
            self.ui.actionLoaderAll.triggered.connect(
                lambda: self.change_action_chk_show_loader(self.ui.actionLoaderAll))
            self.ui.actionWithoutLoader.triggered.connect(
                lambda: self.change_action_chk_show_loader(self.ui.actionWithoutLoader))
            self.ui.actionForgeLoader.triggered.connect(
                lambda: self.change_action_chk_show_loader(self.ui.actionForgeLoader))
            self.ui.actionFabricLoader.triggered.connect(
                lambda: self.change_action_chk_show_loader(self.ui.actionFabricLoader))
            self.ui.actionBothLoader.triggered.connect(
                lambda: self.change_action_chk_show_loader(self.ui.actionBothLoader))

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

        self.load_pages()

    def change_action_chk_show_state(self, action):
        for chk in self.showlist_state:
            if chk != action:
                chk.setChecked(False)

        self.load_pages()

    # ------------------------------------------------------------------------------------------------------------------

    def filter_change(self):
        try:
            self.current_page = 0
            self.load_pages()
        except Exception as e:
            print('MAIN_WINDOW filter_change: ', str(e))

    def change_cmb_list(self):
        try:
            islist = self.is_list()
            self.ui.actionShowUpdated.setEnabled(islist)
            self.ui.actionShowInstalled.setEnabled(islist)
            self.ui.actionShowIgnored.setEnabled(islist)

            if islist is False:
                self.ui.actionShowUpdated.setChecked(False)
                self.ui.actionShowInstalled.setChecked(False)
                self.ui.actionShowIgnored.setChecked(False)

            self.ui.actionShowNoFindFavorites.setEnabled(islist)
            self.ui.actionIgnoreNoLoader.setEnabled(islist)

            self.filter_change()
        except Exception as e:
            print('MAIN_WINDOW change_cmb_list: ', str(e))

    def edit_name_clear(self):
        if self.ui.editName.text() == '':
            self.filter_change()

    def left_page(self):
        if 0 < self.current_page:
            self.current_page -= 1
        self.load_data()

    def right_page(self):
        if self.current_page < self.maxpages:
            self.current_page += 1
        self.load_data()

    # ------------------------------------------------------------------------------------------------------------------

    def change_table_selection(self):
        try:
            self.selectedMods = []
            if len(self.ui.tableMods.selectedIndexes()) > 0:
                islist = self.is_list()
                self.selection_widgets_select(islist)

                if len(self.ui.tableMods.selectedItems()) == 6:
                    self.selection_single(islist)
                else:
                    self.selection_range(islist)

            else:
                self.clear_selected()

        except Exception as e:
            print('MAIN_WINDOW change_table_selection:', e)

    def selection_single(self, islist):
        try:
            mod = self.ui.tableMods.selectedItems()[0].mod

            self.selectedMods.append(mod)

            self.ui.editNameConfig.setText(mod.name)
            self.ui.cmbLoaderConfig.setCurrentIndex(self.ui.cmbLoaderConfig.findText(mod.loader))

            for cat in mod.categories.split(','):
                try:
                    self.chks_categories[cat].setChecked(True)
                except Exception as e:
                    print('MAIN_WINDOW selection_single:', e)
            self.chks_categories[''].setChecked(False)
            self.change_state_categories_config()

            if islist:
                self.ui.chkInstalledConfig.setChecked(bool(mod.installed))
                self.ui.chkIgnoredConfig.setChecked(bool(mod.ignored))

                self.ui.chkUpdated.setEnabled(bool(mod.updated))
                self.ui.chkUpdated.setChecked(not bool(mod.updated))
            else:
                self.ui.chkInstalledConfig.setChecked(False)
                self.ui.chkIgnoredConfig.setChecked(False)
                self.ui.chkUpdated.setChecked(False)

            self.ui.chkPreIgnore.setChecked(bool(mod.preignore))
            self.ui.chkFavoriteConfig.setChecked(bool(mod.favorite))
            self.ui.chkBlockedConfig.setChecked(bool(mod.blocked))
        except Exception as e:
            print('MAIN_WINDOW selection_single:', e)

    def selection_range(self, islist):
        try:
            for r in self.ui.tableMods.selectedRanges():
                for i in range(r.topRow(), r.bottomRow() + 1):
                    self.selectedMods.append(self.ui.tableMods.item(i, 0).mod)

            state = Mod(self.selectedMods)

            self.ui.editNameConfig.setText(' - VARIOS (%d) - ' % len(self.selectedMods))

            if state.loader is not None:
                self.ui.cmbLoaderConfig.setCurrentIndex(self.ui.cmbLoaderConfig.findText(state.loader))
            else:
                self.ui.cmbLoaderConfig.setCurrentIndex(0)

            if state.categories is not None:
                for cat in state.categories.split(','):
                    try:
                        self.chks_categories[cat].setChecked(True)
                    except Exception as e:
                        print('MAIN_WINDOW selection_single:', e)
            else:
                self.chks_categories[''].setChecked(True)
            self.change_state_categories_config()

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

            if state.preignore is not None:
                self.ui.chkPreIgnore.setChecked(bool(state.preignore))
            else:
                self.ui.chkPreIgnore.setTristate(True)
                self.ui.chkPreIgnore.setCheckState(Qt.PartiallyChecked)

            if state.favorite is not None:
                self.ui.chkFavoriteConfig.setChecked(bool(state.favorite))
            else:
                self.ui.chkFavoriteConfig.setTristate(True)
                self.ui.chkFavoriteConfig.setCheckState(Qt.PartiallyChecked)

            if state.blocked is not None:
                self.ui.chkBlockedConfig.setChecked(bool(state.blocked))
            else:
                self.ui.chkBlockedConfig.setTristate(True)
                self.ui.chkBlockedConfig.setCheckState(Qt.PartiallyChecked)
        except Exception as e:
            print('MAIN_WINDOW selection_range:', e)

    def selection_widgets_select(self, islist):
        try:
            self.ui.editNameConfig.setEnabled(True)
            self.ui.cmbLoaderConfig.setEnabled(True)
            self.ui.tbtnCategoryConfig.setEnabled(True)
            for chk in self.chks_categories.values():
                chk.setChecked(False)

            self.ui.chkPreIgnore.setEnabled(True)
            self.ui.chkFavoriteConfig.setEnabled(True)
            self.ui.chkBlockedConfig.setEnabled(True)
            self.ui.chkInstalledConfig.setEnabled(islist)
            self.ui.chkIgnoredConfig.setEnabled(islist)
            self.ui.chkUpdated.setEnabled(islist)

            self.ui.chkPreIgnore.setTristate(False)
            self.ui.chkFavoriteConfig.setTristate(False)
            self.ui.chkBlockedConfig.setTristate(False)
            self.ui.chkInstalledConfig.setTristate(False)
            self.ui.chkIgnoredConfig.setTristate(False)
            self.ui.chkUpdated.setTristate(False)
        except Exception as e:
            print('MAIN_WINDOW selection_widgets_select:', e)

    # ------------------------------------------------------------------------------------------------------------------

    def clear_selected(self):
        try:
            self.selectedMods = []

            self.ui.editNameConfig.setText('')
            self.ui.cmbLoaderConfig.setCurrentIndex(0)

            self.ui.tbtnCategoryConfig.setToolButtonStyle(Qt.ToolButtonTextOnly)
            self.ui.tbtnCategoryConfig.setText('')

            self.ui.btnSaveConfig.setEnabled(False)
            self.ui.editNameConfig.setEnabled(False)
            self.ui.cmbLoaderConfig.setEnabled(False)
            self.ui.tbtnCategoryConfig.setEnabled(False)

            self.ui.chkInstalledConfig.setChecked(False)
            self.ui.chkIgnoredConfig.setChecked(False)
            self.ui.chkUpdated.setChecked(False)
            self.ui.chkPreIgnore.setChecked(False)
            self.ui.chkFavoriteConfig.setChecked(False)
            self.ui.chkBlockedConfig.setChecked(False)

            self.ui.chkInstalledConfig.setEnabled(False)
            self.ui.chkIgnoredConfig.setEnabled(False)
            self.ui.chkUpdated.setEnabled(False)
            self.ui.chkPreIgnore.setEnabled(False)
            self.ui.chkFavoriteConfig.setEnabled(False)
            self.ui.chkBlockedConfig.setEnabled(False)
        except Exception as e:
            print('MAIN_WINDOW clear_selected: ', str(e))

    def save_mod_config(self):
        try:
            if len(self.selectedMods) > 0:
                q = QtSql.QSqlQuery()

                for mod in self.selectedMods:
                    q.prepare(
                        'UPDATE Mods SET loader = :loader, categories = :categories, preignore = :preignore, favorite = :favorite, blocked = :blocked, newmod = 0 WHERE projectid == :projectid;')
                    q.bindValue(':projectid', mod.projectid)

                    if self.ui.cmbLoaderConfig.currentIndex() != 0:
                        q.bindValue(':loader', self.ui.cmbLoaderConfig.currentText())
                    else:
                        q.bindValue(':loader', mod.loader)

                    if not self.chks_categories[''].isChecked():
                        q.bindValue(':categories', self.get_categories_from_checks())
                    else:
                        q.bindValue(':categories', mod.categories)

                    if self.ui.chkPreIgnore.checkState() != Qt.PartiallyChecked:
                        q.bindValue(':preignore', int(self.ui.chkPreIgnore.isChecked()))
                    else:
                        q.bindValue(':preignore', mod.preignore)

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
                        q.bindValue(':mod', mod.projectid)
                        self.exec(q)

                    elif self.is_list():
                        q.prepare('UPDATE ModsLists SET  installed = :installed, ignored = :ignored, updated = :updated WHERE list == :list AND mod == :mod;')
                        q.bindValue(':list', self.ui.cmbModList.currentText())
                        q.bindValue(':mod', mod.projectid)

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

                current_page = self.current_page
                scroll = self.ui.tableMods.verticalScrollBar().sliderPosition()
                print(scroll)
                self.load_pages()
                if current_page == self.current_page:
                    QCoreApplication.processEvents()
                    self.ui.tableMods.verticalScrollBar().setSliderPosition(scroll)
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
    def optional_filter(field, value: Union[bool, str, int], previus_sql, tableas='', novalue='', like=False):
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
                return prefix + tableas + field + condition + str(value) + ' '
            else:
                return ' '
        except Exception as e:
            print('MAIN_WINDOW optional_filter: ', str(e))

    @staticmethod
    def actual_category_filter(text, compare_index=0):
        for cat in MainWindow.categories:
            if cat[compare_index] == text:
                return cat
        return ['', '', None]

    def query_create_basic_where(self):
        try:
            where = ''
            where += self.optional_filter('loader', self.get_loader(), where, tableas='M')
            where += self.optional_filter('categories', self.ui.cmbCategories.currentText(), where, like=True,
                                          novalue='Todas', tableas='M')
            where += self.optional_filter('name', self.ui.editName.text(), where, like=True, tableas='M')
            return where
        except Exception as e:
            print('MAIN_WINDOW query_where_order: ', str(e))

    def query_bind_basic_where(self, q):
        try:
            q.bindValue(':loader', self.get_loader())
            q.bindValue(':categories',
                        '%' + MainWindow.actual_category_filter(self.ui.cmbCategories.currentText())[1] + '%')
            q.bindValue(':name', '%' + self.ui.editName.text() + '%')

            q.bindValue(':list', self.ui.cmbModList.currentText())
        except Exception as e:
            print('MAIN_WINDOW query_bind_basic_where: ', str(e))

    def prepare_fill_table_query(self, q, count=False):
        try:
            where_q = self.query_create_basic_where()
            orderby_q = 'ORDER BY M.favorite DESC, M.blocked ASC, M.name ASC '

            if self.is_list():
                select_q = 'SELECT M.icon, M.name, M.categories, M.loader, M.update_date, M.path, ML.installed, ML.ignored, ML.updated, M.favorite, M.blocked, M.projectid, M.preignore '
                from_q = 'FROM ModsLists as ML LEFT JOIN Mods as M ON ML.mod = M.projectid'
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
                select_q = 'SELECT M.icon, M.name, M.categories, M.loader, M.update_date, M.path, 0, 0, 0, M.favorite, M.blocked, M.projectid, M.preignore '
                from_q = 'FROM Mods as M'
                if self.ui.cmbModList.currentIndex() == self.ui.cmbModList.count() - 4:
                    where_q += self.optional_filter('newmod', 1, where_q)
                elif self.ui.cmbModList.currentIndex() == self.ui.cmbModList.count() - 3:
                    where_q += self.optional_filter('preignore', 1, where_q)
                elif self.ui.cmbModList.currentIndex() == self.ui.cmbModList.count() - 2:
                    where_q += self.optional_filter('favorite', 1, where_q)
                elif self.ui.cmbModList.currentIndex() == self.ui.cmbModList.count() - 1:
                    where_q += self.optional_filter('blocked', 1, where_q)

            offset_q = ';'
            if count:
                select_q = 'SELECT COUNT(M.projectid) '
            else:
                offset_q = 'LIMIT ' + str(MainWindow.rows_per_page) + ' OFFSET ' + str(
                    self.current_page * MainWindow.rows_per_page) + ';'

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
                self.maxpages = int(q.value(0) / MainWindow.rows_per_page)

                if self.maxpages > 0 and (q.value(0) % MainWindow.rows_per_page) == 0:
                    self.maxpages -= 1

            else:
                self.found_results = 0
                self.maxpages = 0

            if self.current_page > self.maxpages:
                self.current_page = self.maxpages

            self.load_data()

        except Exception as e:
            print('MAIN_WINDOW load_pages: ', str(e))

    def load_data(self):
        q = QtSql.QSqlQuery()
        self.tableMods.clear()
        self.prepare_fill_table_query(q)

        if self.exec(q):
            # print(self.current_page, q.lastQuery())
            while q.next():
                self.tableMods.append(Mod(q))

        self.fill_table()

    def fill_table(self):
        try:
            self.clear_selected()
            self.check_table_buttons()
            self.ui.tableMods.setRowCount(0)
            QCoreApplication.processEvents()

            if self.found_results > 0:

                start = self.current_page * MainWindow.rows_per_page + 1
                finish = (self.current_page + 1) * MainWindow.rows_per_page
                if finish > self.found_results:
                    self.ui.lblActualPages.setText('%d - %d / %d' % (start, self.found_results, self.found_results))
                else:
                    self.ui.lblActualPages.setText('%d - %d / %d' % (start, finish, self.found_results))

                self.ui.tableMods.setRowCount(len(self.tableMods))
                for i, mod in enumerate(self.tableMods):
                    self.ui.tableMods.setItem(i, 0, TableItemButton(mod))
                    self.ui.tableMods.setItem(i, 1, TableItemName(mod.name, self.bold_font))
                    self.ui.tableMods.setItem(i, 2, TableItemCategories(mod.categories))
                    self.ui.tableMods.setItem(i, 3, QtWidgets.QTableWidgetItem('  ' + mod.loader + '  '))

                    try:
                        date = '  ' + time.strftime('%d/%m/%Y', time.localtime(mod.update_date)) + '  '
                    except:
                        date = '  -  '
                    self.ui.tableMods.setItem(i, 4, QtWidgets.QTableWidgetItem(date))
                    self.ui.tableMods.setItem(i, 5, QtWidgets.QTableWidgetItem(self.get_state_icon(mod), ''))

                    self.ui.tableMods.item(i, 3).setTextAlignment(QtCore.Qt.AlignCenter)
                    self.ui.tableMods.item(i, 4).setTextAlignment(QtCore.Qt.AlignCenter)

            else:
                self.ui.lblActualPages.setText('0 / 0')

        except Exception as e:
            print('MAIN_WINDOW load_data: ', e)

    def check_table_buttons(self):
        self.ui.btnPageLeft.setEnabled(0 < self.current_page)
        self.ui.btnPageRight.setEnabled(self.current_page < self.maxpages)
        self.ui.lblActualPages.setEnabled(self.found_results != 0)

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
                    self.load_pages()
        except Exception as e:
            print('MAIN_WINDOW show_searching_dialog: ', str(e))

    # ------------------------------------------------------------------------------------------------------------------

    def is_list(self):
        return 1 < self.ui.cmbModList.currentIndex() < self.ui.cmbModList.count() - 4

    def get_loader(self):
        for loader in self.showlist_loader:
            if loader.isChecked():
                return loader.text()
        return ''

    def get_state_icon(self, mod):
        if mod.blocked:
            return self.state_icons['b']
        else:
            state = ''

            if mod.updated:
                state += 'u'

            if mod.favorite:
                state += 'f'

            if mod.installed:
                state += 'i'
            elif mod.ignored:
                state += 'g'

            if state != '':
                return self.state_icons[state]
            else:
                return self.state_icons['e']

    def get_categories_from_checks(self):
        c = []
        for cat, chk in self.chks_categories.items():
            if chk.isChecked():
                c.append(cat)
        c.sort()
        return ",".join(c)

    @staticmethod
    def exec(q):
        try:
            b = q.exec_()
            if b is False:
                print(q.lastError().text())
            return b
        except Exception as e:
            print('MAIN_WINDOW exec', e)
