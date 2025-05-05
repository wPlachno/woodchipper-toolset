from models.wctmp_control_file import WoodchipperTemplatingControlFile as ControlFile
from models.wctmp_token_file import WoodchipperTokenFile as TokenFile
from core.wctmp_control_stack import WoodchipperTemplateControlStack as ControlStack
from core.wctmp_errors import ERROR
import core.constants as C
from utilities.wcutil import WoodchipperNamespace as WCNamespace

class WoodchipperTemplateExpander:
    def __init__(self, file_path):
        self.path = file_path
        self.control = ControlFile(self.path)
        self.files = []

    def expand(self, force=False):
        control_stack = ControlStack(self.control)
        remaining_content = self.control.load()

        # If would overwrite an existing file and !force
        would_overwrite_file = False
        overwritten_file_name = ""
        if not force and would_overwrite_file:
            return self.buildError(ERROR.WOULD_OVERWRITE_FILE, [overwritten_file_name])

        return None

    def save(self):
        for file in self.files:
            file.save()

    def toNamespace(self):
        ns = WCNamespace("extender")
        ns.add(C.KEY.EXPANDER.CONTROL, self.control.toNamespace())
        ns.add(C.KEY.EXPANDER.FILES, [])
        for file in self.files:
            ns.files.append(file.toNamespace())
        return ns

    @staticmethod
    def buildError(error, data=None):
        ns = WCNamespace("Error")
        ns.add("code", error)
        ns.add("data", data)
        return ns
