from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QPixmap, QPainter, QIcon


class IconUtils:
    categories_icons = {}

    @staticmethod
    def getNormalIcon(image):
        pm = QPixmap(image)
        return IconUtils.__getIconWithoutTint(pm)

    @staticmethod
    def getLargeIcon(categories, center=False):
        pm = IconUtils.__getLargePixmap(categories, center=center)
        return IconUtils.__getIconWithoutTint(pm)

    @staticmethod
    def __getIconWithoutTint(pixmap):
        icon = QIcon(pixmap)
        icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
        icon.addPixmap(pixmap, QIcon.Normal, QIcon.On)
        icon.addPixmap(pixmap, QIcon.Active, QIcon.Off)
        icon.addPixmap(pixmap, QIcon.Active, QIcon.On)
        icon.addPixmap(pixmap, QIcon.Disabled, QIcon.Off)
        icon.addPixmap(pixmap, QIcon.Disabled, QIcon.On)
        icon.addPixmap(pixmap, QIcon.Selected, QIcon.Off)
        icon.addPixmap(pixmap, QIcon.Selected, QIcon.On)
        return icon

    @staticmethod
    def __getLargePixmap(categories, center=False):
        if center:
            icon = IconUtils.categories_icons.get('|center|' + categories)
        else:
            icon = IconUtils.categories_icons.get(categories)

        if not isinstance(icon, QPixmap):
            pm = QPixmap(':/categories/categories/empty.png')
            painter = QPainter(pm)
            if categories != 'without-category':
                cat = categories.split(',')
                start = 0
                if center:
                    start = ((5 - len(cat)) * 29) / 2

                for i, c in enumerate(cat):
                    px = QPixmap(':/categories/categories/' + c + '.png')
                    painter.drawPixmap(
                        QRectF(start + (i * (px.rect().width() + 5)), 0, 24, 24),
                        px,
                        QRectF(px.rect()))
            else:
                px = QPixmap(':/categories/categories/' + categories + '.png')
                painter.drawPixmap(QRectF(pm.width() / 2 - px.width() / 2, 0, 24, 24), px, QRectF(px.rect()))

            if center:
                IconUtils.categories_icons['|center|' + categories] = pm
            else:
                IconUtils.categories_icons[categories] = pm
            return pm
        else:
            return icon
