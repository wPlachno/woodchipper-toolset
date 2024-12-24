from utilities.wcutil import WoodchipperNamespace as WCNamespace
from wcresponse import WoodchipperCoreResponse as WCResponse


class WoodchipperController:
    def __init__(self, handlers):
        self.request = None
        self.data = None
        self.handlers = handlers
        self.results = WCResponse()

    def process_request(self, process_request):
        self.request = process_request
        self.results.build_from_request(self.request)
        # if self.request.debug:
        handler_id = self.request.mode
        if handler_id:
            self.results.mode = handler_id
            handler_type = self.handlers[handler_id]
            handler = handler_type(self.request, self.results)
            self.data = handler.handle()
            self.results.data = self.data
        else:
            self.results.error = "Unable to figure out which handler should operate on the request."