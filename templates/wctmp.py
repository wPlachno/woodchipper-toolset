
import sys

from interface.constants import MODE
from interface.wctmp_cli import WoodchipperTemplateCommandLineInterface as WCCLI
from interface.wctmp_controller import WoodchipperController as WCController

def _main(args):
    cli = WCCLI()
    control = WCController()
    process_request = cli.process_request(sys.argv)
    if not process_request.mode == MODE.NONE:
        control.process_request(process_request)
        cli.display_results(control.results)

if __name__ == "__main__":
    _main(sys.argv)