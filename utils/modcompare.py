from utils.mod import Mod
from utils.utils import Utils


class ModCompare:

    def __init__(self, mods: list[Mod], islist: bool):
        try:
            self.multiple_mods = len(mods) > 1

            self.loader = mods[0].loader
            self.categories = mods[0].categories
            self.update_date = mods[0].update_date

            self.installed = mods[0].installed if islist else mods[0].autoinstall
            self.ignored = mods[0].ignored if islist else mods[0].autoignore
            self.updated = mods[0].updated

            self.favorite = mods[0].favorite
            self.blocked = mods[0].blocked

            if self.multiple_mods:
                self.name = ' - VARIOS (%d) - ' % len(mods)
                self.compare_states(mods, islist)
            else:
                self.name = mods[0].name

        except Exception as e:
            Utils.print_exception('MODCOMPARE init', e)

    def compare_states(self, mods: list[Mod], islist: bool):
        try:
            for mod in mods[1:]:
                if self.loader != mod.loader:
                    self.loader = None

                if self.categories != mod.categories:
                    self.categories = None

                if self.update_date != mod.update_date:
                    self.update_date = None

                if self.installed != (mod.installed if islist else mod.autoinstall):
                    self.installed = None

                if self.ignored != (mod.ignored if islist else mod.autoignore):
                    self.ignored = None

                if self.updated != mod.updated:
                    self.updated = None

                if self.favorite != mod.favorite:
                    self.favorite = None

                if self.blocked != mod.blocked:
                    self.blocked = None

        except Exception as e:
            Utils.print_exception('MODCOMPARE compare_states', e)
