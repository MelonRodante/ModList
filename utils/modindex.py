from datetime import datetime

import requests
from PyQt5.QtCore import QByteArray


class ModIndex:
    cat_id = {
        406:  "world-gen",
        407:  "world-biomes",
        408:  "world-ores-resources",
        409:  "world-structures",
        410:  "world-dimensions",
        411:  "world-mobs",

        412:  "technology",
        413:  "technology-processing",
        414:  "technology-player-transport",
        415:  "technology-item-fluid-energy-transport",
        416:  "technology-farming",
        417:  "technology-energy",
        418:  "technology-genetics",
        4843: "technology-automation",

        419:  "magic",
        420:  "storage",
        421:  "library-api",
        422:  "adventure-rpg",
        423:  "map-information",
        424:  "cosmetic",
        425:  "mc-miscellaneous",

        426:  "mc-addons",
        427:  "mc-addons",  # "addons-thermalexpansion",
        428:  "mc-addons",  # "addons-tinkers-construct",
        429:  "mc-addons",  # "addons-industrialcraft",
        430:  "mc-addons",  # "addons-thaumcraft",
        432:  "mc-addons",  # "addons-buildcraft",
        433:  "mc-addons",  # "addons-forestry",
        4485: "mc-addons",  # "blood-magic",
        4486: "mc-addons",  # "[4486]lucky-blocks",
        4545: "mc-addons",  # "applied-energistics-2",
        4773: "mc-addons",  # "crafttweaker",

        434:  "armor-weapons-tools",
        435:  "server-utility",
        436:  "mc-food",
        4558: "redstone",
        4671: "twitch-integration",
        4906: None,  # "mc-creator",
        4780: None,  # "[4780]fabric",
    }

    ignore_cat = ('mc-addons',
                  'addons-thermalexpansion',
                  'addons-tinkers-construct',
                  'addons-industrialcraft',
                  'addons-thaumcraft',
                  'addons-buildcraft',
                  'addons-forestry',
                  'blood-magic',
                  'lucky-blocks',
                  'applied-energistics-2',
                  'crafttweaker')

    def __init__(self, mod: dict):
        try:
            self.projectid = mod.get('id')
            self.path = mod.get('websiteUrl')
            self.name = mod.get('name')
            self.loader = ModIndex.getLoader(mod)
            self.categories = mod.get('categories')
            self.update_date = mod.get('dateModified')
            self.icon = mod.get('attachments')
            self.dependencies = mod.get('latestFiles')

            self.error = 0
            self.newmod = 0
            self.update = 0
            self.addlist = 0
            self.preinstall = 0
            self.preignore = 0

        except Exception as e:
            print('ModIndex __init__:', e)

    def setCategories(self):
        try:
            categories = set()
            if isinstance(self.categories, list):
                for cat in self.categories:
                    cat = ModIndex.cat_id.get(cat.get('categoryId'))
                    if cat is not None:
                        categories.add(cat)
            categories = list(categories)
            categories.sort()

            if len(categories) > 0:
                self.categories = ','.join(categories)
            else:
                self.categories = 'without-category'
        except:
            self.categories = 'error'

    def setDate(self):
        try:
            if isinstance(self.update_date, str):
                if self.update_date.__contains__('.'):
                    self.update_date = int(datetime.strptime(self.update_date, '%Y-%m-%dT%H:%M:%S.%f%z').replace(microsecond=0).timestamp())
                else:
                    self.update_date = int(datetime.strptime(self.update_date, '%Y-%m-%dT%H:%M:%S%z').replace(microsecond=0).timestamp())
            elif not isinstance(self.update_date, int):
                self.update_date = 0
        except:
            self.update_date = -1

    def setIcon(self):
        try:
            if isinstance(self.icon, list):
                for attach in self.icon:
                    if attach.get('isDefault') is True:
                        self.icon = QByteArray(requests.get(attach.get('thumbnailUrl')).content)
            else:
                self.update_date = QByteArray()
        except:
            self.update_date = QByteArray()

    def setDependencies(self):
        try:
            dependencies = set()
            if self.dependencies is not None:
                for file in self.dependencies:
                    if file.get('dependencies') is not None:
                        for dep in file.get('dependencies'):
                            if dep.get('addonId') is not None:
                                dependencies.add(dep.get('addonId'))
            self.dependencies = list(dependencies)
        except Exception as e:
            print('ModIndex setDependencies:', e)
            self.dependencies = []

    @staticmethod
    def getLoader(mod):
        try:
            forge = False
            fabric = False


            if mod.get('modLoaders') is not None:
                for loader in mod.get('modLoaders'):
                    if loader == 'Forge':
                        forge = True
                    elif loader == 'Fabric':
                        fabric = True

            elif mod.get('gameVersionLatestFiles') is not None:
                for file in mod.get('gameVersionLatestFiles'):
                    if file.get('modLoader') == 1:
                        forge = True
                    elif file.get('modLoader') == 4:
                        fabric = True


            if forge and fabric:
                return 'Forge / Fabric'
            elif forge:
                return 'Forge'
            elif fabric:
                return 'Fabric'
            else:
                return 'Sin Loader'
        except Exception as e:
            print('ModIndex getLoader:', e)
            return 'error'
