import PyQt5
from PyQt5.QtWidgets import QLabel

from pyqt_style import colors
from pyqt_widgets.labelmodname import LabelModName

categories_dict = {
        'world-gen':
            ('World Gen', '<img src=:/categories/categories/world-gen.png>'),
        'world-biomes':
            ('Biomes', '<img src=:/categories/categories/world-biomes.png>'),
        'world-ores-resources':
            ('Ores / Resources', '<img src=:/categories/categories/world-ores-resources.png>'),
        'world-structures':
            ('Structures', '<img src=:/categories/categories/world-structures.png>'),
        'world-dimensions':
            ('Dimensions', '<img src=:/categories/categories/world-dimensions.png>'),
        'world-mobs':
            ('Mobs', '<img src=:/categories/categories/world-mobs.png>'),
        'technology':
            ('Technology', '<img src=:/categories/categories/technology.png>'),
        'technology-processing':
            ('Processing', '<img src=:/categories/categories/technology-processing.png>'),
        'technology-player-transport':
            ('Player Transport', '<img src=:/categories/categories/technology-player-transport.png>'),
        'technology-item-fluid-energy-transport':
            ('I / F / E Transport', '<img src=:/categories/categories/technology-item-fluid-energy-transport.png>'),
        'technology-farming':
            ('Farming', '<img src=:/categories/categories/technology-farming.png>'),
        'technology-energy':
            ('Energy', '<img src=:/categories/categories/technology-energy.png>'),
        'technology-genetics':
            ('Genetics', '<img src=:/categories/categories/technology-genetics.png>'),
        'technology-automation':
            ('Automation', '<img src=:/categories/categories/technology-automation.png>'),
        'magic':
            ('Magic', '<img src=:/categories/categories/magic.png>'),
        'storage':
            ('Storage', '<img src=:/categories/categories/storage.png>'),
        'library-api':
            ('API / Library', '<img src=:/categories/categories/library-api.png>'),
        'adventure-rpg':
            ('Adventure and RPG', '<img src=:/categories/categories/adventure-rpg.png>'),
        'map-information':
            ('Map / Information', '<img src=:/categories/categories/map-information.png>'),
        'cosmetic':
            ('Cosmetic', '<img src=:/categories/categories/cosmetic.png>'),
        'mc-miscellaneous':
            ('Miscellaneous', '<img src=:/categories/categories/mc-miscellaneous.png>'),
        'mc-addons':
            ('Addons', '<img src=:/categories/categories/mc-addons.png>'),
        'armor-weapons-tools':
            ('Armor / Weapons / Tools', '<img src=:/categories/categories/armor-weapons-tools.png>'),
        'server-utility':
            ('Server Utility', '<img src=:/categories/categories/server-utility.png>'),
        'mc-food':
            ('Food', '<img src=:/categories/categories/mc-food.png>'),
        'redstone':
            ('Redstone', '<img src=:/categories/categories/redstone.png>'),
        'twitch-integration':
            ('Twitch Integration', '<img src=:/categories/categories/twitch-integration.png>')
    }


class LabelModCategories(QLabel):

    def __init__(self, mod_categories):
        try:
            QLabel.__init__(self)
            categories = ''

            for i, cat in enumerate(mod_categories.split(',')):
                if i > 0:
                    categories += ' '
                if cat in categories_dict:
                    categories += categories_dict[cat][1]
                elif cat != 'mc-creator':
                    categories += '<div style="text-align: center; font-family: MS Shell Dlg 2; color: ' + colors.TextColor + '; font-size:12px;">Sin categoria</div>'

            self.setText(categories)
            self.setStyleSheet('background-color: #00000000')
            self.setAttribute(PyQt5.QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)

        except Exception as e:
            print('LabelModCategories: ', str(e))
