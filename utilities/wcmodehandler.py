

class WoodchipperCoreModeHandler:
    def __init__(self, request: any, response: any):
        self.request = request
        self.response = response

    def handle(self):
        return True