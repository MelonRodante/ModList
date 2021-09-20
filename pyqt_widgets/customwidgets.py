from PyQt5.QtWidgets import QPushButton


class Mod:
    def __init__(self, q):
        self.name =        q.value(1)
        self.category =    q.value(2)
        self.loader =      q.value(3)
        self.update_date = q.value(4)
        self.path =        q.value(5)
        self.installed =   q.value(6)
        self.ignored =     q.value(7)
        self.updated =     q.value(8)
        self.favorite =    q.value(9)
        self.blocked =     q.value(10)


class CustomButton(QPushButton):
    def __init__(self, mod):
        QPushButton.__init__(self)
        self.mod = mod


