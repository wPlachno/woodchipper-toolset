from models.wctmp_file import KEY, WoodchipperTemplatingFile as WCFile

class WoodchipperTemplatingControlFile(WCFile):
    def __init__(self, file_path):
        WCFile.__init__(self, file_path)
        self.draft = ""

    def add(self, text):
        self.draft += text

    def save(self):
        with (open(self.path, 'w')
              as text_file):
            text_file.write(self.draft)

    def toNamespace(self):
        ns = WCFile.toNamespace(self)
        ns.add(KEY.FILE.CONTROL, self.content)
        ns.add(KEY.FILE.CONTENT, self.draft)
        return ns