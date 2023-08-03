import traceback

import PyQt5
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QPixmap, QPainter, QIcon

from utils.utils import Utils


class IconUtils:
    other_cat_icons = {}
    multi_categories_icons = {}

    @staticmethod
    def getIconWithoutTint(pixmap):
        try:
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

        except Exception as e:
            Utils.print_exception('ICON_UTILS getIconWithoutTint', e)


    @staticmethod
    def get_cat_icon_str(cat):
        return ':/categories/categories/' + cat + '.png'

    @staticmethod
    def pixmap_to_qbytearray(image):
        try:
            if isinstance(image, str):
                px = QPixmap(IconUtils.get_cat_icon_str(image))
            elif isinstance(image, QPixmap):
                px = image
            else:
                return QtCore.QByteArray()

            byte_array = QtCore.QByteArray()
            buff = QtCore.QBuffer(byte_array)
            buff.open(QtCore.QIODevice.WriteOnly)
            ok = px.save(buff, "PNG")
            if ok:
                return byte_array
            else:
                return QtCore.QByteArray()

        except Exception as e:
            Utils.print_exception('ICON_UTILS pixmap_to_qbytearray', e)

    @staticmethod
    def qbytearray_to_pixmap(array, size=48):
        try:
            if isinstance(array, PyQt5.QtCore.QByteArray):
                pixmap = QtGui.QPixmap()
                pixmap.loadFromData(array)
            else:
                pixmap = QtGui.QPixmap(':/widgets/widgets/noicon.png')

            return pixmap.scaled(size, size, Qt.KeepAspectRatio)

        except Exception as e:
            Utils.print_exception('ICON_UTILS qbytearray_to_pixmap', e)

    @staticmethod
    def getCatNormalPixMap(image):
        try:
            if image.startswith('-mlc-'):
                return IconUtils.other_cat_icons[image]
            else:
                return QPixmap(IconUtils.get_cat_icon_str(image))

        except Exception as e:
            Utils.print_exception('ICON_UTILS getCatNormalPixMap', e)

    @staticmethod
    def getCatNormalIcon(image):
        try:
            if image.startswith('-mlc-'):
                return IconUtils.getIconWithoutTint(IconUtils.other_cat_icons[image])
            else:
                return IconUtils.getIconWithoutTint(QPixmap(IconUtils.get_cat_icon_str(image)))

        except Exception as e:
            Utils.print_exception('ICON_UTILS getCatNormalIcon', e)

    @staticmethod
    def getNormalIcon(image):
        try:
            return IconUtils.getIconWithoutTint(QPixmap(image))

        except Exception as e:
            Utils.print_exception('ICON_UTILS getNormalIcon', e)

    @staticmethod
    def getLargeIcon(categories, center=False):
        try:
            pm = IconUtils.__getLargePixmap(categories, center=center)
            return IconUtils.getIconWithoutTint(pm)

        except Exception as e:
            Utils.print_exception('ICON_UTILS getLargeIcon', e)

    @staticmethod
    def __getLargePixmap(categories, center=False):
        try:
            if center:
                icon = IconUtils.multi_categories_icons.get('|center|' + categories)
            else:
                icon = IconUtils.multi_categories_icons.get(categories)

            if not isinstance(icon, QPixmap):
                pm = QPixmap(IconUtils.get_cat_icon_str('empty'))
                painter = QPainter(pm)
                if categories != 'without-category':
                    cat = categories.split(',')
                    start = 0
                    if center:
                        start = ((5 - len(cat)) * 58) / 2

                    for i, c in enumerate(cat):
                        px = IconUtils.getCatNormalPixMap(c)
                        painter.drawPixmap(
                            QRectF(start + (i * (px.rect().width() + 10)), 0, 48, 48),
                            px,
                            QRectF(px.rect()))
                else:
                    px = QPixmap(IconUtils.get_cat_icon_str(categories))
                    painter.drawPixmap(QRectF(pm.width() / 2 - px.width() / 2, 0, 48, 48), px, QRectF(px.rect()))

                if center:
                    IconUtils.multi_categories_icons['|center|' + categories] = pm
                else:
                    IconUtils.multi_categories_icons[categories] = pm

                return pm
            else:
                return icon

        except Exception as e:
            Utils.print_exception('ICON_UTILS __getLargePixmap', e)

