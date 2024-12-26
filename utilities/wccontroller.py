# wccontroller.py
# Version: 0.0.1.000
# Last Changes: 12/25/24

from utilities.wcresponse import WoodchipperCoreResponse as WCResponse

class WoodchipperController:
    def __init__(self, handlers):
        self.request = None
        self.data = None
        self.handlers = handlers
        self.results = WCResponse()

    def process_request(self, process_request):
        self.request = process_request
        self.results.build_from_request(self.request)
        handler_id = self.request.mode
        if handler_id:
            self.results.mode = handler_id
            handler_type = self.handlers[handler_id]
            handler = handler_type(self.request, self.results)
            self.data = handler.handle()
            self.results.data = self.data
            self.results.success = True
        else:
            self.results.error = "Unable to figure out which handler should operate on the request."