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
            version_compare = self.current.compare_versions_with(core_record)
            if version_compare == C.COMPARE.GREATER_THAN:
                new_state = C.STATE.AFTER_CORE
            elif version_compare == C.COMPARE.EQUAL_TO:
                new_state = C.STATE.UP_TO_DATE
            if self.has_local_changes():
                new_state = C.STATE.HAS_LOCAL_CHANGES
        self.state = new_state