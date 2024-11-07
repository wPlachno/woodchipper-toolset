import datetime

from wctk_record import WCRecord
from wctk_tracker import WCTracker
import constants as C
from wcutil import WoodChipperFile, WoodchipperDictionaryFile


class WoodchipperToolkitClone(WCTracker):

    def __init__(self):
        WCTracker.__init__(self, delimiter=C.DELIMITER.CLONE)
        self.state = C.STATE.UNKNOWN

    def compare(self, core_record):
        WCTracker.update(self)
        new_state = C.STATE.UNKNOWN
        if self.current:
            new_state = C.STATE.BEHIND_CORE
            if self.current.is_higher_version_than(core_record):
                new_state = C.STATE.AFTER_CORE
            elif self.current.has_same_version_as(core_record):
                new_state = C.STATE.UP_TO_DATE
            elif self.has_local_changes():
                new_state = C.STATE.HAS_LOCAL_CHANGES
        self.state = new_state