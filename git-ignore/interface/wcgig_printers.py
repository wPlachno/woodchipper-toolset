# wcgig_printers.py
# Version: 0.0.0.001
# 12/26/24

from utilities.wcmodeprinter import WoodchipperCoreModePrinter as WCPrinter
from constants import NODE as describe_node
from utilities.wcconstants import Verbosity

class WoodchipperGignorePrinter(WCPrinter):
    def __init__(self, request, response):
        WCPrinter.__init__(self, request, response)

    def print(self):
        for node in self.data.nodes:
            self.printer.pr(describe_node(node["name"], node["status"]), Verbosity.NORMAL)