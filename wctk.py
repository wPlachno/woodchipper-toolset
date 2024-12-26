# wctk.py
# Version: 0.0.1.001
# Will Plachno, 12/26/2024

import sys

from utilities.wccore import WoodchipperCore as WCCore
from interface.constants import MODE
import interface.wctk_printer as printers
import interface.wctk_request as my_parser
import core.wctk_handlers as handlers


def _main(args):
    core = WCCore()
    core.set_parser_builder(my_parser.build_parser)
    core.set_debug_mode_description("No file editing will be completed when debug mode is active.")
    core.add_mode(MODE.SHOW, handlers.WoodchipperHandlerShow, printers.WoodchipperToolkitPrinterShow)
    core.add_mode(MODE.ADD, handlers.WoodchipperHandlerAdd, printers.WoodchipperToolkitPrinterAdd)
    core.add_mode(MODE.PUSH, handlers.WoodchipperHandlerPush, printers.WoodchipperToolkitPrinterPush)
    core.add_mode(MODE.GRAB, handlers.WoodchipperHandlerGrab, printers.WoodchipperToolkitPrinterGrab)
    core.run()


if __name__ == "__main__":
    _main(sys.argv)