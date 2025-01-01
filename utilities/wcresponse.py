# wcresponse.py
# Version: 0.0.1.010
# Last Changes: 01/01/2025


class WoodchipperCoreResponse:
    def __init__(self):
        self.request = None
        self.mode = "none"
        self.debug = False
        self.error = None
        self.success = False
        self.data = None

    def build_from_request(self, request):
        self.request = request
        self.mode = self.request.mode
        self.debug = self.request.debug
        self.error = None
        self.success = False
        self.data = None

    def __str__(self):
        if self.success:
            return f"SUCCESS: [{self.data}]"
        else:
            return f"ERROR: [{self.error}]"
