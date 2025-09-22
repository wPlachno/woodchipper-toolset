# wcn_printer.py
# Written By: Will Plachno
# Created: 01/08/2025
# Version: 0.0.1.002
# Last Changed: 01/08/2025


from utilities.wcmodeprinter import WoodchipperCoreModePrinter as WCPrinter
from utilities.wcconstants import Verbosity, clr, COLOR
from interface.wcn_colorStack import ColorStack
from constants import SECTION, NOTES, HEADERS, TIME_READABLE

class WoodchipperNotePrinterDefault(WCPrinter):
    def __init__(self, request, response):
        WCPrinter.__init__(self, request, response)
        self.stack = ColorStack()

    def print(self):
        if WCPrinter.print(self):
            self.printer.pr(HEADERS[self.response.mode])
            if len(self.data.notes) > 0:
                self.print_notes()
            else:
                self.printer.pr("None")

    def print_notes(self):
        for note in self.data.notes:
            self.print_note(note)

    def print_note(self, data):
        note_id = data.index
        timestamp=data.timestamp
        text=data.text
        if ":" in text:
            text_pieces = text.split(":")
            key = text_pieces[0]
            value = ":".join(text_pieces[1:])
            key_color = self.stack.check(key)
            text = clr(key, key_color) + ":" + value
        section=SECTION.FROM_LIB[data.library]
        frame = NOTES.LOCAL if section == SECTION.LOCAL else NOTES.CORE
        self.printer.pr(frame.format(note_id,timestamp.strftime(TIME_READABLE), text), Verbosity.NORMAL)

class WoodchipperNotePrinterStateful(WoodchipperNotePrinterDefault):
    def print_notes(self):
        prev_state = self.data.notes[0]
        self.printer.pr("From: ", new_line=False)
        self.print_note(prev_state)
        new_state = self.data.notes[1]
        self.printer.pr("To:   ", new_line=False)
        self.print_note(new_state)