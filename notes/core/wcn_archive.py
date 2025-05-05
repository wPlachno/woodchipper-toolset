# wcn_archive.py
# Created: Will Plachno on 8/22/24
# Version: 0.0.2.001
# Last Changed: 01/11/2025

import constants as S
from utilities.wcutil import WoodChipperFile as Scribe
from core.wcn_note import WoodchipperNote
from pathlib import Path

""" wcn_archive.py

This file contains the WoodchipperNoteArchive class, which is a model class of a collection of notes 
stored in a single file. The WoodchipperNoteArchive is a hidden file in which WoodchipperNotes are saved, 
1 per line.
The lifetime of the WoodchipperNoteArchive class consists of the object getting initialized with default values,
then given a path and loading the file. At this point, the user does whatever to the WoodchipperNoteArchive as
necessary, then calls the save function when the changes should be committed.
"""

class WoodchipperNoteArchive:
    def __init__(self):
        self.path: Path|None = None
        self.notes: [WoodchipperNote] = []
        self.file: Scribe|None = None

    def append_text_as_note(self, text: str) -> int:
        new_note: WoodchipperNote = WoodchipperNote()
        new_note.define(text)
        index: int = len(self.notes)
        self.notes.append(new_note)
        return index

    def append_note(self, note: WoodchipperNote) -> int:
        index: int = len(self.notes)
        self.notes.append(note)
        return index

    def remove(self,index: int) -> WoodchipperNote:
        return self.notes.pop(index)

    def clear(self):
        while len(self.notes):
            self.notes.pop()

    def insert(self, target_index: int, note: WoodchipperNote):
        self.notes.insert(target_index, note)

    def move(self, target: int, destination: int):
        dest: int = destination
        if dest != target:
            if dest > target:
                dest = dest-1
            target_note: WoodchipperNote = self.notes.pop(target)
            self.notes.insert(dest, target_note)

    def edit(self, index: int, text: str):
        self.notes[index].text = text

    def reset(self, index: int, text: str):
        self.notes[index].define(text)

    def load(self, path: Path):
        self.path = path
        self.file = Scribe(path)
        self.file.read()
        for line in self.file.text:
            if line != S.EMPTY and line != S.NL:
                new_note: WoodchipperNote = WoodchipperNote()
                self.notes.append(new_note.read(line))

    def save(self):
        file_text: [str] = list(())
        for index in range(0,len(self.notes)):
            file_text.append(self.notes[index].write())
        self.file.text = file_text
        self.file.write()