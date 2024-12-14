from utilities.wcutil import WoodchipperNamespace as WCNamespace


class WoodchipperController:
    def __init__(self, handlers):
        self.request = None
        self.data = None
        self.handlers = handlers
        self.results = WCNamespace("ControllerResults")

    def process_request(self, process_request):
        self.request = process_request
        self.initialize_results()
        # if self.request.debug:
        handler = self.handlers[self.request.handler]
        self.data = handler(self.request, self.results)
        self.results.add("data", self.data)

    def initialize_results(self):
        self.results.add("mode", self.request.mode)
        self.results.add("debug", self.request.debug)
        self.results.add("error", None)
        self.results.add("success", False)
