from types import SimpleNamespace

from wctk_archive import WoodchipperArchive as WCArchive
from wcutil import WoodchipperNamespace as WCNamespace
import wctk_handler as WCHandlers
import constants as C

class WoodchipperController:
    def __init__(self):
        self.archive = None
        self.request = None
        self.handler = None
        self.data = None
        self.file_name = C.FILE_NAME.ARCHIVE
        self.results = WCNamespace("ControllerResults")

    def process_request(self, process_request):
        self.request = process_request
        if self.request.debug:
            self.file_name = C.FILE_NAME.DEBUG
        self.archive = WCArchive(self.file_name)
        self.archive.load()
        self.handler = self._choose_handler()
        self._initialize_results()
        self.data = self.handler.handle()
        self.results.add("data", self.data)

    def _choose_handler(self):
        match self.request.mode:
            case C.MODE.ADD:
                return WCHandlers.WoodchipperHandlerAdd(self.request, self.archive)
            case C.MODE.PUSH:
                return WCHandlers.WoodchipperHandlerPush(self.request, self.archive)
            case C.MODE.GRAB:
                return WCHandlers.WoodchipperHandlerGrab(self.request, self.archive)
            case C.MODE.SHOW:
                return WCHandlers.WoodchipperHandlerShow(self.request, self.archive)

    def _initialize_results(self):
        self.results.add("mode", self.request.mode)
        self.results.add("debug", self.request.debug)
        self.results.add("target", self.request.target)
        self.results.add("path", self.request.path)

