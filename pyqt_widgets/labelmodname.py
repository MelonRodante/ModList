import PyQt5
from PyQt5.QtWidgets import QLabel

from pyqt_style import colors


class LabelModName(QLabel):
    def __init__(self, mod):
        try:
            QLabel.__init__(self)
            text = ' <b style="' \
                   'text-align: center; ' \
                   'font-family: MS Shell Dlg 2; ' \
                   'color: ' + colors.TextColor + '; ' \
                   'font-size:15px;"> ' \
                   + mod.name + \
                   '</b> '

            if mod.installed and mod.favorite:
                icon = ' <img src=:/states/states/installed_favorite.png>'
            elif mod.installed and not mod.favorite:
                icon = ' <img src=:/states/states/installed.png>'
            elif mod.ignored and mod.favorite:
                icon = ' <img src=:/states/states/ignored_favorite.png>'
            elif mod.ignored and not mod.favorite:
                icon = ' <img src=:/states/states/ignored.png>'
            elif mod.favorite:
                icon = ' <img src=:/states/states/favorite.png title="this will be displayed as a tooltip">'
            elif mod.blocked:
                icon = ' <img src=:/states/states/blocked.png>'
            else:
                icon = ''

            if mod.updated:
                icon = '<img src=:/states/states/updated.png>' + icon

            self.setText('<table width=\"100%\"><td width=\"50%\" align=\"left\">' + text + '</td> <td width=\"50%\" align=\"right\">' + icon + '</td></table>')
            self.setStyleSheet('background-color: #00000000')
            self.setAttribute(PyQt5.QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)

        except Exception as e:
            print('LabelModName: ', str(e))
