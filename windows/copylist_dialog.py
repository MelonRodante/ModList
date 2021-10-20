from PyQt5 import QtWidgets, QtCore, QtSql
from PyQt5.QtCore import QSize, Qt

from pyqt_windows.copylist_dialog import Ui_CopyListDialog


class CopyListDialog(QtWidgets.QDialog):

    def __init__(self):
        super(CopyListDialog, self).__init__()
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
        self.ui = Ui_CopyListDialog()
        self.ui.setupUi(self)

        self.lists = []

        self.exitcode = 0
        self.setupWidgets()
        self.setupEvents()
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

            self.lists = ['', '-']
            if q.exec_():
                while q.next():
                    self.lists.append(q.value(0))
                    self.ui.cmbListCopy.addItem(q.value(0), '( ' + q.value(1) + ' | ' + q.value(2) + ' )')

            model = self.ui.cmbListCopy.model()
            for i in range(model.rowCount()):
                model.setData(model.index(i, 0), QSize(0, 20), QtCore.Qt.SizeHintRole)
        except Exception as e:
            print('COPYLIST_DIALOG setup_cmb:', e)

    # ------------------------------------------------------------------------------------------------------------------

    def setupEvents(self):
        pass

    def btn_copy_list(self):
        self.done(1)