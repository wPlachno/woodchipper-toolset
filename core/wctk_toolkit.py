from core.wctk_tracker import WCTracker
from core.wctk_clone import WoodchipperToolkitClone as WCClone
from interface import constants as C


class WoodchipperToolkit(WCTracker):

    def __init__(self):
        WCTracker.__init__(self, delimiter=C.DELIMITER.TOOLKIT)
        self.state = C.STATE.UNKNOWN
        self.clones = []

    def __contains__(self, item):
        target = item
        if item is WCTracker:
            target = item.name
        for cl in self.clones:
            if cl.name == target:
                return True
        return False

    def __getitem__(self, item):
        item_text = str(item)
        for clone in self.clones:
            if clone.name == item_text:
                return clone
        return None

    def update(self):
        WCTracker.update(self)
        self.state = C.STATE.UP_TO_DATE
        if self.current and self.archive:
            if self.current.is_higher_version_than(self.archive):
                self.archive = self.current
            elif self.has_local_changes():
                self.state = C.STATE.HAS_LOCAL_CHANGES
        for clone in self.clones:
            clone.update()
            clone.compare(self.archive)

    def parse_archive(self, text):
        self.clones.clear()
        clone_data = WCTracker.parse_archive(self, text)
        for clone_text in clone_data:
            current_clone = WCClone()
            current_clone.parse_archive(clone_text)
            self.clones.append(current_clone)

    def write_archive(self):
        out_string = WCTracker.write_archive(self)
        for clone in self.clones:
            out_string += self.delimiter + clone.write_archive()
        return out_string

    def add_clone(self, name, path):
        new_cl = WCClone()
        new_cl.name = name
        new_cl.path = path
        new_cl.update()
        new_cl.compare(self.archive)
        self.clones.append(new_cl)

