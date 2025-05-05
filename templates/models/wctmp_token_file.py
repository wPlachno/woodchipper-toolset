from models.wctmp_file import WoodchipperTemplatingFile as WCFile

class WoodchipperTokenFile(WCFile):
    def __init__(self, file_path, replacement_text=None):
        WCFile.__init__(self, file_path)
        self.replacement_text = replacement_text

    def get_replacement(self):
        if self.replacement_text:
            return self.replacement_text
        return ""
