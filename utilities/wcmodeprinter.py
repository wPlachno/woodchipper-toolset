# wcmodeprinter.py
# Version: 0.0.1.010
# Last Changes: 12/25/24

from utilities.wcprinter import WoodchipperToolkitPrinter

class WoodchipperCoreModePrinter:
    def __init__(self, response: any, printer: WoodchipperToolkitPrinter):
        self.response = response
        self.data = self.response.data
        self.printer = printer

    def print(self):
        self.printer.pr(self.data)