# wcn_parser.py
# Written by: Will Plachno
# Created: 01/04/2025
# Version: 0.0.1.002
# Last Changed: 01/08/2025

from utilities.wcparser import CLParser as WCParser
from constants import MODE, SECTION

def build_parser():
    parser = WCParser("wcn",
                      version="0.0.2.000",
                      description="A system for taking notes in the terminal that are localized to the working directory.",
                      footer="Created by Will Plachno. Copyright 2024.")
    parser.add_argument("mode", choices=[MODE.SHOW, MODE.ADD, MODE.REMOVE, MODE.MOVE, MODE.UPDATE, MODE.REPLACE, MODE.CLEAR], default=MODE.DEFAULT,
                        description="The mode we are operating in.\n  show - Lists notes\n  add - Adds a note\n  remove - Removes a note\n  move - Moves a note from one index to another\n  update - Changes a notes text\n  replace - Replaces a note completely\n  clear - Removes all notes")
    parser.add_argument("target", nargs="+",
                        description="The targets needed to complete the script. Highly dependent on the mode, but could consist of a quoted string (when creating, updating, or replacing notes) or one or more note indices (when moving, removing, updating, or replacing notes). Note that the proper order would be source_index, destination_index, text.")
    parser.add_argument("section", choices=[SECTION.CORE, SECTION.LOCAL, SECTION.ALL], default=SECTION.ALL,
                        description="The notes are either stored in a user-wide 'Core' file or a 'Local' file in the working directory. The 'section' argument determines whether the script execution should pay attention to only the core (-c), only the local (-l), or both (-a) files.")
    return parser

def post_parser(raw_request):
    request = raw_request
    if request.mode == MODE.DEFAULT:
        if len(request.target) == 0:
            request.mode = MODE.SHOW
        else:
            request.mode = MODE.ADD
    setattr(request, "lib", SECTION.TO_LIB[request.section])
    return request