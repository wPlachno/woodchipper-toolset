from difflib import *

from utilities.wcutil import WoodChipperFile as WCFile

class COLOR:

    RED='\033[0;31m'
    GREY='\033[90m'
    YELLOW='\033[93m'
    BLUE='\033[94m'
    DARK_YELLOW='\033[0;33m'
    GREEN='\033[0;32m'
    DARK_GREEN='\033[2;32m'
    PURPLE='\033[0;35m'
    BLACK='\033[0;30m'
    WHITE='\033[37m'
    DEFAULT='\033[0m'

PROFILE= {
    '+': COLOR.GREEN,
    '*': COLOR.GREEN,
    '-': COLOR.RED,
    ' ': COLOR.GREY,
    '#': COLOR.PURPLE,
    'default': COLOR.YELLOW
}

class DiffColor:
    def __init__(self, use_context=True):
        default = DiffColor._diff_colorizer
        if use_context:
            default = self._context_colorizer
            self.current_file_color = COLOR.GREEN
        self.formatters = { 'default': [ default ]}

    def register_formatter(self, string_transform_function, file_ext='default'):
        previous_list = []
        if file_ext in self.formatters.keys:
            previous_list = self.formatters[file_ext]
        previous_list.append(string_transform_function)
        self.formatters[file_ext] = previous_list

    def format_line(self, text_line, file_ext='default'):
        line = text_line[:]
        formatters = self.formatters.get(file_ext, self.formatters['default'])
        for formatter in formatters:
            line = formatter(line)
        return line

    def _context_colorizer(self, line):
        color = COLOR.GREY
        if line.startswith('*** '):
            color = COLOR.GREEN
            self.current_file_color = color
        elif line.startswith('--- '):
            color = COLOR.RED
            self.current_file_color = color
        elif line.startswith('****'):
            color = COLOR.PURPLE
        elif line.startswith('!'):
            color = f"{self.current_file_color}!{COLOR.YELLOW}"
            line = line[1:]
        elif line.startswith('+'):
            color = COLOR.GREEN
        elif line.startswith('-'):
            color = COLOR.RED
        return f"{color}{line}{COLOR.DEFAULT}\n"

    @staticmethod
    def _diff_colorizer(line):
        color = PROFILE[line[0]] if line[0] in PROFILE.keys() else PROFILE['default']
        return f"{color}{line}{COLOR.DEFAULT}\n"




def get_diff_from_file_paths(previous_file_path, next_file_path, cli_colorize=False):
    prev_file = WCFile(previous_file_path)
    prev_file.read()
    next_file = WCFile(next_file_path)
    next_file.read()
    diff_lines = list(context_diff(prev_file.text, next_file.text, lineterm=''))
    has_changes = check_diff_for_changes(diff_lines)
    # diff_lines = reformat_diff_lines(diff_lines)
    if cli_colorize:
        diff_lines = colorize_diff_for_terminal(diff_lines, previous_file_path.split('.')[-1])
    return has_changes, diff_lines

def check_diff_for_changes(diff_lines):
    for line in diff_lines:
        if line.startswith('!'):
            return True
    return False

def reformat_diff_lines(diff_lines):
    new_lines = []
    current_index = 2
    current_diff = 0
    return new_lines

def colorize_diff_for_terminal(diff_list, file_ext="txt", use_context=True, keep_context_header=False):
    colorizer = DiffColor(use_context)
    colorized_diff = []
    prepped_list = _prep_lines_for_terminal(diff_list, keep_context_header)
    for line in prepped_list:
        colorized_line = colorizer.format_line(line, file_ext)
        colorized_diff.append(colorized_line)
    return colorized_diff

def _prep_lines_for_terminal(diff_lines, keep_context_header=False):
    new_lines = []
    header_line_count = 0 if keep_context_header else 2
    for line in diff_lines:
        prepped_line = line #.strip()
        if prepped_line.endswith('\n'):
            prepped_line = prepped_line[:-1]
        if header_line_count == 0:
            if len(prepped_line) > 0:
                new_lines.append(prepped_line)
        else:
            header_line_count -= 1
    return new_lines

def _format_line_identifier(line):
    if line.startswith("*** ") and line.endswith(" ****"):
        line_indices = line[4:-5].split(',')

        