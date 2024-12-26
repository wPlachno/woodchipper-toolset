# wcmodehandler.py
# Version: 0.0.1.000
# Last Changes: 12/25/24

class WoodchipperCoreModeHandler:
    def __init__(self, request: any, response: any):
        self.request = request
        self.response = response

    def handle(self):
        return True