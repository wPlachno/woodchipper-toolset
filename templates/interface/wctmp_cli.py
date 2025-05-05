import interface.wctmp_request as WCParser
from utilities.wcutil import WoodchipperSettingsFile as WCProfile
from utilities.wcprinter import WoodchipperPrinter as WCPrinter
from utilities.wcconstants import Verbosity
import interface.constants as C

class WoodchipperTemplateCommandLineInterface:
    def __init__(self, parser=WCParser.build_parser):
        self.profile = WCProfile()
        self.parser = parser()
        WCProfile.setup_argparse_parser_with_config(self.parser)
        self.printer = WCPrinter(self.profile.verbosity)
        self.request = None

    def process_request(self, args):
        self.request = self.parser.parse_args(args)
        if self._check_config():
            self._print_profile(Verbosity.DEBUG)
            self.printer.nl()
            self._print_request(Verbosity.DEBUG)
            self.printer.nl(Verbosity.DEBUG)
        return self.request

    def display_results(self, results):
        self.printer.pr(results, Verbosity.DEBUG)
        self.printer.nl(Verbosity.DEBUG)
        if not results.success:
            self.printer.v_frame(C.ERROR.CODE[results.error.code], results.error.data)
        else:
            self.printer.pr(results)

    def _check_config(self):
        proceed, out_string, test = self.profile.check_parser(self.request)
        self.printer.verbosity = self.profile.verbosity
        if test:
            self.request.mode = C.MODE.TEST
            self.request.target = test
        elif not proceed:
            self.request.mode = C.MODE.NONE
            self.printer.pr(out_string, Verbosity.RESULTS_ONLY, new_line=False)
            return False
        return True

    def _print_profile(self, verbosity=Verbosity.DEBUG):
        self.printer.label("Profile", verbosity)
        for key in self.profile.keys:
            self.printer.kvp(key, self.profile[key], verbosity)

    def _print_request(self, verbosity=Verbosity.DEBUG):
        self.printer.label("Request", verbosity)
        req = vars(self.request)
        for key in req:
            self.printer.kvp(key, req[key], verbosity)

    def ACHHOO(self):
        self.printer.pr("Functionality Unwritten.", Verbosity.NORMAL)

