from PyQt5.QtWidgets import QMenu


class CustomQMenu(QMenu):
    def __init__(self, index):
        QMenu.__init__(self)
        self.index = index
