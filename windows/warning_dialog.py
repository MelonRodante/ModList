from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from pyqt_windows.warning_dialog import Ui_WarningDialog


class WarningDialog(QtWidgets.QDialog):

    def __init__(self, msg, confirmation_dialog=True):
        super(WarningDialog, self).__init__()
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
        self.ui = Ui_WarningDialog()
        self.ui.setupUi(self)

        self.ui.lblAviso.setText(msg)

        if confirmation_dialog:
            self.ui.botones.setStandardButtons(QtWidgets.QDialogButtonBox.Yes | QtWidgets.QDialogButtonBox.No)
        else:
            self.ui.botones.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)

        self.show()
        self.setFixedSize(self.size())


