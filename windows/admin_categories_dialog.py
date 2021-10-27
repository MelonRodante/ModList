import PyQt5
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt, QSize, QRectF
from PyQt5.QtGui import QIcon, QPixmap, QPainter
from PyQt5.QtWidgets import QFileDialog
from qtpy import QtSql

from pyqt_windows.category_list_dialog import Ui_AdminCategoriesDialog
from utils.icon_utils import IconUtils


class AdminCategoriesDialog(QtWidgets.QDialog):

    def __init__(self):
        super(AdminCategoriesDialog, self).__init__()
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
        self.ui = Ui_AdminCategoriesDialog()
        self.ui.setupUi(self)

        self.pixmap = None

        self.exitcode = 0
        self.setupWidgets()
        self.setupEvents()
        self.fill_table()
        self.show()

    # ------------------------------------------------------------------------------------------------------------------

    def setupWidgets(self):
        try:
            self.modify_table()
            self.modify_css()
        except Exception as e:
            print('ADMIN_CATEGORIES_DIALOG setupWidgets:', e)

    def modify_table(self):
        try:
            self.ui.tableCategories.setIconSize(QSize(24, 24))
            self.ui.tableCategories.setColumnWidth(0, 25)

            header = self.ui.tableCategories.horizontalHeader()
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
            header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        except Exception as e:
            print('ADMIN_CATEGORIES_DIALOG modify_table:', e)

    def modify_css(self):
        try:
            f = self.ui.tableCategories.horizontalHeader().font()
            f.setBold(True)
            self.ui.tableCategories.horizontalHeader().setFont(f)
        except Exception as e:
            print('ADMIN_CATEGORIES_DIALOG modify_css:', e)

    # ------------------------------------------------------------------------------------------------------------------

    def setupEvents(self):
        try:
            self.ui.editCategoryName.textChanged.connect(self.change_editname)
            self.ui.btnIcon.clicked.connect(self.btn_icon)
            self.ui.btnAddSave.clicked.connect(self.add_category)
        except Exception as e:
            print('ADMIN_CATEGORIES_DIALOG setupEvents:', e)

    def change_editname(self):
        try:
            if self.ui.editCategoryName.text() and not self.ui.editCategoryName.text().isspace():
                name = " ".join(self.ui.editCategoryName.text().strip().split())

                cat_id = ''
                for letter in name:
                    if letter.isalpha():
                        cat_id += letter.lower()
                    elif letter == ' ':
                        cat_id += '-'
                cat_id = '-mlc-' + cat_id
                self.ui.editCategoryID.setText(cat_id)

                find = False
                for i in range(self.ui.tableCategories.rowCount()):
                    if cat_id == self.ui.tableCategories.item(i, 1).text().strip():
                        find = True
                        break

                self.ui.btnAddSave.setDisabled(find)
                self.ui.btnRemove.setEnabled(find)
            else:
                self.ui.btnAddSave.setEnabled(False)
                self.ui.btnRemove.setEnabled(False)

        except Exception as e:
            print('ADMIN_CATEGORIES_DIALOG change_editname:', e)

    def btn_icon(self):
        try:
            fname = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\', "Image files (*.png)")
            self.pixmap = QPixmap(fname[0]).scaled(24, 24, Qt.KeepAspectRatio)

            painter = QPainter(self.pixmap)

            px = QPixmap(':/categories/categories/cat_border.png')
            painter.drawPixmap(QRectF(0, 0, 24, 24), px, QRectF(px.rect()))

            self.ui.btnIcon.setIcon(QIcon(self.pixmap))
            self.ui.btnIcon.setText('')
        except Exception as e:
            print('ADMIN_CATEGORIES_DIALOG btn_icon:', e)

    def add_category(self):
        try:
            q = QtSql.QSqlQuery()
            q.prepare('INSERT INTO Categories(cat_id, cat_name, grp, ord, icon) VALUES (:cat_id, :cat_name, :grp, :ord, :icon)')
            q.bindValue(':cat_id', self.ui.editCategoryID.text())
            q.bindValue(':cat_name', " ".join(self.ui.editCategoryName.text().strip().split()))
            q.bindValue(':grp', self.ui.spinGroup.value() + 100)
            q.bindValue(':ord', self.ui.spinOrder.value())

            q.bindValue(':icon', IconUtils.pixmap_to_qbytearray(self.pixmap))

            if q.exec():
                self.pixmap = None
                self.ui.btnIcon.setIcon(QIcon())
                self.ui.btnIcon.setText('24x24')

                self.ui.editCategoryName.setText('')
                self.ui.editCategoryID.setText('')
                self.ui.spinGroup.setValue(1)
                self.ui.spinOrder.setValue(1)
                self.fill_table()
                self.exitcode = 1
        except Exception as e:
            print('ADMIN_CATEGORIES_DIALOG add_category:', e)

    def fill_table(self):
        try:
            q = QtSql.QSqlQuery()
            q.prepare('SELECT icon, cat_id, cat_name, grp, ord FROM Categories WHERE grp > 100;')

            categories = []
            self.ui.tableCategories.setRowCount(0)
            if q.exec_():
                while q.next():
                    categories.append([IconUtils.qbytearray_to_pixmap(q.value(0)), q.value(1), q.value(2), q.value(3), q.value(4)])
            else:
                print('ADMIN_CATEGORIES_DIALOG fill_table query:', q.lastError().text())

            self.ui.tableCategories.setRowCount(len(categories))
            for i, cat in enumerate(categories):
                self.ui.tableCategories.setItem(i, 0, QtWidgets.QTableWidgetItem(IconUtils.getNormalIcon(cat[0]), ''))
                self.ui.tableCategories.setItem(i, 1, QtWidgets.QTableWidgetItem('  ' + cat[1] + '  '))
                self.ui.tableCategories.setItem(i, 2, QtWidgets.QTableWidgetItem('  ' + cat[2] + '  '))
                self.ui.tableCategories.setItem(i, 3, QtWidgets.QTableWidgetItem('  ' + str(cat[3]) + '  '))
                self.ui.tableCategories.setItem(i, 4, QtWidgets.QTableWidgetItem('  ' + str(cat[4]) + '  '))

                self.ui.tableCategories.item(i, 0).setTextAlignment(Qt.AlignCenter)
                # self.ui.tableCategories.item(i, 1).setTextAlignment(Qt.AlignCenter)
                self.ui.tableCategories.item(i, 3).setTextAlignment(Qt.AlignCenter)
                self.ui.tableCategories.item(i, 4).setTextAlignment(Qt.AlignCenter)


        except Exception as e:
            print('ADMIN_CATEGORIES_DIALOG fill_table:', e)

    def closeEvent(self, evnt):
        try:
            self.done(self.exitcode)
        except Exception as e:
            print('ADMIN_LIST_DIALOG closeEvent:', e)