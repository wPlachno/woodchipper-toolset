import interface.wctk_request as WCParser
from utilities.wcutil import WoodchipperSettingsFile as WCProfile
from utilities.wcprinter import WoodchipperToolkitPrinter as WCPrinter
from utilities.wcconstants import Verbosity
from interface.constants import MODE, HANDLER, OUT, clr_state as CLR_STATE


class WoodchipperToolkitCommandLineInterface:
    def __init__(self):
        self.profile = WCProfile()
        self.parser = WCParser.build_parser()
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
        if not results.data.success:
            self.printer.error(results.data.error)
        else:
            printer = self.printer.pr
            match results.data.handler:
                case HANDLER.GRAB.TOOLKIT:
                    printer = self._print_grab_toolkit
                case HANDLER.GRAB.CLONE:
                    printer = self._print_grab_clone
                case HANDLER.PUSH.TOOLKIT:
                    printer = self._print_push_toolkit
                case HANDLER.PUSH.CLONE:
                    printer = self._print_push_clone
                case HANDLER.ADD.TOOLKIT:
                    printer = self._print_add_toolkit
                case HANDLER.ADD.CLONE:
                    printer = self._print_add_clone
                case HANDLER.SHOW.TOOLKIT:
                    printer = self._print_show_toolkit
                case HANDLER.SHOW.CLONE:
                    printer = self._print_show_clone
                case HANDLER.SHOW.ALL:
                    printer = self._print_show_all
            printer(results)

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

    def _print_add_toolkit(self, results):
        tk = results.data.toolkit
        self.printer.v_frame(OUT.ADD.TOOLKIT, tk.name, tk.path)

    def _print_add_clone(self, results):
        tk = results.data.toolkit
        cl = results.data.clone
        frame_list = OUT.ADD.CLONE.REGISTERED if results.data.existed else OUT.ADD.CLONE.DUPLICATED
        self.printer.v_frame(frame_list, tk.name, cl.name, cl.path, tk.path)

    def _print_push_toolkit(self, results):
        tk = results.data.toolkit
        clones = results.data.clones
        header_frame = OUT.PUSH.TOOLKIT.HEADER
        self.printer.v_frame(header_frame, tk.name, tk.path)
        for clone in clones:
            clone_frame = OUT.PUSH.TOOLKIT.ITEM.SUCCESS if clone.replaced else OUT.PUSH.TOOLKIT.ITEM.FAILED
            self.printer.v_frame(clone_frame, clone.name, clone.path, clone.error)


    def _print_push_clone(self, results):
        tk = results.data.toolkit
        cl = results.data.clone
        clone_frame = OUT.PUSH.TOOLKIT.ITEM.SUCCESS if cl.replaced else OUT.PUSH.TOOLKIT.ITEM.FAILED
        self.printer.v_frame(clone_frame, cl.name, cl.path, cl.error)


    def _print_grab_toolkit(self, results):
        tk = results.data.toolkit
        frame = OUT.GRAB.TOOLKIT
        self.printer.v_frame(frame, tk.name, tk.version, tk.old_version)

    def _print_grab_clone(self, results):
        tk = results.data.toolkit
        cl = results.data.clone
        frame = OUT.GRAB.CLONE
        self.printer.v_frame(frame, tk.name, cl.name, cl.path, cl.version)

    def _print_show_all(self, results):
        toolkits = results.data.toolkits
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


    def _print_show_toolkit(self, results):
        toolkit = results.data.toolkit
        self.printer.v_frame(OUT.SHOW.TOOLKIT.HEADER, toolkit.name, toolkit.version, CLR_STATE(toolkit.state), toolkit.path)
        if len(results.data.clones) > 0:
            clone_str = ""
            clone_frame = OUT.SHOW.TOOLKIT.LIST_ITEM[self.printer.verbosity]
            for clone in results.data.clones:
                clone_str += clone_frame.format(clone.name, clone.version, CLR_STATE(clone.state), clone.path)
            if self.printer.verbosity == Verbosity.RESULTS_ONLY:
                clone_str = clone_str[:-2]
            self.printer.pr(clone_str, Verbosity.RESULTS_ONLY, False)
        else:
            self.printer.pr(OUT.SHOW.TOOLKIT.NO_CLONES)

    def _print_show_clone(self, results):
        tk = results.data.toolkit
        cl = results.data.clone
        self.printer.v_frame(OUT.SHOW.CLONE.DESCRIPTION, tk.name, cl.name, cl.version, CLR_STATE(cl.state), cl.path)
        self.printer.v_frame(OUT.SHOW.CLONE.DIFF_HEADER, tk.name, cl.name, tk.path, cl.path)
        if (results.data.diff is None) or (len(results.data.diff) == 0):
            self.printer.pr(OUT.SHOW.CLONE.NO_CHANGES)
        else:
            for line in results.data.diff:
                self.printer.pr(line, Verbosity.RESULTS_ONLY, new_line=False)




    def ACHHOO(self):
        self.printer.pr("Functionality Unwritten.", Verbosity.NORMAL)

