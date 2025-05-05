# wcn_note.py
# Created: Will Plachno on 8/22/24
# Version: 0.0.2.001
# Last Changed: 01/11/2025

import constants as S
from datetime import datetime

# wcn_note.py
# This file contains the WoodchipperNote class, which is a model class of an individual note.
# A note consists of a timestamp and some text.

class WoodchipperNote:
    def __init__(self):
        self.time: datetime = datetime.now()
        self.text: str = S.EMPTY

    def __str__(self) -> str:
        return S.COLOR_SUB+self.time.strftime(S.TIME_READABLE)+S.COLOR_DEFAULT+" - "+self.text

    def read(self, record: str):
        record_pieces = record.split(S.NOTE_DELIMITER)
        self.time = datetime.fromtimestamp(float(record_pieces[0]))
        self.text = record_pieces[1]
        return self

    def write(self) -> str:
        return self.time.strftime(S.TIME_EPOCH)+S.NOTE_DELIMITER+self.text+S.NOTE_DELIMITER+S.NL

    def define(self, text: str):
        self.time = datetime.now()
        self.text = text


