import interface.wctk_request as WCParser
from utilities.wcutil import WoodchipperSettingsFile as WCProfile
from utilities.wcprinter import WoodchipperToolkitPrinter as WCPrinter
from utilities.wcconstants import Verbosity
from interface.constants import MODE, HANDLER, OUT, clr_state as CLR_STATE


class WoodchipperCommandLineInterface:
    def __init__(self, printers, parser_build_function=WCParser.build_parser):
        self.profile = WCProfile()
        self.parser = parser_build_function()
        self._check_parser_for_mode()
        self.printer = WCPrinter(self.profile.verbosity)
        self.printers = printers
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
        if not results.data.success:
            self.printer.error(results.data.error)
        else:
            printer = self.printers[results.mode]
            printer(self.request, self.printer)
            printer.print()

    def _check_config(self):
        proceed, out_string, test = self.profile.check_parser(self.request)
        self.printer.verbosity = self.profile.verbosity
        if test:
            self.request.mode = MODE.TEST
            self.request.target = test
        elif not proceed:
            self.request.mode = MODE.NONE
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

    def _check_parser_for_mode(self):
        found = False
        for arg in self.parser.args:
            if arg.name == "mode":
                found = True
        if not found:
            raise Exception(f"The parser must contain a 'mode' argument, but none was found.")