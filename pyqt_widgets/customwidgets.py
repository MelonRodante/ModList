from PyQt5.QtWidgets import QPushButton


class Mod:
    def __init__(self, path, installed, ignored, updated, favorite, blocked):
        self.path = path
        self.installed = installed
        self.ignored = ignored
        self.updated = updated
        self.favorite = favorite
        self.blocked = blocked

    def print(self):
        print('installed:', self.installed, 'ignored:', self.ignored, 'updated:', self.updated, 'favorite:', self.favorite, 'blocked:', self.blocked)

class CustomButton(QPushButton):
    def __init__(self, mod):
        QPushButton.__init__(self)
        self.mod = mod


