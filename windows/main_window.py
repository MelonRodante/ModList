import os
import time
from functools import partial

from typing import Union


from PyQt5 import QtWidgets, QtSql, QtGui
from PyQt5.QtCore import QSize, Qt, QCoreApplication
from PyQt5.QtGui import QFont, QGuiApplication, QPixmap
from PyQt5.QtWidgets import QAbstractItemView, QMenu, QWidget, QSizePolicy, QButtonGroup, QAction

from utils.database import Database
from utils.icon_utils import IconUtils
from utils.mod import Mod
from pyqt_style import colors
from pyqt_widgets.delegates import TableStyleItemDelegate
from pyqt_widgets.tableitems import TableItemName, TableItemButton, TableItemCategories
from pyqt_windows.main_window import Ui_ModList
from utils.modcompare import ModCompare
from utils.utils import Utils
from windows.admin_categories_dialog import AdminCategoriesDialog
from windows.admin_list_dialog import AdminListDialog
from windows.copylist_dialog import CopyListDialog
from windows.searching_dialog import SearchingDialog
from windows.searching_mod_id_dialog import SearchingModIdDialog
from windows.warning_dialog import WarningDialog


class MainWindow(QtWidgets.QMainWindow):
    rows_per_page = 100

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_ModList()
        self.ui.setupUi(self)

        Database.connect_db()

        self.table_name_font = self.create_font_table_name()
        self.table_others_font = self.create_font_table_others()
        self.state_icons = self.create_state_icons()

        self.chks_categories = None
        self.chks_categories_group = None
        self.load_categories()

        self.islist = False

        self.current_page = 0
        self.maxpages = 0
        self.found_results = 0
        self.tableMods = []

        self.selectedMods = []

        self.setupWidgets()
        self.setupEvents()
        self.load_pages()
        self.show()

    def setupWidgets(self):
        try:
            self.modify_css()
            self.resize_table()
            self.create_cmb_values_lists()
            self.resize_combobox_loader_config()

            empty = QWidget()
            empty.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.ui.toolBar.insertWidget(self.ui.actionResetFilters, empty)
            self.ui.toolBar.setStyleSheet('QToolBar {border-right-color: ' + colors.ColorStrong + ';}')
            self.ui.toolBar.insertSeparator(self.ui.actionResetFilters)

            self.ui.actionExit.setShortcut('1')

        except Exception as e:
            Utils.print_exception('MAIN_WINDOW setupWidgets', e)

    def setupEvents(self):
        try:

            self.ui.toolBar.topLevelChanged.connect(self.change_toolbar_orientation)

            self.ui.cmbModList.currentIndexChanged.connect(self.change_cmb_list)
            self.ui.cmbCategories.currentIndexChanged.connect(self.filter_change)
            self.ui.editName.returnPressed.connect(self.filter_change)
            self.ui.editName.textEdited.connect(self.edit_name_clear)

            self.ui.tableMods.itemSelectionChanged.connect(self.select_mods)
            self.ui.tableMods.itemClicked.connect(TableItemButton.click_icon_table)
            self.ui.tableMods.itemPressed.connect(self.context_menu_table)

            self.ui.btnPageLeft.clicked.connect(self.click_left_page)
            self.ui.btnPageRight.clicked.connect(self.click_right_page)

            self.ui.btnSaveConfig.clicked.connect(self.save_configuration_mod)
            self.ui.chkInstalledConfig.clicked.connect(self.change_chk_installed)
            self.ui.chkIgnoredConfig.clicked.connect(self.change_chk_ignored)
            self.ui.chkFavoriteConfig.clicked.connect(self.change_chk_favorite)
            self.ui.chkBlockedConfig.clicked.connect(self.change_chk_blocked)



            # ACTIONS --------------------------------------------------------------------------------------------------

            self.ui.actionAdminCategories.triggered.connect(self.show_admin_categories_dialog)
            self.ui.actionAdminLists.triggered.connect(self.show_admin_list_dialog)
            self.ui.actionCopyList.triggered.connect(self.show_copylist_dialog)
            self.ui.actionSearchingNewMods.triggered.connect(self.show_searching_dialog)
            self.ui.actionSearchModID.triggered.connect(self.show_search_modid_dialog)

            self.ui.actionUpdateModInfo.triggered.connect(self.update_mod_info)
            self.ui.actionDeleteModDB.triggered.connect(self.delete_mod_from_db)

            self.ui.actionMultiselection.triggered.connect(self.table_selectmode)

            self.ui.actionExit.triggered.connect(self.exit_app)



            # FILTERS --------------------------------------------------------------------------------------------------

            self.ui.actionResetFilters.triggered.connect(self.clear_filters)

            loader_buttons = (self.ui.actionNoLoader, self.ui.actionForgeLoader, self.ui.actionFabricLoader, self.ui.actionForgeFabricLoader)
            self.ui.actionNoLoader.triggered.connect(
                lambda: self.exclusive_filter(self.ui.actionNoLoader, loader_buttons))
            self.ui.actionForgeLoader.triggered.connect(
                lambda: self.exclusive_filter(self.ui.actionForgeLoader, loader_buttons))
            self.ui.actionFabricLoader.triggered.connect(
                lambda: self.exclusive_filter(self.ui.actionFabricLoader, loader_buttons))
            self.ui.actionForgeFabricLoader.triggered.connect(
                lambda: self.exclusive_filter(self.ui.actionForgeFabricLoader, loader_buttons))

            autostate_buttons = (self.ui.actionAutoInstall, self.ui.actionAutoIgnore)
            self.ui.actionAutoInstall.triggered.connect(
                lambda: self.exclusive_filter(self.ui.actionAutoInstall, autostate_buttons))
            self.ui.actionAutoIgnore.triggered.connect(
                lambda: self.exclusive_filter(self.ui.actionAutoIgnore, autostate_buttons))

            state_buttons = (self.ui.actionShowInstalled, self.ui.actionShowIgnored)
            self.ui.actionShowInstalled.triggered.connect(
                lambda: self.exclusive_filter(self.ui.actionShowInstalled, state_buttons))
            self.ui.actionShowIgnored.triggered.connect(
                lambda: self.exclusive_filter(self.ui.actionShowIgnored, state_buttons))
            self.ui.actionShowUpdated.triggered.connect(self.load_pages)

        except Exception as e:
            Utils.print_exception('MAIN_WINDOW setupEvents', e)





    '''
    ----------------------------------------------------------------------
    SETUP WIDGETS
    ----------------------------------------------------------------------
    '''

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
            Utils.print_exception('MAIN_WINDOW modify_css', e)

    def filter_change(self):
        try:
            self.current_page = 0
            self.load_pages()

        except Exception as e:
            Utils.print_exception('MAIN_WINDOW filter_change', e)

    def change_toolbar_orientation(self, floating):
        try:
            if floating:
                self.ui.toolBar.setStyleSheet('')
            else:
                if self.ui.toolBar.orientation() == Qt.Orientation.Vertical:
                    if self.toolBarArea(self.ui.toolBar) == Qt.ToolBarArea.LeftToolBarArea:
                        self.ui.toolBar.setStyleSheet('QToolBar {border-right-color: ' + colors.ColorStrong + ';}')
                    elif self.toolBarArea(self.ui.toolBar) == Qt.ToolBarArea.RightToolBarArea:
                        self.ui.toolBar.setStyleSheet('QToolBar {border-left-color: ' + colors.ColorStrong + ';}')
                else:
                    if self.toolBarArea(self.ui.toolBar) == Qt.ToolBarArea.TopToolBarArea:
                        self.ui.toolBar.setStyleSheet('QToolBar {border-bottom-color: ' + colors.ColorStrong + ';}')
                    elif self.toolBarArea(self.ui.toolBar) == Qt.ToolBarArea.BottomToolBarArea:
                        self.ui.toolBar.setStyleSheet('QToolBar {border-top-color: ' + colors.ColorStrong + ';}')

        except Exception as e:
            Utils.print_exception('MAIN_WINDOW change_toolbar_orientation', e)

    def resize_table(self):
        try:
            header = self.ui.tableMods.horizontalHeader()
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
            header.setSectionResizeMode(2, QtWidgets.QHeaderView.Fixed)
            header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(5, QtWidgets.QHeaderView.Fixed)

            # Icon size in pyqt_widgets -> delegates
            self.ui.tableMods.setColumnWidth(0, 59)
            self.ui.tableMods.setColumnWidth(2, 191)
            self.ui.tableMods.setColumnWidth(5, 27)

        except Exception as e:
            Utils.print_exception('MAIN_WINDOW resize_table', e)




    '''
    ----------------------------------------------------------------------
    ACTIONS
    ----------------------------------------------------------------------
    '''

    def clear_filters(self):
        try:
            self.ui.actionNoLoader.setChecked(False)
            self.ui.actionForgeLoader.setChecked(False)
            self.ui.actionFabricLoader.setChecked(False)
            self.ui.actionForgeFabricLoader.setChecked(False)

            self.ui.actionAutoInstall.setChecked(False)
            self.ui.actionAutoIgnore.setChecked(False)

            self.ui.actionShowInstalled.setChecked(False)
            self.ui.actionShowIgnored.setChecked(False)
            self.ui.actionShowUpdated.setChecked(False)

            self.ui.editName.setText('')
            self.ui.cmbCategories.setCurrentIndex(0)

            self.load_pages()

        except Exception as e:
            Utils.print_exception('MAIN_WINDOW clear_filters', e)

    def table_selectmode(self, checked):
        try:
            if checked:
                self.ui.tableMods.setSelectionMode(QAbstractItemView.ExtendedSelection)
            else:
                self.ui.tableMods.setSelectionMode(QAbstractItemView.SingleSelection)

        except Exception as e:
            Utils.print_exception('MAIN_WINDOW table_selectmode', e)

    def exclusive_filter(self, button, list_buttons):
        try:
            if button.isChecked():
                for loader_filter in list_buttons:
                    if loader_filter != button:
                        loader_filter.setChecked(False)
            self.load_pages()

        except Exception as e:
            Utils.print_exception('MAIN_WINDOW exclusive_filter', e)

    def update_mod_info(self):
        q = QtSql.QSqlQuery()
        for mod in self.selectedMods:
            mod.update_basic_info(q)
        self.load_pages_maintain_slider()

    def delete_mod_from_db(self):
        if WarningDialog('Are you sure you want to delete ' + str(len(self.selectedMods)) + ' Mod/s from database?').exec():
            q = QtSql.QSqlQuery()
            for mod in self.selectedMods:
                mod.delete_from_db(q)
            self.load_pages_maintain_slider()

    def exit_app(self):
        try:
            # self.ui.cmbLoaderConfig.setCurrentIndex(3)
            self.ui.chkBlockedConfig.setChecked(True)
        except Exception as e:
            Utils.print_exception('MAIN_WINDOW exit', e)






    '''
    ----------------------------------------------------------------------
    CATEGORIES
    ----------------------------------------------------------------------
    '''

    def load_categories(self):
        try:
            Mod.categories = {'': {
                        'cat_id':           '',
                        'cat_name':         'NO MODIFY',
                        'cat_grp':          0,
                        'cat_ord':          0,
                        'cat_icon':         QPixmap(),
                        'cat_check':        None,
                        'cat_index_filter': None
                    }}
            self.chks_categories_group = QButtonGroup()

            q = QtSql.QSqlQuery()
            q.prepare('SELECT C.cat_id, C.cat_name, C.icon, C.grp, C.ord FROM Categories as C ORDER BY C.grp ASC, C.ord ASC, C.cat_name ASC;')

            if Utils.query_exec(q, 'MAIN_WINDOW load_categories'):
                while q.next():

                    icon = IconUtils.qbytearray_to_pixmap(q.value(2), size=48)
                    Mod.categories[q.value(0)] = {
                        'cat_id':           q.value(0),
                        'cat_name':         q.value(1),
                        'cat_grp':          q.value(3),
                        'cat_ord':          q.value(4),
                        'cat_icon':         icon,
                        'cat_check':        None,
                        'cat_index_filter': None
                    }

                    IconUtils.other_cat_icons[q.value(0)] = icon

            self.create_cmb_values_categories()
            self.create_menu_chk_categories_config()

        except Exception as e:
            Utils.print_exception('MAIN_WINDOW load_categories', e)

    def create_cmb_values_categories(self):
        try:
            self.ui.cmbCategories.clear()
            self.ui.cmbCategories.addItem('All Categories')
            self.ui.cmbCategories.insertSeparator(1)

            lastgrp = 1
            for cat in Mod.categories.values():
                if cat.get('cat_id') != '':
                    if lastgrp != cat.get('cat_grp'):
                        self.ui.cmbCategories.insertSeparator(self.ui.cmbCategories.count())
                        lastgrp = cat.get('cat_grp')
                    cat['cat_index_filter'] = self.ui.cmbCategories.count()
                    self.ui.cmbCategories.addItem(IconUtils.getCatNormalIcon(cat.get('cat_id')), cat.get('cat_name'))

            model = self.ui.cmbCategories.model()
            for i in range(model.rowCount()):
                model.setData(model.index(i, 0), QSize(0, 20), Qt.SizeHintRole)

        except Exception as e:
            Utils.print_exception('MAIN_WINDOW create_cmb_values_categories', e)

    def create_menu_chk_categories_config(self):
        try:
            menu = QtWidgets.QMenu()
            menu.setStyleSheet('QMenu {border: 1px solid ' + colors.ColorStrong + ';} QMenu::item {background-color: ' + colors.Background + '} QMenu::item:selected {background-color: ' + colors.B30 + '}')

            menu.addAction(self.create_chk_category_config_action(menu, Mod.categories.get('')))
            menu.addAction(self.create_chk_category_config_action(menu, Mod.categories.get('-cc-without-category')))
            menu.addSeparator()

            curse_categories = menu.addMenu('Curse Categories...')
            other_categories = None
            if len(Mod.categories) > len(Database.categories):
                other_categories = menu.addMenu('Other Categories...')

            lastgrp = 1
            for cat in Mod.categories.values():
                if cat.get('cat_id') != '' and cat.get('cat_id') != '-cc-without-category':
                    if cat.get('cat_grp') > 100 and other_categories is not None:
                        if lastgrp != cat.get('cat_grp'):
                            other_categories.addSeparator()
                            lastgrp = cat.get('cat_grp')
                        other_categories.addAction(self.create_chk_category_config_action(menu, cat))
                    else:
                        if lastgrp != cat.get('cat_grp') and lastgrp > 100:
                            if lastgrp > 100:
                                curse_categories.addSeparator()
                            lastgrp = cat.get('cat_grp')
                        curse_categories.addAction(self.create_chk_category_config_action(menu, cat))
                        if cat.get('cat_id') == '-cc-without-category':
                            curse_categories.addSeparator()

            self.ui.tbtnCategoryConfig.setMenu(menu)
            self.ui.tbtnCategoryConfig.clicked.connect(self.ui.tbtnCategoryConfig.showMenu)

            self.chks_categories_group.setExclusive(False)
            self.chks_categories_group.buttonPressed.connect(self.change_chk_categories)

        except Exception as e:
            Utils.print_exception('MAIN_WINDOW create_menu_chk_categories_config', e)

    def create_chk_category_config_action(self, menu, cat):
        try:
            action = QtWidgets.QWidgetAction(menu)
            height = 26

            chk = QtWidgets.QCheckBox()
            chk.setText("{:<38}".format(cat.get('cat_name')))
            chk.setIcon(IconUtils.getIconWithoutTint(cat.get('cat_icon')))
            if cat.get('cat_id') == '':
                f = chk.font()
                f.setPixelSize(14)
                f.setBold(True)
                chk.setFont(f)

            chk.setStyleSheet('QCheckBox {padding-top: 10px; padding-bottom: 10px; spacing: 5px; margin-top: -5px; margin-bottom: -5px; margin-right: -30px;}' 'QCheckBox:hover {background-color: ' + colors.B30 + ';}'                                                                                                                                                                                                 'QCheckBox::indicator {height: %dpx;}' % height)
            chk.setFixedHeight(height)
            chk.setFocusPolicy(Qt.NoFocus)

            cat['cat_check'] = chk
            self.chks_categories_group.addButton(chk)
            action.setDefaultWidget(chk)
            return action

        except Exception as e:
            Utils.print_exception('MAIN_WINDOW create_chk_category_config_action', e)

    # ------------------------------------------

    def actual_category_filter(self):
        try:
            for cat in Mod.categories.values():
                if cat.get('cat_index_filter') == self.ui.cmbCategories.currentIndex():
                    return cat['cat_id']
            return ''

        except Exception as e:
            Utils.print_exception('MAIN_WINDOW actual_category_filter', e)

    def change_chk_categories(self, chk):
        try:

            chk.nextCheckState()

            if chk == Mod.categories.get('').get('cat_check'):
                for cat in Mod.categories.values():
                    cat.get('cat_check').setChecked(False)
                chk.setChecked(True)
            else:
                i = 0
                for cat in Mod.categories.values():
                    if cat.get('cat_check').isChecked() and cat != Mod.categories.get(''):
                        i += 1

                if i == 0:
                    Mod.categories.get('').get('cat_check').setChecked(True)

                else:
                    if chk == Mod.categories.get('-cc-without-category').get('cat_check'):
                        if chk.isChecked:
                            for cat in Mod.categories.values():
                                cat.get('cat_check').setChecked(False)
                            chk.setChecked(True)

                    elif i >= 6:
                        chk.setChecked(False)

                    else:
                        Mod.categories.get('').get('cat_check').setChecked(False)
                        Mod.categories.get('-cc-without-category').get('cat_check').setChecked(False)

            self.change_state_categories_config()

            chk.nextCheckState()

        except Exception as e:
            Utils.print_exception('MAIN_WINDOW change_chk_categories', e)

    def change_state_categories_config(self):
        try:
            if Mod.categories.get('').get('cat_check').isChecked():
                self.ui.tbtnCategoryConfig.setToolButtonStyle(Qt.ToolButtonTextOnly)
                self.ui.tbtnCategoryConfig.setText('')
            else:
                self.ui.tbtnCategoryConfig.setToolButtonStyle(Qt.ToolButtonIconOnly)
                self.ui.tbtnCategoryConfig.setIcon(IconUtils.getLargeIcon(self.get_categories_from_checks(), center=True))

        except Exception as e:
            Utils.print_exception('MAIN_WINDOW change_state_categories_config', e)







    '''
    ----------------------------------------------------------------------
    LIST AND NAME
    ----------------------------------------------------------------------
    '''

    def create_cmb_values_lists(self):
        try:
            q = QtSql.QSqlQuery()
            q.prepare('select listname from Lists')

            self.ui.cmbModList.clear()

            self.ui.cmbModList.addItem('All Mods')
            self.ui.cmbModList.insertSeparator(self.ui.cmbModList.count())

            if self.exec(q, 'create_cmb_values_lists'):
                while q.next():
                    self.ui.cmbModList.addItem(q.value(0))

            if self.ui.cmbModList.count() > 2:
                self.ui.cmbModList.insertSeparator(self.ui.cmbModList.count())
            self.ui.cmbModList.addItem('New Mods')
            self.ui.cmbModList.addItem('Favorites')
            self.ui.cmbModList.addItem('Blocked')
            self.ui.cmbModList.addItem('No Blocked')

            model = self.ui.cmbModList.model()
            for i in range(model.rowCount()):
                model.setData(model.index(i, 0), QSize(0, 20), Qt.SizeHintRole)

        except Exception as e:
            Utils.print_exception('MAIN_WINDOW create_cmb_values_lists', e)

    def change_cmb_list(self):
        try:
            self.set_islist()

            self.ui.actionShowInstalled.setEnabled(self.islist)
            self.ui.actionShowIgnored.setEnabled(self.islist)
            self.ui.actionShowUpdated.setEnabled(self.islist)

            '''
            self.ui.btnViewInstalled.setEnabled(self.islist)
            self.ui.btnViewIgnored.setEnabled(self.islist)
            self.ui.btnViewUpdated.setEnabled(self.islist)
            '''

            if not self.islist:
                self.ui.chkInstalledConfig.setText('Auto-Install')
                self.ui.chkIgnoredConfig.setText('Auto-Ignore')
            else:
                self.ui.chkInstalledConfig.setText('Installed')
                self.ui.chkIgnoredConfig.setText('Ignored')

            self.filter_change()

        except Exception as e:
            Utils.print_exception('MAIN_WINDOW change_cmb_list', e)

    # ------------------------------------------

    def edit_name_clear(self):
        try:
            if self.ui.editName.text() == '':
                self.filter_change()

        except Exception as e:
            Utils.print_exception('MAIN_WINDOW edit_name_clear', e)






    '''
    ----------------------------------------------------------------------
    QUERY
    ----------------------------------------------------------------------
    '''

    def query_create_basic_where(self):
        try:
            where = ''
            where += self.optional_filter('loader', self.get_loader(), where, tableas='M')
            where += self.optional_filter('categories', self.ui.cmbCategories.currentText(), where, like=True,
                                          novalue='All Categories', tableas='M')
            where += self.optional_filter('name', self.ui.editName.text(), where, like=True, tableas='M')

            if self.ui.actionAutoInstall.isChecked():
                where += self.optional_filter('autoinstall', 1, where, tableas='M')
            elif self.ui.actionAutoIgnore.isChecked():
                where += self.optional_filter('autoignore', 1, where, tableas='M')

            return where

        except Exception as e:
            Utils.print_exception('MAIN_WINDOW query_create_basic_where', e)

    def query_bind_basic_where(self, q):
        try:
            q.bindValue(':loader', self.get_loader())
            q.bindValue(':categories', '%' + self.actual_category_filter() + '%')
            q.bindValue(':name', '%' + self.ui.editName.text() + '%')

            q.bindValue(':list', self.ui.cmbModList.currentText())

        except Exception as e:
            Utils.print_exception('MAIN_WINDOW query_bind_basic_where', e)

    def prepare_fill_table_query(self, q, count=False):
        try:
            if self.islist:
                select_q, from_q, where_q, orderby_q = self.prepare_fill_table_query_list()
            else:
                select_q, from_q, where_q, orderby_q = self.prepare_fill_table_query_nolist()

            offset_q = ';'
            if count:
                select_q = 'SELECT COUNT(M.projectid) '
            else:
                offset_q = 'LIMIT ' + str(MainWindow.rows_per_page) + ' OFFSET ' + str(
                    self.current_page * MainWindow.rows_per_page) + ';'

            q.prepare(select_q + from_q + where_q + orderby_q + offset_q)
            self.query_bind_basic_where(q)

        except Exception as e:
            Utils.print_exception('MAIN_WINDOW prepare_fill_table_query', e)

    def prepare_fill_table_query_list(self):
        try:
            select_q = Mod.select_modslist
            from_q = Mod.from_modslist
            where_q = self.query_create_basic_where()
            orderby_q = 'ORDER BY M.favorite DESC, M.blocked ASC, M.name ASC '

            where_q += self.optional_filter('list', self.ui.cmbModList.currentText(), where_q, tableas='ML')

            if self.ui.actionShowUpdated.isChecked():
                where_q += self.optional_filter('updated', 1, where_q, tableas='ML')
                orderby_q = 'ORDER BY ML.installed DESC, ML.updated DESC, M.favorite DESC, M.name ASC '

            if not self.ui.actionAutoInstall.isChecked() and not self.ui.actionAutoIgnore.isChecked():
                if self.ui.actionShowInstalled.isChecked():
                    where_q += self.optional_filter('installed', 1, where_q, tableas='ML')
                elif self.ui.actionShowIgnored.isChecked():
                    where_q += self.optional_filter('ignored', 1, where_q, tableas='ML')
                else:
                    where_q += self.optional_filter('installed', 0, where_q, tableas='ML')
                    where_q += self.optional_filter('ignored', 0, where_q, tableas='ML')

            return select_q, from_q, where_q, orderby_q

        except Exception as e:
            Utils.print_exception('MAIN_WINDOW prepare_fill_table_query_list', e)

    def prepare_fill_table_query_nolist(self):
        try:
            select_q = Mod.select_mods
            from_q = Mod.from_mods
            where_q = self.query_create_basic_where()
            orderby_q = 'ORDER BY M.favorite DESC, M.blocked ASC, M.name ASC '

            if self.ui.cmbModList.currentIndex() == self.ui.cmbModList.count() - 4:
                where_q += self.optional_filter('newmod', 1, where_q)
            elif self.ui.cmbModList.currentIndex() == self.ui.cmbModList.count() - 3:
                where_q += self.optional_filter('favorite', 1, where_q)
            elif self.ui.cmbModList.currentIndex() == self.ui.cmbModList.count() - 2:
                where_q += self.optional_filter('blocked', 1, where_q)
            elif self.ui.cmbModList.currentIndex() == self.ui.cmbModList.count() - 1:
                where_q += self.optional_filter('blocked', 0, where_q)

            return select_q, from_q, where_q, orderby_q

        except Exception as e:
            Utils.print_exception('MAIN_WINDOW prepare_fill_table_query_nolist', e)






    '''
    ----------------------------------------------------------------------
    TABLE
    ----------------------------------------------------------------------
    '''

    def click_left_page(self):
        try:
            if 0 < self.current_page:
                self.current_page -= 1
            self.load_data()

        except Exception as e:
            Utils.print_exception('MAIN_WINDOW click_left_page', e)

    def click_right_page(self):
        try:
            if self.current_page < self.maxpages:
                self.current_page += 1
            self.load_data()

        except Exception as e:
            Utils.print_exception('MAIN_WINDOW click_right_page', e)

    def check_table_buttons(self):
        try:
            self.ui.btnPageLeft.setEnabled(0 < self.current_page)
            self.ui.btnPageRight.setEnabled(self.current_page < self.maxpages)
            self.ui.lblActualPages.setEnabled(self.found_results != 0)

        except Exception as e:
            Utils.print_exception('MAIN_WINDOW check_table_buttons', e)

    # ------------------------------------------

    def clear_selected(self, enabled):
        try:
            self.ui.editNameConfig.setText('')
            self.ui.cmbLoaderConfig.setCurrentIndex(0)

            for cat in Mod.categories.values():
                cat.get('cat_check').setChecked(False)
            Mod.categories.get('').get('cat_check').setChecked(True)

            self.ui.btnSaveConfig.setEnabled(enabled)
            self.ui.editNameConfig.setEnabled(enabled)
            self.ui.cmbLoaderConfig.setEnabled(enabled)
            self.ui.tbtnCategoryConfig.setEnabled(enabled)

            self.ui.chkUpdated.setEnabled(enabled)
            self.ui.chkInstalledConfig.setEnabled(enabled)
            self.ui.chkIgnoredConfig.setEnabled(enabled)
            self.ui.chkFavoriteConfig.setEnabled(enabled)
            self.ui.chkBlockedConfig.setEnabled(enabled)

            self.ui.chkInstalledConfig.setChecked(False)
            self.ui.chkIgnoredConfig.setChecked(False)
            self.ui.chkUpdated.setChecked(False)
            self.ui.chkFavoriteConfig.setChecked(False)
            self.ui.chkBlockedConfig.setChecked(False)

            return enabled

        except Exception as e:
            Utils.print_exception('MAIN_WINDOW clear_selected', e)

    def select_mods(self):
        try:
            self.selectedMods = []

            for r in self.ui.tableMods.selectedRanges():
                for i in range(r.topRow(), r.bottomRow() + 1):
                    self.selectedMods.append(self.ui.tableMods.item(i, 0).mod)


            if self.clear_selected(len(self.selectedMods) > 0):

                self.ui.actionUpdateModInfo.setEnabled(True)
                self.ui.actionDeleteModDB.setEnabled(True)

                state = ModCompare(self.selectedMods, self.islist)

                self.ui.editNameConfig.setText(state.name)


                if state.loader is not None:
                    self.ui.cmbLoaderConfig.setCurrentIndex(self.ui.cmbLoaderConfig.findText(state.loader))
                else:
                    self.ui.cmbLoaderConfig.setCurrentIndex(0)


                if state.categories is not None:
                    for cat in state.categories.split(','):
                        Mod.categories.get(cat).get('cat_check').setChecked(True)
                        Mod.categories.get('').get('cat_check').setChecked(False)
                else:
                    Mod.categories.get('').get('cat_check').setChecked(True)


                if state.favorite is not None:
                    self.ui.chkFavoriteConfig.setTristate(False)
                    self.ui.chkFavoriteConfig.setChecked(bool(state.favorite))
                else:
                    self.ui.chkFavoriteConfig.setTristate(True)
                    self.ui.chkFavoriteConfig.setCheckState(Qt.PartiallyChecked)


                if state.blocked is not None:
                    self.ui.chkBlockedConfig.setTristate(False)
                    self.ui.chkBlockedConfig.setChecked(bool(state.blocked))
                else:
                    self.ui.chkBlockedConfig.setTristate(True)
                    self.ui.chkBlockedConfig.setCheckState(Qt.PartiallyChecked)


                if state.installed is not None:
                    self.ui.chkInstalledConfig.setTristate(False)
                    self.ui.chkInstalledConfig.setChecked(bool(state.installed))
                else:
                    self.ui.chkInstalledConfig.setTristate(True)
                    self.ui.chkInstalledConfig.setCheckState(Qt.PartiallyChecked)


                if state.ignored is not None:
                    self.ui.chkIgnoredConfig.setTristate(False)
                    self.ui.chkIgnoredConfig.setChecked(bool(state.ignored))
                else:
                    self.ui.chkIgnoredConfig.setTristate(True)
                    self.ui.chkIgnoredConfig.setCheckState(Qt.PartiallyChecked)


                if self.islist:
                    if state.updated is not None:
                        self.ui.chkUpdated.setTristate(False)
                        self.ui.chkUpdated.setEnabled(bool(state.updated))
                        self.ui.chkUpdated.setChecked(not bool(state.updated))
                    else:
                        self.ui.chkUpdated.setTristate(True)
                        self.ui.chkUpdated.setCheckState(Qt.PartiallyChecked)
                else:
                    self.ui.chkUpdated.setEnabled(False)
                    self.ui.chkUpdated.setChecked(False)

                for cat in Mod.categories:
                    Mod.categories.get(cat).get('cat_check').setChecked(False)
                Mod.categories.get('').get('cat_check').setChecked(True)
            else:
                self.ui.actionUpdateModInfo.setEnabled(False)
                self.ui.actionDeleteModDB.setEnabled(False)

            self.change_state_categories_config()

        except Exception as e:
            Utils.print_exception('MAIN_WINDOW select_mods', e)

    # ------------------------------------------

    def load_pages(self):
        try:
            q = QtSql.QSqlQuery()
            self.prepare_fill_table_query(q, count=True)
            if self.exec(q, 'load_pages') and q.next():
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
            Utils.print_exception('MAIN_WINDOW load_pages', e)

    def load_data(self):
        try:
            q = QtSql.QSqlQuery()
            self.tableMods.clear()
            self.prepare_fill_table_query(q)

            if self.exec(q, 'load_data'):
                # print(q.lastQuery())
                while q.next():
                    self.tableMods.append(Mod(q))

            self.fill_table()

        except Exception as e:
            Utils.print_exception('MAIN_WINDOW load_data', e)

    def fill_table(self):
        try:
            self.selectedMods = []
            self.clear_selected(False)

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

                    self.ui.tableMods.setItem(i, 1, TableItemName(mod, self.table_name_font))

                    self.ui.tableMods.setItem(i, 2, TableItemCategories(mod.categories))

                    self.ui.tableMods.setItem(i, 3, QtWidgets.QTableWidgetItem('  ' + mod.loader + '  '))
                    self.ui.tableMods.setItem(i, 4, QtWidgets.QTableWidgetItem(MainWindow.epoch_to_date(mod)))
                    self.ui.tableMods.setItem(i, 5, QtWidgets.QTableWidgetItem(self.get_state_icon(mod), ''))

                    self.ui.tableMods.item(i, 3).setTextAlignment(Qt.AlignCenter)
                    self.ui.tableMods.item(i, 3).setFont(self.table_others_font)

                    self.ui.tableMods.item(i, 4).setTextAlignment(Qt.AlignCenter)
                    self.ui.tableMods.item(i, 4).setFont(self.table_others_font)

            else:
                self.ui.lblActualPages.setText('0 / 0')

        except Exception as e:
            Utils.print_exception('MAIN_WINDOW fill_table', e)

    # ------------------------------------------

    def context_menu_table(self):
        try:
            if Qt.RightButton == QGuiApplication.mouseButtons():
                q = QtSql.QSqlQuery()
                top_menu = QMenu(self)

                menu = top_menu.addMenu("Menu")

                openlinks = QAction("Open Mod Links", self)
                openlinks.triggered.connect(self.table_open_links)
                menu.addAction(openlinks)


                addlist = menu.addMenu("Add to list...")

                q.prepare('select listname, loader from Lists;')
                actions = []
                if self.exec(q, 'context_menu_table'):
                    while q.next():
                        if q.value(0) != self.ui.cmbModList.currentText():
                            action = QAction(q.value(0), self)
                            action.triggered.connect(partial(self.table_add_list, q, q.value(0), q.value(1)))
                            actions.append(action)
                        elif not self.islist:
                            action = QAction(q.value(0), self)
                            action.triggered.connect(partial(self.table_add_list, q, q.value(0), q.value(1)))
                            actions.append(action)
                    addlist.addActions(actions)

                if self.islist:
                    delaction = QAction("Remove from list", self)
                    delaction.triggered.connect(partial(self.table_del_list, q))
                    menu.addAction(delaction)

                menu.addSeparator()

                autoinstall = QAction("Mark as Auto-Install", self)
                autoinstall.triggered.connect(partial(self.table_mark_autoinstall, q))
                menu.addAction(autoinstall)

                noautoinstall = QAction("Unmark as Auto-Install", self)
                noautoinstall.triggered.connect(partial(self.table_unmark_autoinstall, q))
                menu.addAction(noautoinstall)

                menu.addSeparator()

                autoignore = QAction("Mark as Auto-Ignore", self)
                autoignore.triggered.connect(partial(self.table_mark_autoignore, q))
                menu.addAction(autoignore)

                noautoignore = QAction("Unmark as Auto-Ignore", self)
                noautoignore.triggered.connect(partial(self.table_unmark_autoignore, q))
                menu.addAction(noautoignore)

                menu.exec_(QtGui.QCursor.pos())

        except Exception as e:
            Utils.print_exception('MAIN_WINDOW context_menu_table', e)  # , traceback.format_exc())

    def table_open_links(self):
        for mod in self.selectedMods:
            os.startfile(mod.path)


    def table_add_list(self, q, listname, loader):
        try:
            validloaders = [loader, 'No Loader', 'Forge | Fabric']
            for mod in self.selectedMods:
                if mod.loader not in validloaders:
                    WarningDialog('Cannot insert the selected mods in the list because one or\n more are not compatible with the list Loader.', confirmation_dialog=False).exec()
                    return

            if WarningDialog('Are you sure you want to insert ' + str(len(self.selectedMods)) + ' Mod/s in "' + listname + '" list?').exec():
                for mod in self.selectedMods:
                    mod.insert_in_list(q, listname)

        except Exception as e:
            Utils.print_exception('MAIN_WINDOW table_add_list', e)

    def table_del_list(self, q):
        try:
            if WarningDialog('Are you sure you want to remove ' + str(len(self.selectedMods)) + ' Mod/s from "' + self.ui.cmbModList.currentText() + '" list?').exec():
                for mod in self.selectedMods:
                    q.prepare('DELETE FROM ModsLists WHERE list == :list and mod == :mod;')
                    q.bindValue(':list', self.ui.cmbModList.currentText())
                    q.bindValue(':mod', mod.projectid)
                    self.exec(q, 'table_del_list')

                self.load_pages_maintain_slider()

        except Exception as e:
            Utils.print_exception('MAIN_WINDOW table_del_list', e)

    def table_mark_autoinstall(self, q):
        try:
            if WarningDialog('Are you sure you want to mark ' + str(len(self.selectedMods)) + ' Mod/s as Auto-Install?').exec():
                for mod in self.selectedMods:
                    q.prepare('UPDATE Mods SET autoinstall = 1, autoignore = 0 WHERE projectid == :projectid;')
                    q.bindValue(':projectid', mod.projectid)
                    self.exec(q, 'table_mark_autoinstall')

                self.load_pages_maintain_slider()

        except Exception as e:
            Utils.print_exception('MAIN_WINDOW table_mark_autoinstall', e)

    def table_unmark_autoinstall(self, q):
        try:
            if WarningDialog('Are you sure you want to unmark ' + str(len(self.selectedMods)) + ' Mod/s as Auto-Install?').exec():
                for mod in self.selectedMods:
                    q.prepare('UPDATE Mods SET autoinstall = 0 WHERE projectid == :projectid;')
                    q.bindValue(':projectid', mod.projectid)
                    self.exec(q, 'table_mark_autoinstall')

                self.load_pages_maintain_slider()

        except Exception as e:
            Utils.print_exception('MAIN_WINDOW table_unmark_autoinstall', e)

    def table_mark_autoignore(self, q):
        try:
            if WarningDialog('Are you sure you want to mark ' + str(len(self.selectedMods)) + ' Mod/s as Auto-Ignore?').exec():
                for mod in self.selectedMods:
                    q.prepare('UPDATE Mods SET autoinstall = 0, autoignore = 1 WHERE projectid == :projectid;')
                    q.bindValue(':projectid', mod.projectid)
                    self.exec(q, 'table_mark_autoignore')

                self.load_pages_maintain_slider()

        except Exception as e:
            Utils.print_exception('MAIN_WINDOW table_mark_autoignore', e)

    def table_unmark_autoignore(self, q):
        try:
            if WarningDialog('Are you sure you want to unmark ' + str(len(self.selectedMods)) + ' Mod/s as Auto-Ignore?').exec():
                for mod in self.selectedMods:
                    q.prepare('UPDATE Mods SET autoignore = 0 WHERE projectid == :projectid;')
                    q.bindValue(':projectid', mod.projectid)
                    self.exec(q, 'table_mark_autoignore')

                self.load_pages_maintain_slider()

        except Exception as e:
            Utils.print_exception('MAIN_WINDOW table_unmark_autoignore', e)







    '''
    ----------------------------------------------------------------------
    CONFIG WIDGETS
    ----------------------------------------------------------------------
    '''

    def save_configuration_mod(self):
        try:
            if len(self.selectedMods) > 0:
                q = QtSql.QSqlQuery()

                for mod in self.selectedMods:
                    self.update_mods_table(q, mod)

                    if self.ui.chkBlockedConfig.checkState() == Qt.Checked:
                        q.prepare('DELETE FROM ModsLists WHERE mod == :mod;')
                        q.bindValue(':mod', mod.projectid)
                        self.exec(q, 'save_configuration_mod')
                    elif self.islist:
                        self.update_modslists_table(q, mod)

                self.load_pages_maintain_slider()

        except Exception as e:
            Utils.print_exception('MAIN_WINDOW save_configuration_mod: ', e)

    def update_mods_table(self, q, mod):
        try:
            q.prepare('UPDATE Mods SET '
                      'loader = :loader, categories = :categories, '
                      'favorite = :favorite, blocked = :blocked, '
                      'newmod = 0, '
                      'autoinstall = :autoinstall, autoignore = :autoignore '
                      'WHERE projectid == :projectid;')
            q.bindValue(':projectid', mod.projectid)

            if self.ui.cmbLoaderConfig.currentIndex() != 0:
                q.bindValue(':loader', self.ui.cmbLoaderConfig.currentText())
            else:
                q.bindValue(':loader', mod.loader)

            if not Mod.categories.get('').get('cat_check').isChecked():
                q.bindValue(':categories', self.get_categories_from_checks())
            else:
                q.bindValue(':categories', mod.categories)

            if self.ui.chkFavoriteConfig.checkState() != Qt.PartiallyChecked:
                q.bindValue(':favorite', int(self.ui.chkFavoriteConfig.isChecked()))
            else:
                q.bindValue(':favorite', mod.favorite)

            if self.ui.chkBlockedConfig.checkState() != Qt.PartiallyChecked:
                q.bindValue(':blocked', int(self.ui.chkBlockedConfig.isChecked()))
            else:
                q.bindValue(':blocked', mod.blocked)

            if self.islist:
                q.bindValue(':autoinstall', mod.autoinstall)
                q.bindValue(':autoignore', mod.autoignore)
            else:
                if self.ui.chkInstalledConfig.checkState() != Qt.PartiallyChecked:
                    q.bindValue(':autoinstall', int(self.ui.chkInstalledConfig.isChecked()))
                else:
                    q.bindValue(':autoinstall', mod.autoinstall)

                if self.ui.chkIgnoredConfig.checkState() != Qt.PartiallyChecked:
                    q.bindValue(':autoignore', int(self.ui.chkIgnoredConfig.isChecked()))
                else:
                    q.bindValue(':autoignore', mod.autoignore)

            self.exec(q, 'update_modslists_table')

        except Exception as e:
            Utils.print_exception('MAIN_WINDOW update_mods_table: ', e)

    def update_modslists_table(self, q, mod):
        try:
            q.prepare(
                'UPDATE ModsLists SET  installed = :installed, ignored = :ignored, updated = :updated WHERE list == :list AND mod == :mod;')
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

            self.exec(q, 'update_modslists_table')

        except Exception as e:
            Utils.print_exception('MAIN_WINDOW update_modslists_table: ', e)

    # ------------------------------------------

    def resize_combobox_loader_config(self):
        try:
            self.ui.cmbLoaderConfig.insertSeparator(1)
            model = self.ui.cmbLoaderConfig.model()
            for i in range(model.rowCount()):
                model.setData(model.index(i, 0), QSize(0, 20), Qt.SizeHintRole)

        except Exception as e:
            Utils.print_exception('MAIN_WINDOW resize_combobox_loader: ', e)

    # ------------------------------------------

    def change_chk_installed(self):
        try:
            if self.ui.chkInstalledConfig.checkState() == Qt.Checked:
                if self.ui.chkIgnoredConfig.isChecked():
                    self.ui.chkIgnoredConfig.setChecked(False)
                if self.ui.chkBlockedConfig.isChecked():
                    self.ui.chkBlockedConfig.setChecked(False)

        except Exception as e:
            Utils.print_exception('MAIN_WINDOW change_chk_installed: ', e)

    def change_chk_ignored(self):
        try:
            if self.ui.chkIgnoredConfig.checkState() == Qt.Checked:
                if self.ui.chkInstalledConfig.isChecked():
                    self.ui.chkInstalledConfig.setChecked(False)
                if self.ui.chkBlockedConfig.isChecked():
                    self.ui.chkBlockedConfig.setChecked(False)

        except Exception as e:
            Utils.print_exception('MAIN_WINDOW change_chk_ignored: ', e)

    def change_chk_favorite(self):
        try:
            if self.ui.chkFavoriteConfig.checkState() == Qt.Checked:
                if self.ui.chkBlockedConfig.isChecked():
                    self.ui.chkBlockedConfig.setChecked(False)

        except Exception as e:
            Utils.print_exception('MAIN_WINDOW change_chk_favorite: ', e)

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
            Utils.print_exception('MAIN_WINDOW change_chk_blocked: ', e)






    '''
    ----------------------------------------------------------------------
    DIALOGS
    ----------------------------------------------------------------------
    '''

    def show_admin_categories_dialog(self):
        try:
            dialog = AdminCategoriesDialog()
            code = dialog.exec()

            if code == 1:
                self.load_categories()
                QCoreApplication.processEvents()
                self.load_pages_maintain_slider()

        except Exception as e:
            Utils.print_exception('MAIN_WINDOW show_admin_list_dialog: ', e)

    def show_admin_list_dialog(self):
        try:
            dialog = AdminListDialog()
            code = dialog.exec()

            if code == 1:
                self.create_cmb_values_lists()
                self.ui.cmbModList.setCurrentIndex(1)
                self.ui.cmbModList.setCurrentIndex(0)

        except Exception as e:
            Utils.print_exception('MAIN_WINDOW show_admin_list_dialog: ', e)

    def show_searching_dialog(self):
        try:
            listname = None
            if self.islist:
                listname = self.ui.cmbModList.currentText()

            dialog = SearchingDialog(listname)
            if dialog.exec():
                loader = dialog.ui.cmbModList.currentText()
                if loader != self.ui.cmbModList.currentText():
                    self.ui.cmbModList.setCurrentIndex(self.ui.cmbModList.findText(loader))
                else:
                    self.load_pages()

        except Exception as e:
            Utils.print_exception('MAIN_WINDOW show_searching_dialog: ', e)

    def show_copylist_dialog(self):
        try:
            listname = None
            if self.islist:
                listname = self.ui.cmbModList.currentText()

            dialog = CopyListDialog(listname)
            editname = dialog.ui.editNameCopy
            code = dialog.exec()

            if code == 1:
                self.create_cmb_values_lists()
                self.ui.cmbModList.setCurrentIndex(self.ui.cmbModList.findText(editname.text()))

        except Exception as e:
            Utils.print_exception('MAIN_WINDOW show_copylist_dialog: ', e)


    def show_search_modid_dialog(self):
        try:
            dialog = SearchingModIdDialog()
            code = dialog.exec()

            if code == 1:
                self.load_pages_maintain_slider()

        except Exception as e:
            Utils.print_exception('MAIN_WINDOW show_search_modid_dialog: ', e)






    '''
    ----------------------------------------------------------------------
    UTILITIES
    ----------------------------------------------------------------------
    '''

    def set_islist(self):
        self.islist = 1 < self.ui.cmbModList.currentIndex() < self.ui.cmbModList.count() - 4

    @staticmethod
    def get_categories_from_checks():
        try:
            c = []
            for cat in Mod.categories.values():
                if cat.get('cat_check').isChecked():
                    c.append(cat.get('cat_id'))
            c.sort()
            return ",".join(c)

        except Exception as e:
            Utils.print_exception('MAIN_WINDOW get_categories_from_checks: ', e)

    def get_loader(self):
        try:
            if self.ui.actionNoLoader.isChecked():
                return 'No Loader'
            elif self.ui.actionForgeLoader.isChecked():
                return 'Forge'
            elif self.ui.actionFabricLoader.isChecked():
                return 'Fabric'
            elif self.ui.actionForgeFabricLoader.isChecked():
                return 'Forge | Fabric'

        except Exception as e:
            Utils.print_exception('MAIN_WINDOW get_loader: ', e)

    def get_state_icon(self, mod):
        try:
            state = ''

            if mod.updated:
                state += 'u'

            if mod.blocked:
                return self.state_icons[state + 'b']
            else:

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

        except Exception as e:
            Utils.print_exception('MAIN_WINDOW get_state_icon: ', e)

    def load_pages_maintain_slider(self):
        try:
            current_page = self.current_page
            scroll = self.ui.tableMods.verticalScrollBar().sliderPosition()
            self.load_pages()
            if current_page == self.current_page:
                QCoreApplication.processEvents()
                self.ui.tableMods.verticalScrollBar().setSliderPosition(scroll)

        except Exception as e:
            Utils.print_exception('MAIN_WINDOW save_configuration_mod: ', e)

    @staticmethod
    def epoch_to_date(mod: Mod):
        try:
            return '  ' + time.strftime('%d/%m/%Y', time.localtime(mod.update_date)) + '  '
        except ValueError:
            return '  -  '

    # ------------------------------------------

    @staticmethod
    def create_font_table_name():
        try:
            f = QFont()
            f.setBold(True)
            f.setPixelSize(18)
            return f

        except Exception as e:
            Utils.print_exception('MAIN_WINDOW create_bold_font: ', e)

    @staticmethod
    def create_font_table_others():
        try:
            f = QFont()
            f.setBold(True)
            f.setPointSize(10)
            return f

        except Exception as e:
            Utils.print_exception('MAIN_WINDOW create_bold_font: ', e)

    @staticmethod
    def create_state_icons():
        try:
            return {
                'e': IconUtils.getNormalIcon(":/state/state/empty.png"),

                'f': IconUtils.getNormalIcon(":/states/states/favorite.png"),

                'b': IconUtils.getNormalIcon(":/states/states/blocked.png"),
                'ub': IconUtils.getNormalIcon(":/states/states/updated_blocked.png"),

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

        except Exception as e:
            Utils.print_exception('MAIN_WINDOW create_state_icons: ', e)

    # ------------------------------------------

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
            elif isinstance(value, int):
                return prefix + tableas + field + condition + str(value) + ' '
            else:
                return ' '

        except Exception as e:
            Utils.print_exception('MAIN_WINDOW optional_filter: ', e)

    @staticmethod
    def exec(q, msg=''):
        try:
            b = q.exec_()
            if b is False:
                print(q.lastError().text())
            return b

        except Exception as e:
            Utils.print_exception('MAIN_WINDOW exec ' + msg + ':', e)
