# wcn_colorStack.py
# Written by: Will Plachno
# Created: 09/22/2025
# Version: 0.0.1.001
# Last Changed: 09/22/2025

from constants import CLR_ARRAY

class ColorStack:
    def __init__(self):
        self.max = len(CLR_ARRAY)
        self.current = 0
        self.stack = dict()

    def check(self, key):
        if key in self.stack:
            return self.stack[key]
        else:
            target = CLR_ARRAY[self.current]
            nextIdx = self.current+1
            if nextIdx == self.max:
                nextIdx = 0
            self.current = nextIdx
            self.stack[key] = target
            return target
