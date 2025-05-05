# wcgig_handlers.py
# Created: 12/26/24
# Version: 0.0.0.002
# Last Changed: 01/04/2025

from pathlib import Path
from os import getcwd
from constants import FILE_NAME_GIT_IGNORE as gig_file_name, RESPONSE, ERROR
from utilities.wcmodehandler import WoodchipperCoreModeHandler as WCHandler
from default_nodes import setup_defaults as setup_nodes
from utilities.wcutil import WoodchipperListFile as WCFile

class WoodchipperGignoreHandler(WCHandler):
    def __init__(self, request, response):
        WCHandler.__init__(self, request, response)
        self.target = request.target
        self.path = Path(getcwd()) / gig_file_name
        self.file = WCFile(self.path)
        self.file.read()
        self.nodes = []

    def compile_node(self, name, status):
        return self.nodes.append({ RESPONSE.KEY.NAME: name, RESPONSE.KEY.STATUS: status })

    def add_node(self, name):
            if not name in self.file:
                self.file.add(name)
                self.compile_node(name, RESPONSE.STATUS.ADDED)
                return True
            else:
                self.compile_node(name, RESPONSE.STATUS.EXISTS)
                return False

    def remove_node(self, name):
            if not name in self.file:
                self.compile_node(name, RESPONSE.STATUS.MISSING)
                return False
            else:
                self.file.remove(name)
                self.compile_node(name, RESPONSE.STATUS.REMOVED)
                return True

    def remove_similar_nodes(self, name):
        matching = []
        token = name.split('*')[0]
        for node in self.file:
            if node.startswith(token):
                matching.append(node)
        for node in matching:
            self.remove_node(node)
        return len(matching)

    def save(self):
        if not self.debug:
            self.file.write()

    def compile_nodes(self, success=True):
        self.save()
        self.log_kvp("nodes", self.nodes)
        if success:
            self.log_success()


class WoodchipperGignoreHandlerShow(WoodchipperGignoreHandler):
    def handle(self):
        if len(self.file.text) == 0:
            self.log_error(ERROR.FILE_IS_EMPTY)
            return
        for rawLine in self.file.text:
            line = rawLine.strip()
            if not line.startswith('#') and len(line) > 0:
                self.compile_node(line, RESPONSE.STATUS.EXISTS)
        self.compile_nodes()

class WoodchipperGignoreHandlerAdd(WoodchipperGignoreHandler):
    def handle(self):
        for node in self.target:
            self.add_node(node)
        self.compile_nodes()

class WoodchipperGignoreHandlerSetup(WoodchipperGignoreHandler):
    def handle(self):
        targets = setup_nodes["default"]
        for target in self.target:
            setup_type = target.lower()
            if setup_type in setup_nodes:
                targets = targets + setup_nodes[setup_type]
        for node in targets:
            self.add_node(node)
        self.compile_nodes()

class WoodchipperGignoreHandlerRemove(WoodchipperGignoreHandler):
    def handle(self):
        for node in self.target:
            if '*' in node:
                self.remove_similar_nodes(node)
            else:
                self.remove_node(node)
        self.compile_nodes()

class WoodchipperGignoreHandlerClear(WoodchipperGignoreHandler):
    def handle(self):
        self.file.clear()
        self.compile_nodes()