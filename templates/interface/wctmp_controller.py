from utilities.wcutil import WoodchipperNamespace as WCNamespace
from core.wctmp_expander import WoodchipperTemplateExpander as WCExpander
import interface.constants as C


class WoodchipperController:
    def __init__(self):
        self.request = None
        self.data = None
        self.affect_file_system = True
        self.results = WCNamespace("ControllerResults")

    def process_request(self, process_request):
        self.request = process_request
        if self.request.debug:
            self.affect_file_system = False
        self._initialize_results()
        self._handle_request()

    def _initialize_results(self):
        self.results.add(C.KEY.RESULTS.DEBUG, self.request.debug)
        self.results.add(C.KEY.RESULTS.ERROR, None)
        self.results.add(C.KEY.RESULTS.SUCCESS, False)
        self.results.add(C.KEY.RESULTS.EXPANDER, None)

    def _handle_request(self):
        if not self.request.path:
            self.results.error = WCExpander.buildError(C.ERROR.NO_CONTROL_FILE.CODE)
        else:
            expander = WCExpander(self.request.path)
            self.results.error = expander.expand()
            self.results.success = self.results.error is None
            self.results.expander = expander.toNamespace()
