# wcn_handler.py
# Created: 01/04/2025
# Version: 0.0.1.002
# Last Changed: 01/08/2025

from pathlib import Path
from os import getcwd

from utilities.wcmodehandler import WoodchipperCoreModeHandler as WCHandler
from constants import RESPONSE as OUT, LIB
from core.wcn_library import WoodchipperNoteLibrary


class WoodchipperNoteHandler(WCHandler):
    def __init__(self, request, response):
        WCHandler.__init__(self, request, response)
        self.library = self._initialize_library()
        self.lib = self.request.lib
        self.targets = self.request.target
        self.log_kvp(OUT.CORE_PATH, self.library.core.path)
        self.log_kvp(OUT.LOCAL_PATH, self.library.local.path)
        self.log_kvp(OUT.LIB, self.lib)

    def _initialize_library(self):
        lib = WoodchipperNoteLibrary()
        lib.set_paths(Path.home(), Path(getcwd()), self.debug)
        return lib

    def save(self, lib=LIB.ALL):
        self.library.save(lib)

    def compile_success(self, notes=None, lib=LIB.ALL, success=True):
        self.save(lib)
        self.log_kvp(OUT.NOTES, notes)
        if success:
            self.log_success()

    def validate_targets(self, validator=None):
        if validator:
            if not validator(len(self.targets)):
                self.log_error(f"Incorrect arguments for mode={self.request.mode}.")
                return False
        return True

    @staticmethod
    def validate_at_least_1(arg_num):
        return arg_num>0
    @staticmethod
    def validate_only_1_pair(arg_num):
        return arg_num==2
    @staticmethod
    def validate_exactly_1(arg_num):
        return arg_num==1

class WoodchipperNoteHandlerShow(WoodchipperNoteHandler):
    def handle(self):
        lib_description = self.library.describe_library(self.lib)
        self.compile_success(notes=lib_description)

class WoodchipperNoteHandlerAdd(WoodchipperNoteHandler):
    def handle(self):
        if self.validate_targets(self.validate_at_least_1):
            added = []
            for target in self.targets:
                added.append(self.library.append_text(target, self.lib))
            self.compile_success(notes=added)

class WoodchipperNoteHandlerRemove(WoodchipperNoteHandler):
    def handle(self):
        if self.validate_targets(self.validate_at_least_1):
            deleted_notes = []
            target_notes = list(map(lambda x: int(x), self.targets))
            target_notes.sort(reverse=True)
            for target in target_notes:
                deleted = self.library.delete_by_nid(int(target))
                deleted_notes.append(deleted)
            if len(deleted_notes) > 1:
                deleted_notes.sort(key=lambda x: x.index)
            self.compile_success(notes=deleted_notes)

class WoodchipperNoteHandlerMove(WoodchipperNoteHandler):
    def handle(self):
        if self.validate_targets(self.validate_only_1_pair):
            target_nid = int(self.targets[0])
            destination_nid = int(self.targets[1])
            movement = self.library.move_by_nid(target_nid, destination_nid)
            self.compile_success(notes=movement)
        elif self.validate_targets(self.validate_exactly_1):
            target_nid = int(self.targets[0])
            movement = self.library.relocate_by_nid(target_nid)
            self.compile_success(notes=movement)

class WoodchipperNoteHandlerUpdate(WoodchipperNoteHandler):
    def handle(self):
        if self.validate_targets(self.validate_only_1_pair):
            target_nid = int(self.targets[0])
            new_text = self.targets[1]
            update = self.library.update_by_nid(target_nid, new_text)
            self.compile_success(notes=update)

class WoodchipperNoteHandlerReplace(WoodchipperNoteHandler):
    def handle(self):
        if self.validate_targets(self.validate_only_1_pair):
            target_nid = int(self.targets[0])
            new_text = self.targets[1]
            replace = self.library.replace_by_nid(target_nid, new_text)
            self.compile_success(notes=replace)

class WoodchipperNoteHandlerClear(WoodchipperNoteHandler):
    def handle(self):
        lost_notes = self.library.clear_library(self.lib)
        self.compile_success(notes=lost_notes)