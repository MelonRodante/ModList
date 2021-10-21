from PyQt5 import QtWidgets, QtCore, QtSql
from PyQt5.QtCore import QSize, Qt

from pyqt_windows.copylist_dialog import Ui_CopyListDialog
from utils.database import Database


class CopyListDialog(QtWidgets.QDialog):

    def __init__(self, list):
        super(CopyListDialog, self).__init__()
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
        self.ui = Ui_CopyListDialog()
        self.ui.setupUi(self)

        self.lists = {}

        self.exitcode = 0
        self.setupWidgets()
        self.setupEvents()

        if list is not None:
            for i, l in enumerate(self.lists):
                if list == l:
                    self.ui.cmbListCopy.setCurrentIndex(i)

        self.show()

    # ------------------------------------------------------------------------------------------------------------------

    def setupWidgets(self):
        self.setup_cmb()

    def setup_cmb(self):
        try:
            q = QtSql.QSqlQuery()
            q.prepare('SELECT listname, version, loader FROM Lists;')

            self.ui.cmbListCopy.clear()
            self.ui.cmbListCopy.addItem('')
            if self.ui.cmbListCopy.count() >= 1:
                self.ui.cmbListCopy.insertSeparator(self.ui.cmbListCopy.count())

            self.lists = {'': ['-', '-']}
            if q.exec_():
                while q.next():
                    self.lists[q.value(0)] = [q.value(1), q.value(2)]
                    self.ui.cmbListCopy.addItem(q.value(0))

            model = self.ui.cmbListCopy.model()
            for i in range(model.rowCount()):
                model.setData(model.index(i, 0), QSize(0, 20), Qt.SizeHintRole)
        except Exception as e:
            print('COPYLIST_DIALOG setup_cmb:', e)

    # ------------------------------------------------------------------------------------------------------------------

    def setupEvents(self):
        self.ui.editNameCopy.editingFinished.connect(lambda: self.ui.editNameCopy.setText(" ".join(self.ui.editNameCopy.text().strip().split())))

        self.ui.editNameCopy.textChanged.connect(self.valid_data)
        self.ui.cmbListCopy.currentIndexChanged.connect(self.change_cmb)

        self.ui.btnCopy.clicked.connect(self.btn_copy_list)

    def change_cmb(self):
        version, loader = self.lists[self.ui.cmbListCopy.currentText()]
        self.ui.lblVersion.setText(version)
        self.ui.lblLoader.setText(loader)
        self.valid_data()

    def valid_data(self):
        self.ui.btnCopy.setEnabled(self.ui.cmbListCopy.currentIndex() > 0 and self.valid_copy_name())

    def valid_copy_name(self):
        if self.ui.editNameCopy.text() and not self.ui.editNameCopy.text().isspace():
            q = QtSql.QSqlQuery()
            q.prepare('SELECT listname FROM Lists WHERE listname == :listname;')
            q.bindValue(':listname', " ".join(self.ui.editNameCopy.text().strip().split()))
            if q.exec():
                if q.next():
                    return False
                else:
                    return True
            else:
                return False
        else:
            return False

    def btn_copy_list(self):
        Database.db.transaction()
        q = QtSql.QSqlQuery()

        cmbvalue = self.lists[self.ui.cmbListCopy.currentIndex()]

        q.prepare('SELECT version, loader FROM Lists WHERE listname == :listname;')
        q.bindValue(':listname', cmbvalue)
        if q.exec():
            if q.next():
                version = q.value(0)
                loader = q.value(1)

                q.prepare('INSERT INTO Lists(listname, version, loader) VALUES (:listname, :version, :loader);')
                q.bindValue(':listname', " ".join(self.ui.editNameCopy.text().strip().split()))
                q.bindValue(':version', version)
                q.bindValue(':loader', loader)

                if q.exec():
                    q.prepare('INSERT INTO ModsLists(list, mod, installed, ignored, updated) SELECT :newlist, mod, installed, ignored, updated FROM ModsLists WHERE list == :list')
                    q.bindValue(':newlist', " ".join(self.ui.editNameCopy.text().strip().split()))
                    q.bindValue(':list', cmbvalue)

                    if q.exec():
                        Database.db.commit()
                        self.done(1)
                    else:
                        Database.db.commit()
                        self.done(0)

                else:
                    Database.db.commit()
                    self.done(0)
            else:
                Database.db.commit()
                self.done(0)

        else:
            Database.db.commit()
            self.done(0)