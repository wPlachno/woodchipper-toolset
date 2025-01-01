# wccore.py
# Version: 0.0.1.000
# Last Changes: 12/25/24

import sys

from utilities.wccli import WoodchipperCommandLineInterface as WCCLI
from utilities.wccontroller import WoodchipperController as WCController
from utilities.wcmodehandler import WoodchipperCoreModeHandler as WCHandler
from utilities.wcmodeprinter import WoodchipperCoreModePrinter as WCPrinter
from utilities.wcparser import CLParser as WCParser
from utilities.wcutil import WoodchipperDictionary as WCDict, int_from_string, bool_from_user

class WoodchipperCore:
    def __init__(self: any):
        self.handlers = WCDict(default_value=WCHandler)
        self.printers = WCDict(default_value=WCPrinter)
        self.parser_builder = WoodchipperCore.default_parser
        self.debug_mode_description = "Runs the script in debug mode."

    def set_parser_builder(self, build_func: callable):
        self.parser_builder = build_func
        return self

    def set_debug_mode_description(self, desc: str):
        self.debug_mode_description = desc
        return self

    def add_mode(self, key: str, handler: type[WCHandler], printer: type[WCPrinter], default:bool=False):
        self.handlers[key] = handler
        self.printers[key] = printer
        if default:
            self.handlers["default"] = handler
            self.printers["default"] = printer
        return self

    def run(self):
        cli = self.build_cli()
        control = self.build_controller()
        process_request = cli.process_request(sys.argv)
        if not process_request.mode == "none":
            control.process_request(process_request)
            cli.display_results(control.results)

    def build_parser_function(self) -> WCParser:
        parser = self.parser_builder()
        parser.add_argument("--version",
                            description="Prints the version of the script.")
        parser.add_argument("-h", "--help",
                            description="Prints this help documentation.")
        parser.add_argument("-c", "--config", default=False,
                            description="Limits script completion to configuration settings.")
        parser.add_argument("-v", "--verbosity", shaper=int_from_string, nargs=1,
                            description="Sets how complete the script printing will be.\n0: No printing.\n1: Success/Fail only.\n2: Descriptive, user-based output.\n3. Verbose yet succinct output for developers.")
        parser.add_argument("-d", "--debug", shaper=bool_from_user, nargs=1,
                            description=self.debug_mode_description)
        parser.add_argument("--test", nargs=1, hide=True)
        if not WoodchipperCore.check_for_mode(parser.args):
            parser.add_argument("mode", hide=True,
                                description="The mode we are operating in.")
        return parser

    def build_cli(self) -> WCCLI:
        return WCCLI(self.printers, self.build_parser_function)

    def build_controller(self) -> WCController:
        return WCController(self.handlers)

    @staticmethod
    def default_parser(*args) -> WCParser:
            parser = WCParser("unknown script",
                              version="0.0.0.1",
                              description="Unknown",
                              footer="Created by Will Plachno. Copyright 2024.")
            parser.add_argument("target",
                                description="The target for the script.")
            parser.add_argument("mode",
                                description="The mode we are operating in.")
            return parser

    @staticmethod
    def check_for_mode(args):
        for arg in args:
            if arg.name == "mode":
                return True
        return False