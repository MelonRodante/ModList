from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QSize, Qt
from qtpy import QtSql

from pyqt_windows.searching_dialog import Ui_SearchingDialog


class SearchingDialog(QtWidgets.QDialog):

    def __init__(self):
        super(SearchingDialog, self).__init__()
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
        self.ui = Ui_SearchingDialog()
        self.ui.setupUi(self)

        self.setupWidgets()
        self.setupEvents()
        self.show()

    def setupWidgets(self):
        self.modify_css()
        self.create_cmb_values_lists()

    def modify_css(self):
        self.ui.btnSearchNewMods.setStyleSheet('QPushButton {border: 1px solid #F0651F; background-color: #0F1A25;} '
                                               'QPushButton:hover {background-color: #19232D;}'
                                               'QPushButton:pressed {background-color: #54687A;}'
                                               'QPushButton:disabled {border: 1px solid #000000;}')

    def create_cmb_values_lists(self):
        q = QtSql.QSqlQuery()
        q.prepare('select list from Lists')

        self.ui.cmbModList.clear()

        self.ui.cmbModList.addItem('')
        self.ui.cmbModList.insertSeparator(self.ui.cmbModList.count())

        if q.exec_():
            while q.next():
                self.ui.cmbModList.addItem(q.value(0))

            model = self.ui.cmbModList.model()
            for i in range(model.rowCount()):
                model.setData(model.index(i, 0), QSize(0, 20), QtCore.Qt.SizeHintRole)

    def setupEvents(self):
        self.ui.cmbModList.currentIndexChanged.connect(self.change_cmb_modlist)

    def change_cmb_modlist(self):
        self.ui.btnSearchNewMods.setEnabled(self.ui.cmbModList.currentIndex() > 1)