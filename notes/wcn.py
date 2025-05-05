# wcn.py
# Written by: Will Plachno
# Created: 08/22/24
# Version: 0.0.2.001
# Last Changed: 01/08/2025

import sys

from utilities.wccore import WoodchipperCore as WCCore
import interface.wcn_parser as my_parser
import core.wcn_handler as handlers
import interface.wcn_printer as printers
from constants import MODE

def _main(args):
    core = WCCore()
    core.set_parser_builder(my_parser.build_parser)
    core.set_post_parser(my_parser.post_parser)
    core.set_debug_mode_description("Debug mode enters a separate note system so that testing can be done without altering your existing notes.")
    core.add_mode(MODE.SHOW, handlers.WoodchipperNoteHandlerShow, printers.WoodchipperNotePrinterDefault)
    core.add_mode(MODE.ADD, handlers.WoodchipperNoteHandlerAdd, printers.WoodchipperNotePrinterDefault)
    core.add_mode(MODE.REMOVE, handlers.WoodchipperNoteHandlerRemove, printers.WoodchipperNotePrinterDefault)
    core.add_mode(MODE.MOVE, handlers.WoodchipperNoteHandlerMove, printers.WoodchipperNotePrinterStateful)
    core.add_mode(MODE.UPDATE, handlers.WoodchipperNoteHandlerUpdate, printers.WoodchipperNotePrinterStateful)
    core.add_mode(MODE.REPLACE, handlers.WoodchipperNoteHandlerReplace, printers.WoodchipperNotePrinterStateful)
    core.add_mode(MODE.CLEAR, handlers.WoodchipperNoteHandlerClear, printers.WoodchipperNotePrinterDefault)
    core.run()

if __name__ == "__main__":
    _main(sys.argv)
