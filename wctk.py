
import sys

from interface.constants import MODE
from interface.wctk_cli import WoodchipperToolkitCommandLineInterface as WCCLI
from interface.wctk_controller import WoodchipperController as WCController
from utilities.wccore import WoodchipperCore as WCCore
import interface.wctk_request as my_parser
import core.wtck_handlers as handlers
import interface.wctk_printer as printers


""" Todo
- build out the wctk_controller pipelines 
- build out the WoodchipperToolkit and WoodchipperToolkitClone classes 
- No target specified errors, wctk_handlers.handle_all
"""


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