# wcn_library.py
# Created: Will Plachno on 8/22/24
# Version: 0.0.2.002
# Last Changed: 01/11/2025

from utilities import wcutil
from core.wcn_archive import WoodchipperNoteArchive as WCArchive
from core.wcn_note import WoodchipperNote
from constants import LIB, FILE_NAME, RESPONSE
from pathlib import Path
from utilities.wcutil import WoodchipperNamespace

# A note on terminology:
# "index" is the zero-based-index location of the note within the individual files.
# "nid" is the one-based-index location of the note across both files.
# "Archive" refers to a single file's collection of notes, while
# "Library" refers to a group of Archives, the core archive and a local archive.

class WoodchipperNoteLibrary:

    class NotePointer:

        class SAFETY:
            EXCEPTION="e"
            BOUNDED="b"
            NONE="n"

        def __init__(self, lib=LIB.CORE, index=-1, archive=None, safe=SAFETY.EXCEPTION):
            self._lib = lib
            self._index = index
            self._archive = archive
            self.set(safe=safe)

        def set(self, lib=None, index: int =None, archive=None, safe=SAFETY.EXCEPTION):
            if lib: self._lib = lib
            if index: self._index = index
            if archive: self._archive = archive
            if self._lib == LIB.ALL:
                # If lib is ALL, we have a NID that should be converted to an actual pointer
                zero_based_nid: int = self._index-1
                cutoff: int = len(self._archive.core.notes)
                if zero_based_nid < cutoff:
                    self._lib = LIB.CORE
                    self._index = zero_based_nid
                else:
                    self._lib = LIB.LOCAL
                    self._index = zero_based_nid - cutoff
            if self._index >= len(self.library().notes):
                if safe == self.SAFETY.EXCEPTION:
                    raise Exception("Given index cannot be resolved.")
                elif safe == self.SAFETY.BOUNDED:
                    # Check if the index would be valid as an nid
                    if self._lib == LIB.CORE:
                        self.set(LIB.ALL)
                    else:
                        self._index = len(self._archive.local.notes)-1

        def step(self, step: int=1):
            self.set(index=self._index+step, safe=WoodchipperNoteLibrary.NotePointer.SAFETY.BOUNDED)

        def exists(self) -> bool:
            if self._archive and -1 < self._index < len(self.library().notes):
                return True
            return False

        def library(self, opposite: bool=False) -> WCArchive:
            if self._lib == LIB.CORE:
                return self._archive.core if not opposite else self._archive.local
            return self._archive.local if not opposite else self._archive.core

        def note(self) -> WoodchipperNote:
            if self.exists:
                return self.library().notes[self._index]
            raise Exception("Cannot retrieve imaginary Note.")

        def nid(self) -> int:
            nid = self._index + 1
            if self._lib == LIB.LOCAL:
                nid += len(self._archive.core.notes)
            return nid

        def same_library_as(self, other):
            if type(other) == str:
                return self._lib == other
            elif type(other) == type(self):
                return self._lib == other.get_lib()
            else:
                raise Exception(f"A {type(other)} cannot be compared to a NotePointer using same_library_as()")

        def remove(self, pointers=None) -> WoodchipperNote:
            note: WoodchipperNote = self.library().remove(self._index)
            if pointers:
                for pointer in pointers:
                    if pointer.get_lib() == self._lib:
                        pointer.step(-1)
            return note

        def insert_note(self, note:WoodchipperNote) -> WoodchipperNote:
            pointer = self.library().insert(self._index, note)
            return self.note()

        def update_text(self, updated_text: str) -> WoodchipperNote:
            old_note: WoodchipperNote = self.note()
            self.library().edit(self._index, updated_text)
            return old_note

        def replace_note(self, new_text: str) -> WoodchipperNote:
            old_note: WoodchipperNote = self.note()
            self.library().reset(self._index, new_text)
            return old_note

        def relocate_to_end_of_other_library(self) -> WoodchipperNote:
            old_note: WoodchipperNote = self.note()
            self.remove()
            self._lib = LIB.LOCAL if self._lib == LIB.CORE else LIB.CORE
            self._index = self.library().append_note(old_note)
            return old_note


        def get_index(self) -> int:
            return self._index
        def get_lib(self) -> str:
            return self._lib
        def get_archive(self):
            return self._archive


    # CORE METHODS

    def __init__(self):
        self.core: WCArchive = WCArchive()
        self.local: WCArchive = WCArchive()
        self.cutoff: int = 0

    def __len__(self) -> int:
        return len(self.core.notes) + len(self.local.notes)

    def set_paths(self, home_path: Path, work_path: Path, debug: bool =False):
        core_file_name = FILE_NAME.DEBUG if debug else FILE_NAME.CORE
        local_file_name = FILE_NAME.DEBUG if debug else FILE_NAME.LOCAL
        self.core.load(home_path / core_file_name)
        self.local.load(work_path / local_file_name)
        self.cutoff = len(self.core.notes)

    def save(self, lib=LIB.ALL):
        if not lib == LIB.CORE:
            self.local.save()
        if not lib == LIB.LOCAL:
            self.core.save()

    def pointer(self, lib=LIB.ALL, index=-1, safe=NotePointer.SAFETY.EXCEPTION) -> NotePointer:
        return WoodchipperNoteLibrary.NotePointer(lib=lib, index=index, archive=self, safe=safe)

    def get_lib_pointers(self, lib=LIB.ALL) -> [NotePointer]:
        pointers = []
        if not lib == LIB.LOCAL:
            for index in range(0, len(self.core.notes)):
                pointers.append(self.pointer(lib=LIB.CORE, index=index))
        if not lib == LIB.CORE:
            for index in range(0, len(self.local.notes)):
                pointers.append(self.pointer(lib=LIB.LOCAL, index=index))
        return pointers

    @staticmethod
    def describe_pointer(pointer) -> WoodchipperNamespace:
        nid = pointer.nid()
        note = pointer.note()
        lib = pointer.get_lib()
        return WoodchipperNoteLibrary.describe_note(note, nid, lib)


    @staticmethod
    def describe_note(note, index=-1, lib=LIB.ALL) -> WoodchipperNamespace:
        note_ns = wcutil.WoodchipperNamespace(f"Note_{index}")
        note_ns.add(RESPONSE.NOTE.INDEX, index)
        note_ns.add(RESPONSE.NOTE.TEXT, note.text)
        note_ns.add(RESPONSE.NOTE.TIME, note.time)
        note_ns.add(RESPONSE.NOTE.LIB, lib)
        return note_ns

    @staticmethod
    def describe_group(pointers) -> [WoodchipperNamespace]:
        notes = []
        for pointer in pointers:
            notes.append(WoodchipperNoteLibrary.describe_pointer(pointer))
        return notes

    def describe_library(self, lib=LIB.ALL) -> [WoodchipperNamespace]:
        pointers = self.get_lib_pointers(lib)
        return self.describe_group(pointers)

    def append_text(self, text, lib=LIB.ALL) -> WoodchipperNamespace:
        library = LIB.LOCAL if lib==LIB.ALL else lib
        archive = self.core if library==LIB.CORE else self.local
        pointer = self.pointer(lib=library, index=archive.append_text_as_note(text))
        return WoodchipperNoteLibrary.describe_pointer(pointer)

    def delete_by_nid(self, nid: int) -> WoodchipperNamespace:
        try:
            target_note_pointer: WoodchipperNoteLibrary.NotePointer = self.pointer(index=nid)
            if target_note_pointer.exists():
                note_description = WoodchipperNoteLibrary.describe_pointer(target_note_pointer)
                target_note_pointer.remove()
                return note_description
        except Exception as ex:
            ex.add_note("Invalid delete arguments.")
            raise ex

    def move_by_nid(self, target_nid: int, destination_nid: int) -> [WoodchipperNamespace]:
        try:
            target_pointer: WoodchipperNoteLibrary.NotePointer = self.pointer(index=target_nid)
            destination_pointer: WoodchipperNoteLibrary.NotePointer = self.pointer(index=destination_nid)
            if target_pointer.exists() and destination_pointer.exists():
                ret_value = [WoodchipperNoteLibrary.describe_pointer(target_pointer)]
                target_note = target_pointer.remove()
                destination_pointer = self.pointer(index=destination_nid, safe=WoodchipperNoteLibrary.NotePointer.SAFETY.NONE)
                destination_pointer.insert_note(target_note)
                ret_value.append(WoodchipperNoteLibrary.describe_pointer(destination_pointer))
                return ret_value
        except Exception as ex:
            ex.add_note("Invalid move arguments.")
            raise ex

    def update_by_nid(self, target_nid: int, updated_text: str) -> [WoodchipperNamespace]:
        try:
            target_pointer: WoodchipperNoteLibrary.NotePointer = self.pointer(index=target_nid)
            if target_pointer.exists():
                ret_value = [WoodchipperNoteLibrary.describe_pointer(target_pointer)]
                target_pointer.update_text(updated_text)
                ret_value.append(WoodchipperNoteLibrary.describe_pointer(target_pointer))
                return ret_value
        except Exception as ex:
            ex.add_note("Invalid update arguments.")
            raise ex

    def replace_by_nid(self, target_nid: int, new_text: str) -> [WoodchipperNamespace]:
        try:
            target_pointer: WoodchipperNoteLibrary.NotePointer = self.pointer(index=target_nid)
            if target_pointer.exists():
                ret_value = [WoodchipperNoteLibrary.describe_pointer(target_pointer)]
                target_pointer.replace_note(new_text)
                ret_value.append(WoodchipperNoteLibrary.describe_pointer(target_pointer))
                return ret_value
        except Exception as ex:
            ex.add_note("Invalid replace arguments.")
            raise ex

    def relocate_by_nid(self, target_nid: int) -> [WoodchipperNamespace]:
        try:
            target_pointer: WoodchipperNoteLibrary.NotePointer = self.pointer(index=target_nid)
            if target_pointer.exists():
                ret_value = [WoodchipperNoteLibrary.describe_pointer(target_pointer)]
                target_pointer.relocate_to_end_of_other_library()
                ret_value.append(WoodchipperNoteLibrary.describe_pointer(target_pointer))
                return ret_value
        except Exception as ex:
            ex.add_note("Invalid relocate arguments.")
            raise ex

    def clear_library(self, lib=LIB.ALL):
        ret_val = self.describe_library(lib)
        if not lib == LIB.LOCAL:
            self.core.clear()
        if not lib == LIB.CORE:
            self.local.clear()
        return ret_val