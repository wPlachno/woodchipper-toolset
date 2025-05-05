from utilities.wcmodeprinter import WoodchipperCoreModePrinter as WCPrinter
from interface.constants import HANDLER, OUT, clr_state as CLR_STATE
from utilities.wcconstants import Verbosity

class WoodchipperToolkitPrinter(WCPrinter):
    def __init__(self, response, printer):
        WCPrinter.__init__(self, response, printer)
        self.target = self.response.data.target

    def print(self):
        if self.target == HANDLER.TARGET.ALL:
            return self.print_all()
        elif self.target == HANDLER.TARGET.TOOLKIT:
            return self.print_toolkit()
        else:
            return self.print_clone()

    def print_all(self):
        return True

    def print_toolkit(self):
        return True

    def print_clone(self):
        return True

class WoodchipperToolkitPrinterShow(WoodchipperToolkitPrinter):

    def print_all(self):
        toolkits = self.data.toolkits
        if len(toolkits) == 0:
            self.printer.pr(OUT.SHOW.ALL.NO_TOOLKITS, Verbosity.RESULTS_ONLY)
        else:
            self.printer.pr(OUT.SHOW.ALL.HEADER.format(len(toolkits)), Verbosity.NORMAL)
            toolkit_str = ""
            frame = OUT.SHOW.ALL.LIST_ITEM[self.printer.verbosity]
            for toolkit in sorted(toolkits, key=lambda tk: tk.name):
                toolkit_str += frame.format(toolkit.name, toolkit.version, CLR_STATE(toolkit.state), toolkit.path)
            if self.printer.verbosity == Verbosity.RESULTS_ONLY:
                toolkit_str = toolkit_str[:-2]
            self.printer.pr(toolkit_str, Verbosity.RESULTS_ONLY, False)
        return True

    def print_toolkit(self):
        toolkit = self.data.toolkit
        self.printer.v_frame(OUT.SHOW.TOOLKIT.HEADER, toolkit.name, toolkit.version, CLR_STATE(toolkit.state), toolkit.path)
        if len(self.data.clones) > 0:
            clone_str = ""
            clone_frame = OUT.SHOW.TOOLKIT.LIST_ITEM[self.printer.verbosity]
            for clone in self.data.clones:
                clone_str += clone_frame.format(clone.name, clone.version, CLR_STATE(clone.state), clone.path)
            if self.printer.verbosity == Verbosity.RESULTS_ONLY:
                clone_str = clone_str[:-2]
            self.printer.pr(clone_str, Verbosity.RESULTS_ONLY, False)
        else:
            self.printer.pr(OUT.SHOW.TOOLKIT.NO_CLONES)
        return True

    def print_clone(self):
        tk = self.data.toolkit
        cl = self.data.clone
        self.printer.v_frame(OUT.SHOW.CLONE.DESCRIPTION, tk.name, cl.name, cl.version, CLR_STATE(cl.state), cl.path)
        self.printer.v_frame(OUT.SHOW.CLONE.DIFF_HEADER, tk.name, cl.name, tk.path, cl.path)
        if (self.data.diff is None) or (len(self.data.diff) == 0):
            self.printer.pr(OUT.SHOW.CLONE.NO_CHANGES)
        else:
            for line in self.data.diff:
                self.printer.pr(line, Verbosity.RESULTS_ONLY, new_line=False)
        return True

class WoodchipperToolkitPrinterAdd(WoodchipperToolkitPrinter):

    def print_all(self):
        return True

    def print_toolkit(self):
        tk = self.data.toolkit
        self.printer.v_frame(OUT.ADD.TOOLKIT, tk.name, tk.path)
        return True

    def print_clone(self):
        tk = self.data.toolkit
        cl = self.data.clone
        frame_list = OUT.ADD.CLONE.REGISTERED if self.data.existed else OUT.ADD.CLONE.DUPLICATED
        self.printer.v_frame(frame_list, tk.name, cl.name, cl.path, tk.path)
        return True

class WoodchipperToolkitPrinterPush(WoodchipperToolkitPrinter):

    def print_all(self):
        return True

    def print_toolkit(self):
        tk = self.data.toolkit
        clones = self.data.clones
        header_frame = OUT.PUSH.TOOLKIT.HEADER
        self.printer.v_frame(header_frame, tk.name, tk.path)
        for clone in clones:
            clone_frame = OUT.PUSH.TOOLKIT.ITEM.SUCCESS if clone.replaced else OUT.PUSH.TOOLKIT.ITEM.FAILED
            self.printer.v_frame(clone_frame, clone.name, clone.path, clone.error)
        return True

    def print_clone(self):
        tk = self.data.toolkit
        cl = self.data.clone
        clone_frame = OUT.PUSH.TOOLKIT.ITEM.SUCCESS if cl.replaced else OUT.PUSH.TOOLKIT.ITEM.FAILED
        self.printer.v_frame(clone_frame, cl.name, cl.path, cl.error)
        return True

class WoodchipperToolkitPrinterGrab(WoodchipperToolkitPrinter):

    def print_all(self):
        return True

    def print_toolkit(self):
        tk = self.data.toolkit
        frame = OUT.GRAB.TOOLKIT
        self.printer.v_frame(frame, tk.name, tk.version, tk.old_version)
        return True

    def print_clone(self):
        tk = self.data.toolkit
        cl = self.data.clone
        frame = OUT.GRAB.CLONE
        self.printer.v_frame(frame, tk.name, cl.name, cl.path, cl.version)
        return True