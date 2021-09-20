import threading
from time import sleep

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QSize, Qt, QObject, pyqtSignal, QThread
from qtpy import QtSql

from pyqt_windows.searching_dialog import Ui_SearchingDialog


class Worker(QObject):
    sig_max_pages = pyqtSignal(int)
    sig_page_finish = pyqtSignal(int)
    sig_finished = pyqtSignal()

    def __init__(self, max_pages):
        super(Worker, self).__init__()
        self.max_pages = 10
        self.canclose = 0

    def run(self):
        try:
            self.sig_max_pages.emit(self.max_pages)

            for i in range(1, self.max_pages + 1):
                if self.canclose:
                    break
                self.task()
                self.sig_page_finish.emit(i)
            self.sig_finished.emit()
        except Exception as e:
            print('SEARCHING_DIALOG run:', e)

    def task(self):
        sleep(0.3)

class SearchingDialog(QtWidgets.QDialog):

    def __init__(self):
        super(SearchingDialog, self).__init__()
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
        self.ui = Ui_SearchingDialog()
        self.ui.setupUi(self)

        self.thread = None
        self.worker = None

        self.setupWidgets()
        self.setupEvents()
        self.show()

    def setupWidgets(self):
        try:
            self.modify_css()
            self.create_cmb_values_lists()
        except Exception as e:
            print('SEARCHING_DIALOG modify_css:', e)

    def modify_css(self):
        try:
            self.ui.btnSearchNewMods.setStyleSheet(
                'QPushButton {border: 1px solid #F0651F; background-color: #0F1A25;} '
                'QPushButton:hover {background-color: #19232D;}'
                'QPushButton:pressed {background-color: #54687A;}'
                'QPushButton:disabled {border: 1px solid #000000;}')
        except Exception as e:
            print('SEARCHING_DIALOG modify_css:', e)

    def create_cmb_values_lists(self):
        try:
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
        except Exception as e:
            print('SEARCHING_DIALOG create_cmb_values_lists:', e)

    def setupEvents(self):
        try:
            self.ui.cmbModList.currentIndexChanged.connect(self.change_cmb_modlist)
            self.ui.btnSearchNewMods.clicked.connect(self.search_mods)
        except Exception as e:
            print('SEARCHING_DIALOG setupEvents:', e)

    def change_cmb_modlist(self):
        try:
            self.ui.btnSearchNewMods.setEnabled(self.ui.cmbModList.currentIndex() > 1)
        except Exception as e:
            print('SEARCHING_DIALOG change_cmb_modlist:', e)

    def search_mods(self):
        try:
            self.ui.cmbModList.setEnabled(False)
            self.ui.spinPages.setEnabled(False)
            self.ui.btnSearchNewMods.setEnabled(False)

            self.thread = QThread()
            self.worker = Worker(self.ui.spinPages.value())
            self.worker.moveToThread(self.thread)

            self.thread.started.connect(self.worker.run)
            self.thread.finished.connect(self.thread.deleteLater)
            self.worker.sig_finished.connect(self.worker.deleteLater)
            self.worker.sig_finished.connect(self.thread.quit)

            self.worker.sig_max_pages.connect(self.set_max_pages)
            self.worker.sig_page_finish.connect(self.set_page_finish)
            self.thread.finished.connect(self.set_finish_search)

            self.thread.start()
        except Exception as e:
            print('SEARCHING_DIALOG search_mods:', e)

    def set_max_pages(self, max_pages):
        try:
            self.ui.progressBar.setMaximum(max_pages)
        except Exception as e:
            print('SEARCHING_DIALOG set_max_pages:', e)

    def set_page_finish(self, page_finish):
        try:
            self.ui.progressBar.setValue(page_finish)
        except Exception as e:
            print('SEARCHING_DIALOG set_page_finish:', e)

    def set_finish_search(self):
        try:
            if not self.worker.canclose:
                self.ui.progressBar.setValue(self.ui.progressBar.maximum())
                sleep(1)

            self.done(self.worker.canclose)
        except Exception as e:
            print('SEARCHING_DIALOG set_finish_search:', e)

    def closeEvent(self, event):
        try:
            if self.worker is not None:
                self.worker.canclose = 1
                self.ui.progressBar.setFormat('Cancelando...')
                event.ignore()
        except Exception as e:
            print('SEARCHING_DIALOG closeEvent:', e)
