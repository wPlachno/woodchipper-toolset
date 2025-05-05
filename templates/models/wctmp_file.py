import pathlib
from utilities.wcutil import WoodchipperNamespace as WCNamespace
from models.constants import KEY

class WoodchipperTemplatingFile:
    def __init__(self, file_path):
        self.path = pathlib.Path(file_path)
        self.content = ""

    def name(self):
        return self.path.name

    def exists(self):
        return self.path.exists()

    def load(self):
        with (open(self.path, 'r')
              as text_file):
            self.content = text_file.read()
        return self.content

    def save(self):
        with (open(self.path, 'w')
              as text_file):
            text_file.write(self.content)

    def add(self, text):
        self.content += text

    def toNamespace(self):
        ns = WCNamespace(self.name())
        ns.add(KEY.FILE.NAME, self.name())
        ns.add(KEY.FILE.PATH, self.path)
        ns.add(KEY.FILE.CONTENT, self.content)
        return ns
