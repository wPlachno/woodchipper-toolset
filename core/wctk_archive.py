import pathlib

from core.wctk_tracker import WCTracker
from core.wctk_toolkit import WoodchipperToolkit as WCToolkit
from utilities.wcutil import WoodChipperFile as WCFile
from interface import constants as C


class WoodchipperArchive:
    def __init__(self, archive_file_name=C.FILE_NAME.ARCHIVE):
        self.file = WCFile(pathlib.Path.home() / archive_file_name)
        self.toolkits = []

    def __contains__(self, item):
        target = item
        if item is WCTracker:
            target = item.name
        for tk in self.toolkits:
            if tk.name == target:
                return True
        return False

    def __getitem__(self, item):
        item_str = str(item)
        for tk in self.toolkits:
            if tk.name == item_str:
                return tk
        return None

    def load(self):
        self.file.read()
        for line in self.file.text:
            current_toolkit = WCToolkit()
            current_toolkit.parse_archive(line)
            self.toolkits.append(current_toolkit)
        for tk in self.toolkits:
            tk.update()

    def save(self):
        if self._requires_save():
            self.file.clear()
            for current_toolkit in self.toolkits:
                self.file.append_line(current_toolkit.write_archive())
            self.file.write()

    def add_toolkit(self, name, path):
        new_tk = WCToolkit()
        new_tk.name = name
        new_tk.path = path
        new_tk.update()
        self.toolkits.append(new_tk)

    def _requires_save(self):
        requires_save = False
        for toolkit in self.toolkits:
            requires_save = requires_save or toolkit.requires_save()
        return requires_save

