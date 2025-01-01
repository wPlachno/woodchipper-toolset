# wcmodehandler.py
# Version: 0.0.1.001
# Last Changes: 01/01/2025 - Made default handler debug aware

class WoodchipperCoreModeHandler:
    def __init__(self, request: any, response: any):
        self.request = request
        self.response = response
        self.debug = request.debug

    def handle(self):
        return True