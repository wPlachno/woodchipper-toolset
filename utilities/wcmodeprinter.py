# wcmodeprinter.py
# Written by: Will Plachno
# Created: 12/24/2024
# Version: 0.0.1.011
# Last Changes: 01/07/25

from utilities.wcprinter import WoodchipperToolkitPrinter
from utilities.wcconstants import Verbosity, CL_GENERAL

class WoodchipperCoreModePrinter:
    def __init__(self, response: any, printer: WoodchipperToolkitPrinter):
        self.response = response
        self.data = self.response.data
        self.printer = printer

    def print(self):
        if self.printer.verbosity == Verbosity.RESULTS_ONLY:
            self.printer.on_bool(self.data.success, CL_GENERAL.SUCCESS, CL_GENERAL.FAILURE, Verbosity.RESULTS_ONLY)
            return False
        elif self.printer.verbosity == Verbosity.SILENT:
            return False
        else:
            return True