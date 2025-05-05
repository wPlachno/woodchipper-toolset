# gignore.py
# Written by: Will Plachno
# Created: 08/27/2024
# Version: 0.0.1.001
# Last Changed: 05/05/2025

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from utilities.wccore import WoodchipperCore as WCCore
from constants import MODE
from interface.wcgig_printers import WoodchipperGignorePrinter as printer
import interface.wcgig_parser as my_parser
import core.wcgig_handlers as handlers

def _main(args):
    core = WCCore()
    core.set_parser_builder(my_parser.build_parser)
    core.set_debug_mode_description("No file editing will be completed when debug mode is active.")
    core.add_mode(MODE.SHOW, handlers.WoodchipperGignoreHandlerShow, printer)
    core.add_mode(MODE.ADD, handlers.WoodchipperGignoreHandlerAdd, printer)
    core.add_mode(MODE.SETUP, handlers.WoodchipperGignoreHandlerSetup, printer)
    core.add_mode(MODE.REMOVE, handlers.WoodchipperGignoreHandlerRemove, printer)
    core.add_mode(MODE.CLEAR, handlers.WoodchipperGignoreHandlerClear, printer)
    core.run()

if __name__ == "__main__":
    _main(sys.argv)
