from time import sleep

from PyQt5 import QtWidgets, QtSql
from PyQt5.QtCore import QSize, Qt

from pyqt_windows.searching_dialog import Ui_SearchingDialog
from utils.searchthread import SearchThread
from utils.utils import Utils


class SearchingDialog(QtWidgets.QDialog):

    def __init__(self, list):
        super(SearchingDialog, self).__init__()
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
        self.ui = Ui_SearchingDialog()
        self.ui.setupUi(self)

        self.exit_code = 0
        self.search_thread = None

        self.setupWidgets()
        self.setupEvents()

        if list is not None:
            self.ui.cmbModList.setCurrentIndex(self.ui.cmbModList.findText(list))
            self.ui.chkSeachNewUpdate.setChecked(True)

        self.show()

    def setupWidgets(self):
        try:
            self.create_cmb_values_lists()

        except Exception as e:
            Utils.print_exception('SEARCHING_DIALOG setupWidgets', e)

    def create_cmb_values_lists(self):
        try:
            q = QtSql.QSqlQuery()
            q.prepare('select listname from Lists')

            self.ui.cmbModList.clear()
            self.ui.cmbModList.addItem('')

            if q.exec_():
                while q.next():
                    self.ui.cmbModList.addItem(q.value(0))

            if self.ui.cmbModList.count() > 1:
                self.ui.cmbModList.insertSeparator(1)

            model = self.ui.cmbModList.model()
            for i in range(model.rowCount()):
                model.setData(model.index(i, 0), QSize(0, 20), Qt.SizeHintRole)

        except Exception as e:
            Utils.print_exception('SEARCHING_DIALOG create_cmb_values_lists', e)

    def setupEvents(self):
        try:
            self.ui.cmbModList.currentIndexChanged.connect(self.change_cmb_modlist)
            self.ui.btnSearchNewMods.clicked.connect(self.btn_search_mods)

        except Exception as e:
            Utils.print_exception('SEARCHING_DIALOG setupEvents', e)

    def change_cmb_modlist(self):
        try:
            self.ui.btnSearchNewMods.setEnabled(self.ui.cmbModList.currentIndex() > 0)

        except Exception as e:
            Utils.print_exception('SEARCHING_DIALOG change_cmb_modlist', e)

    def btn_search_mods(self):
        try:
            self.ui.progressBar.setEnabled(True)
            self.ui.progressBar.setMaximum(0)

            self.ui.cmbModList.setEnabled(False)
            self.ui.chkSeachNewUpdate.setEnabled(False)
            self.ui.btnSearchNewMods.setEnabled(False)

            self.search_thread = SearchThread(self.ui.cmbModList.currentText(), self.ui.chkSeachNewUpdate.isChecked())

            self.search_thread.sig_max_pages.connect(self.set_max_pages)
            self.search_thread.sig_page_finish.connect(self.set_page_finish)
            self.search_thread.sig_finish_code.connect(self.set_finish_code)
            self.search_thread.finished.connect(self.set_finish_search)

            self.search_thread.start()

        except Exception as e:
            Utils.print_exception('SEARCHING_DIALOG btn_search_mod', e)

    def set_max_pages(self, max_pages):
        try:
            self.ui.progressBar.setValue(0)
            self.ui.progressBar.setMaximum(max_pages)
            self.ui.progressBar.setFormat('Buscando Mods... (%m Encontrados)')

        except Exception as e:
            Utils.print_exception('SEARCHING_DIALOG set_max_pages', e)

    def set_page_finish(self, page_finish):
        try:
            self.ui.progressBar.setValue(page_finish)
            self.ui.progressBar.setFormat('%v/%m Procesados')

        except Exception as e:
            Utils.print_exception('SEARCHING_DIALOG set_page_finish', e)

    def set_finish_search(self):
        try:
            if self.exit_code == 0:
                self.ui.progressBar.setValue(self.ui.progressBar.maximum())
                sleep(1)
                self.done(1)
            else:
                self.done(2)

        except Exception as e:
            Utils.print_exception('SEARCHING_DIALOG set_finish_search', e)

    def set_finish_code(self, code):
        self.exit_code = code

    def closeEvent(self, event):
        try:
            if self.search_thread is not None:
                self.search_thread.set_close()
                self.ui.progressBar.setFormat('Cancelando...')
                event.ignore()

        except Exception as e:
            Utils.print_exception('SEARCHING_DIALOG closeEvent', e)
