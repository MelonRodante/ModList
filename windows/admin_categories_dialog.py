from PyQt5 import QtWidgets, QtSql
from PyQt5.QtCore import Qt, QSize, QRectF
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QFont
from PyQt5.QtWidgets import QFileDialog

from pyqt_windows.category_list_dialog import Ui_AdminCategoriesDialog
from utils.icon_utils import IconUtils
from utils.utils import Utils
from windows.warning_dialog import WarningDialog


class AdminCategoriesDialog(QtWidgets.QDialog):

    def __init__(self):
        super(AdminCategoriesDialog, self).__init__()
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
        self.ui = Ui_AdminCategoriesDialog()
        self.ui.setupUi(self)

        self.last_path = 'c:\\'

        self.pixmap = None
        self.font = AdminCategoriesDialog.create_font_table()

        self.exitcode = 0
        self.setupWidgets()
        self.setupEvents()
        self.fill_table()
        self.show()

    @staticmethod
    def create_font_table():
        try:
            f = QFont()
            f.setBold(True)
            f.setPointSize(11)
            return f

        except Exception as e:
            Utils.print_exception('ADMIN_CATEGORIES_DIALOG create_bold_font', e)

    # ------------------------------------------------------------------------------------------------------------------

    def setupWidgets(self):
        try:
            self.modify_table()
            self.modify_css()

        except Exception as e:
            Utils.print_exception('ADMIN_CATEGORIES_DIALOG setupWidgets', e)

    def modify_table(self):
        try:
            header = self.ui.tableCategories.horizontalHeader()
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
            header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)

            self.ui.tableCategories.setIconSize(QSize(48, 48))
            self.ui.tableCategories.setColumnWidth(0, 58)
        except Exception as e:
            Utils.print_exception('ADMIN_CATEGORIES_DIALOG modify_table', e)

    def modify_css(self):
        try:
            f = self.ui.tableCategories.horizontalHeader().font()
            f.setBold(True)
            self.ui.tableCategories.horizontalHeader().setFont(f)
        except Exception as e:
            Utils.print_exception('ADMIN_CATEGORIES_DIALOG modify_css', e)

    # ------------------------------------------------------------------------------------------------------------------

    def setupEvents(self):
        try:
            self.ui.editCategoryID.textChanged.connect(self.change_editcatid)

            self.ui.btnGenerateCatID.clicked.connect(self.btn_generate_id)
            self.ui.btnIcon.clicked.connect(self.btn_icon)

            self.ui.btnAdd.clicked.connect(self.add_category)
            self.ui.btnModify.clicked.connect(self.modify_category)
            self.ui.btnRemove.clicked.connect(self.remove_category)

            self.ui.tableCategories.itemSelectionChanged.connect(self.table_selection)
        except Exception as e:
            Utils.print_exception('ADMIN_CATEGORIES_DIALOG setupEvents', e)

    def change_editcatid(self):
        try:
            if self.ui.editCategoryID.text() and not self.ui.editCategoryID.text().isspace():
                find = False
                for i in range(self.ui.tableCategories.rowCount()):
                    if self.ui.editCategoryID.text() == self.ui.tableCategories.item(i, 1).text().strip():
                        find = True
                        break

                self.ui.btnAdd.setDisabled(find)
                self.ui.btnModify.setEnabled(find)
                self.ui.btnRemove.setEnabled(find)
            else:
                self.ui.btnAdd.setEnabled(False)
                self.ui.btnModify.setEnabled(False)
                self.ui.btnRemove.setEnabled(False)
        except Exception as e:
            Utils.print_exception('ADMIN_CATEGORIES_DIALOG change_editcatid', e)

    def btn_icon(self):
        try:
            fname = QFileDialog.getOpenFileName(self, 'Open file', self.last_path, "Image files (*.png)")
            if fname[0]:
                self.last_path = fname[0]

                self.pixmap = QPixmap(fname[0]).scaled(48, 48, Qt.KeepAspectRatio)

                painter = QPainter(self.pixmap)

                px = QPixmap(':/categories/categories/cat_border.png')
                painter.drawPixmap(QRectF(0, 0, 48, 48), px, QRectF(px.rect()))

                self.ui.btnIcon.setIcon(QIcon(self.pixmap))
                self.ui.btnIcon.setText('')

        except Exception as e:
            Utils.print_exception('ADMIN_CATEGORIES_DIALOG btn_icon', e)

    def btn_generate_id(self):
        try:
            if self.ui.editCategoryName.text() and not self.ui.editCategoryName.text().isspace():
                name = " ".join(self.ui.editCategoryName.text().strip().split())

                cat_id = ''
                for letter in name:
                    if letter.isalpha():
                        cat_id += letter.lower()
                    elif letter == ' ':
                        cat_id += '-'
                if cat_id and not cat_id.isspace():
                    if cat_id[-1] == '-':
                        cat_id = cat_id[:-1]

                    self.ui.editCategoryID.setText('-mlc-' + cat_id)
                else:
                    self.ui.editCategoryID.setText('')
            else:
                self.ui.editCategoryID.setText('')

        except Exception as e:
            Utils.print_exception('ADMIN_CATEGORIES_DIALOG btn_generate_id', e)

    def add_category(self):
        try:
            q = QtSql.QSqlQuery()
            q.prepare(
                'INSERT INTO Categories(cat_id, cat_name, grp, ord, icon) VALUES (:cat_id, :cat_name, :grp, :ord, :icon)')
            q.bindValue(':cat_id', self.ui.editCategoryID.text())
            q.bindValue(':cat_name', " ".join(self.ui.editCategoryName.text().strip().split()))
            q.bindValue(':grp', self.ui.spinGroup.value() + 100)
            q.bindValue(':ord', self.ui.spinOrder.value())

            q.bindValue(':icon', IconUtils.pixmap_to_qbytearray(self.pixmap))

            if q.exec():
                self.pixmap = None
                self.ui.btnIcon.setIcon(QIcon())
                self.ui.btnIcon.setText('48x48')

                self.ui.editCategoryName.setText('')
                self.ui.editCategoryID.setText('')
                self.ui.spinGroup.setValue(1)
                self.ui.spinOrder.setValue(1)
                self.fill_table()
                self.exitcode = 1

        except Exception as e:
            Utils.print_exception('ADMIN_CATEGORIES_DIALOG add_category', e)

    def modify_category(self):
        try:
            icon_update = ''
            if self.pixmap is not None:
                icon_update = ', icon = :icon '

            q = QtSql.QSqlQuery()
            q.prepare('UPDATE Categories SET cat_name = :cat_name, grp = :grp, ord = :ord' + icon_update + ' WHERE cat_id == :cat_id;')
            q.bindValue(':cat_id', self.ui.editCategoryID.text())
            q.bindValue(':cat_name', " ".join(self.ui.editCategoryName.text().strip().split()))
            q.bindValue(':grp', self.ui.spinGroup.value() + 100)
            q.bindValue(':ord', self.ui.spinOrder.value())

            if self.pixmap is not None:
                q.bindValue(':icon', IconUtils.pixmap_to_qbytearray(self.pixmap))

            if q.exec():
                self.pixmap = None
                self.ui.btnIcon.setIcon(QIcon())
                self.ui.btnIcon.setText('48x48')

                self.ui.editCategoryName.setText('')
                self.ui.editCategoryID.setText('')
                self.ui.spinGroup.setValue(1)
                self.ui.spinOrder.setValue(1)
                self.fill_table()
                self.exitcode = 1
            else:
                print('ADMIN_CATEGORIES_DIALOG modify_category query:', q.lastError().text())

        except Exception as e:
            Utils.print_exception('ADMIN_CATEGORIES_DIALOG modify_category', e)

    def remove_category(self):
        try:
            q = QtSql.QSqlQuery()
            q.prepare('SELECT projectid, categories FROM Mods WHERE categories LIKE :categories')
            q.bindValue(':categories', '%' + self.ui.editCategoryID.text() + '%')

            if q.exec():
                in_use_cat = False
                while q.next() and in_use_cat is False:
                    for cat in q.value(1).split(','):
                        if self.ui.editCategoryID.text() == cat:
                            in_use_cat = True
                            break

                if in_use_cat:
                    WarningDialog('It is not possible to delete the category because\nit is being used in one or more mods.', confirmation_dialog=False).exec()
                else:
                    q.prepare('DELETE FROM Categories WHERE cat_id == :cat_id;')
                    q.bindValue(':cat_id', self.ui.editCategoryID.text())
                    if not q.exec():
                        print('ADMIN_CATEGORIES_DIALOG remove_category query delete:', q.lastError().text())
                    else:
                        self.fill_table()

            else:
                print('ADMIN_CATEGORIES_DIALOG remove_category query:', q.lastError().text())
                print(q.lastQuery())

        except Exception as e:
            Utils.print_exception('ADMIN_CATEGORIES_DIALOG remove_category', e)

    def table_selection(self):
        try:
            if len(self.ui.tableCategories.selectedItems()) > 0:
                self.pixmap = None
                self.ui.btnIcon.setIcon(self.ui.tableCategories.selectedItems()[0].icon())
                self.ui.btnIcon.setText('')

                self.ui.editCategoryID.setText(self.ui.tableCategories.selectedItems()[1].text().strip())
                self.ui.editCategoryName.setText(self.ui.tableCategories.selectedItems()[2].text().strip())
                self.ui.spinGroup.setValue(int(self.ui.tableCategories.selectedItems()[3].text()))
                self.ui.spinOrder.setValue(int(self.ui.tableCategories.selectedItems()[4].text()))
            else:
                self.pixmap = None
                self.ui.btnIcon.setIcon(QIcon())
                self.ui.btnIcon.setText('48x48')

                self.ui.editCategoryName.setText('')
                self.ui.editCategoryID.setText('')
                self.ui.spinGroup.setValue(1)
                self.ui.spinOrder.setValue(1)

        except Exception as e:
            Utils.print_exception('ADMIN_CATEGORIES_DIALOG table_selection', e)

    def fill_table(self):
        try:
            q = QtSql.QSqlQuery()
            q.prepare('SELECT icon, cat_id, cat_name, grp, ord FROM Categories WHERE grp > 100 ORDER BY grp ASC, ord ASC, cat_name ASC;')

            categories = []
            self.ui.tableCategories.setRowCount(0)
            if q.exec_():
                while q.next():
                    categories.append(
                        [IconUtils.qbytearray_to_pixmap(q.value(0)), q.value(1), q.value(2), q.value(3), q.value(4)])
            else:
                print('ADMIN_CATEGORIES_DIALOG fill_table query:', q.lastError().text())

            self.ui.tableCategories.setRowCount(len(categories))
            for i, cat in enumerate(categories):
                self.ui.tableCategories.setItem(i, 0, QtWidgets.QTableWidgetItem(IconUtils.getNormalIcon(cat[0]), ''))
                self.ui.tableCategories.setItem(i, 1, QtWidgets.QTableWidgetItem('  ' + cat[1] + '  '))
                self.ui.tableCategories.setItem(i, 2, QtWidgets.QTableWidgetItem('  ' + cat[2] + '  '))
                self.ui.tableCategories.setItem(i, 3, QtWidgets.QTableWidgetItem('  ' + str(cat[3]-100) + '  '))
                self.ui.tableCategories.setItem(i, 4, QtWidgets.QTableWidgetItem('  ' + str(cat[4]) + '  '))

                self.ui.tableCategories.item(i, 0).setTextAlignment(Qt.AlignCenter)
                # self.ui.tableCategories.item(i, 1).setTextAlignment(Qt.AlignCenter)
                self.ui.tableCategories.item(i, 3).setTextAlignment(Qt.AlignCenter)
                self.ui.tableCategories.item(i, 4).setTextAlignment(Qt.AlignCenter)

                self.ui.tableCategories.item(i, 1).setFont(self.font)
                self.ui.tableCategories.item(i, 2).setFont(self.font)
                self.ui.tableCategories.item(i, 3).setFont(self.font)
                self.ui.tableCategories.item(i, 4).setFont(self.font)

        except Exception as e:
            Utils.print_exception('ADMIN_CATEGORIES_DIALOG fill_table', e)

    def closeEvent(self, evnt):
        try:
            self.done(self.exitcode)

        except Exception as e:
            Utils.print_exception('ADMIN_LIST_DIALOG closeEvent', e)
