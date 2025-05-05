
"""
The control stack represents a stack of WCFiles, used to keep track of which tokens are currently active, as well as which files the current content is associated with.
"""
class WoodchipperTemplateControlStack:
    def __init__(self, control_file):
        self.control = control_file
        self.stack = [self.control]

    def push(self, token_file):
        self.stack.append(token_file)

    def pop(self):
        return self.stack.pop()

    def write(self, text):
        self.stack[-1].add(text)
