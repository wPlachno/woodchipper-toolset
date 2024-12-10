
import sys

from interface.constants import MODE
from interface.wctk_cli import WoodchipperToolkitCommandLineInterface as WCCLI
from interface.wctk_controller import WoodchipperController as WCController



""" Todo
- build out the wctk_controller pipelines 
- build out the WoodchipperToolkit and WoodchipperToolkitClone classes 
- No target specified errors, wctk_handlers.handle_all
"""


def _main(args):
    cli = WCCLI()
    control = WCController()
    process_request = cli.process_request(sys.argv)
    if not process_request.mode == MODE.NONE:
        control.process_request(process_request)
        cli.display_results(control.results)

if __name__ == "__main__":
    _main(sys.argv)