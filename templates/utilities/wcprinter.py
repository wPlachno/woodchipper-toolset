from utilities.wcconstants import Verbosity
from interface import constants as C


class WoodchipperPrinter:
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
        self.pr(C.OUT.ERROR.format(text), verbosity)

    def label(self, text, verbosity=Verbosity.NORMAL):
        self.pr(C.S.COLOR_SUPER+text+C.S.COLOR_DEFAULT + C.S.CS, verbosity)

    def kvp(self, key, value, verbosity=Verbosity.NORMAL):
        self.pr(C.S.COLOR_SIBLING+key+C.S.COLOR_DEFAULT+ C.S.CS +str(value), verbosity)

    def v_frame(self, frame_list, *args):
        self.pr(frame_list[self.verbosity].format(*args), Verbosity.RESULTS_ONLY)



