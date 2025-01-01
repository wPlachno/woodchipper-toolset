# wcprinter.py
# Version: 0.0.1.000
# Last Changes: 12/25/24

from utilities.wcconstants import Verbosity, PRINT

class WoodchipperToolkitPrinter:
    def __init__(self, verbosity=Verbosity.NORMAL):
        self.verbosity = verbosity

    def verb(self, verbosity):
        return self.verbosity >= verbosity

    def pr(self, text, verbosity=Verbosity.NORMAL, new_line=True):
        end = "\n" if new_line else ""
        if self.verb(verbosity):
            print(text, end=end)

    def nl(self, verbosity=Verbosity.NORMAL):
        self.pr(text="", verbosity=verbosity)

    def error(self, text, verbosity=Verbosity.NORMAL):
        self.pr(PRINT.ERROR.format(text), verbosity)

    def label(self, text, verbosity=Verbosity.NORMAL):
        self.pr(PRINT.LABEL.format(text), verbosity)

    def kvp(self, key, value, verbosity=Verbosity.NORMAL):
        self.pr(PRINT.KVP.format(key, str(value)), verbosity)

    def v_frame(self, frame_list, *args):
        self.pr(frame_list[self.verbosity].format(*args), Verbosity.RESULTS_ONLY)



