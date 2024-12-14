import sys

import utilities.wcconstants as C
from utilities.wccli import WoodchipperCommandLineInterface as WCCLI
from utilities.wccontroller import WoodchipperController as WCController
from utilities.wcparser import CLParser as WCParser
from utilities.wcutil import WoodchipperDictionary as WCDict, int_from_string, bool_from_user

class WoodchipperCore:
    def __init__(self):
        self.handlers = WCDict(default_value=WoodchipperCore.default_handler)
        self.printers = WCDict(default_value=WoodchipperCore.default_printer)
        self.parser_builder = WoodchipperCore.default_parser
        self.debug_mode_description = "Runs the script in debug mode."

    def set_parser_builder(self, build_func):
        self.parser_builder = build_func

    def set_debug_mode_description(self, desc):
        self.debug_mode_description = desc

    def add_mode(self, key, handler, printer):
        self.handlers[key] = handler
        self.printers[key] = printer

    def run(self):
        cli = self.build_cli()
        control = self.build_controller()
        process_request = cli.process_request(sys.argv)
        if not process_request.mode == C.MODE.NONE:
            control.process_request(process_request)
            cli.display_results(control.results)

    def build_parser_function(self):
        parser = self.parser_builder()
        parser.add_argument("--version",
                            description="Prints the version of the script.")
        parser.add_argument("-h", "--help",
                            description="Prints this help documentation.")
        parser.add_argument("-c", "--config", default=False,
                            description="Limits script completion to configuration settings.")
        parser.add_argument("-v", "--verbosity", shaper=int_from_string, nargs=1,
                            description="Sets how complete the script printing will be.\n0: No printing.\n1: Success/Fail only.\n3:Descriptive, user-based output.\n4.Verbose yet succinct output for developers.")
        parser.add_argument("-d", "--debug", shaper=bool_from_user, nargs=1,
                            description=self.debug_mode_description)
        parser.add_argument("--test", nargs=1, hide=True)
        return parser

    def build_cli(self):
        return WCCLI(self.printers, parser_build_function=self.build_parser_function)

    def build_controller(self):
        return WCController(self.handlers)

    @staticmethod
    def default_handler(*args):
        return args

    @staticmethod
    def default_printer(*args):
        print(args)

    @staticmethod
    def default_parser(*args):
            parser = WCParser("unknown script",
                              version="0.0.0.1",
                              description="Unknown",
                              footer="Created by Will Plachno. Copyright 2024.")
            parser.add_argument("mode",
                                description="The mode we are operating in.")
            parser.add_argument("target",
                                description="The target for the script.")
            return parser
