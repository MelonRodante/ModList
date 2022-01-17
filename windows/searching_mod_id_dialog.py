import json

import requests
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox

from pyqt_windows.searching_mod_id_dialog import Ui_SearchModIdDialog
from utils.curseapilinks import CurseAPI
from utils.database import Database
from utils.modindex import ModIndex
from utils.utils import Utils


class SearchingModIdDialog(QtWidgets.QDialog):

    def __init__(self):
        super(SearchingModIdDialog, self).__init__()
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
        self.ui = Ui_SearchModIdDialog()
        self.ui.setupUi(self)

        self.exit_code = 0

        self.setupEvents()

        self.show()

    def setupEvents(self):
        try:
            self.ui.btnSearch.clicked.connect(self.btn_search_mod)

        except Exception as e:
            Utils.print_exception('SEARCHING_MOD_ID_DIALOG setupEvents', e)

    def btn_search_mod(self):
        try:
            try:
                # mod = requests.get(CurseAPI.minecraft_modid + str(self.ui.spinModid.value()), headers=CurseAPI.header).json()
                mod = requests.get(CurseAPI.minecraft_modid + str(self.ui.spinModid.value()), headers=CurseAPI.header).json().get('data')

                # if mod.get('categorySection').get('gameId') == CurseAPI.gameId and mod.get('categorySection').get('gameCategoryId') == CurseAPI.classId:
                print(str(mod.get('gameId')), str(mod.get('categories')[0].get('classID')))
                if str(mod.get('gameId')) == CurseAPI.gameId and str(mod.get('categories')[0].get('classId')) == CurseAPI.classId:
                    mod = ModIndex(mod)
                    mod.check_mod(Database.db, [''])
                    mod.process_mod(Database.db)
                    self.done(1)
                else:
                    QMessageBox.warning(None, 'MOD NO ENCONTRADO:', 'MOD NO ENCONTRADO:\n\nEl ID de proyecto no es un mod de minecraft.', QtWidgets.QMessageBox.Close)
                    self.done(0)
            except json.decoder.JSONDecodeError:
                QMessageBox.critical(None, 'API ERROR:', 'API ERROR:\n\nLa consulta a la API no ha regresado ningun valor.', QtWidgets.QMessageBox.Close)
                self.done(0)

        except Exception as e:
            Utils.print_exception('SEARCHING_MOD_ID_DIALOG btn_search_mod', e)

'''318416'''