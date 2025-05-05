# constants.py
# Written by: Will Plachno
# Created: 08/22/24
# Version: 0.0.2.001
# Last Changed: 01/08/2025

from utilities.wcconstants import COLOR, clr, OP

class MODE:
    DEFAULT="default"
    SHOW="show"
    ADD="add"
    REMOVE="remove"
    MOVE="move"
    UPDATE="update"
    REPLACE="replace"
    CLEAR="clear"

class SECTION:
    CORE="-c"
    LOCAL="-l"
    ALL="-a"
    FROM_LIB={"C":"-c", "L":"-l", "A":"-a"}
    TO_LIB={"-c":"C", "-l":"L", "-a":"A"}

class LIB:
    CORE="C"
    LOCAL="L"
    ALL="A"
    ERROR="E"

class FILE_NAME:
    CORE = ".wcn_Core.txt"
    LOCAL = ".wcn_Local.txt"
    DEBUG = ".wcn_Debug.txt"

class RESPONSE:
    CORE_PATH = "core_path"
    LOCAL_PATH = "local_path"
    LIB = "lib"
    NOTES = "notes"
    class NOTE:
        INDEX = "index"
        TIME = "timestamp"
        TEXT = "text"
        LIB = "library"

class MODS:
    NONE = "none"
    ADDED = "added"
    REMOVED = "removed"
    MOVED = "moved"
    UPDATED = "updated"
    REPLACED = "replaced"

class NOTES:
    CORE  = f"{OP[0]}: {clr("C", COLOR.SUPER)  } {clr(OP[1], COLOR.SUB)} - {OP[2]}" # Index, Timestamp, Text
    LOCAL = f"{OP[0]}: {clr("L", COLOR.SIBLING)} {clr(OP[1], COLOR.SUB)} - {OP[2]}" # Index, Timestamp, Text

HEADERS = {
    "show": f"{clr("Notes", COLOR.ACTIVE)}: ",
    "add": f"{clr("Added", COLOR.ACTIVE)}: ",
    "remove": f"{clr("Removed", COLOR.ACTIVE)}: ",
    "move": f"{clr("Moved", COLOR.ACTIVE)}: ",
    "update": f"{clr("Updated", COLOR.ACTIVE)}: ",
    "replace": f"{clr("Replaced", COLOR.ACTIVE)}: ",
    "clear": f"{clr("Cleared", COLOR.ACTIVE)}: "
}

CLR_ARRAY = [ '\033[0;32m', '\033[94m', '\033[93m', '\033[2;32m', '\033[0;31m', '\033[0;33m']

EMPTY=""
NL="\n"
BS="\\"

COLOR_RED='\033[0;31m'
COLOR_GREY='\033[90m'
COLOR_YELLOW='\033[93m'
COLOR_DARK_YELLOW='\033[0;33m'
COLOR_GREEN='\033[0;32m'
COLOR_PURPLE='\033[0;35m'
COLOR_BLACK='\033[0;30m'
COLOR_WHITE='\033[37m'
COLOR_DEFAULT='\033[0m'

COLOR_SUPER=COLOR_PURPLE
COLOR_SUB=COLOR_GREY
COLOR_SIBLING=COLOR_DARK_YELLOW
COLOR_ACTIVE=COLOR_GREEN
COLOR_CANCEL=COLOR_RED


CL_DESC_SUCCESS = COLOR_ACTIVE+"Success"+COLOR_DEFAULT
CL_DESC_FAILURE = COLOR_CANCEL+"Failure"+COLOR_DEFAULT

CL_DESC_FRAME_CORE = "{0}: " + COLOR_SUPER + "C" + COLOR_DEFAULT + " {1}" + NL
CL_DESC_FRAME_LOCAL = "{0}: " + COLOR_SIBLING + "L" + COLOR_DEFAULT + " {1}" + NL

CL_DESC_TASK = COLOR_SUPER+"Task"+COLOR_DEFAULT+": "
CL_DESC_UNIMPLEMENTED = " ["+COLOR_CANCEL+"UNIMPLEMENTED"+COLOR_DEFAULT+"]"
CL_DESC_CORE = COLOR_SUPER+"C"+COLOR_DEFAULT+": {0}"+NL
CL_DESC_LOCAL = COLOR_SIBLING+"L"+COLOR_DEFAULT+": {0}"+NL
CL_DESC_ACTIVE = COLOR_ACTIVE+"Active"+COLOR_DEFAULT
CL_DESC_INACTIVE = COLOR_CANCEL+"Inactive"+COLOR_DEFAULT
CL_DESC_NO_NOTES = "No notes found."+NL

CL_DESC_ATTRIBUTE = COLOR_SIBLING+"{0}"+COLOR_DEFAULT+": {1}"+NL
CL_DESC_TEXT = COLOR_SIBLING+"Text"+COLOR_DEFAULT+": {0}"+NL
CL_DESC_INDEX = COLOR_SIBLING+"Index"+COLOR_DEFAULT+": {1}"+NL
CL_DESC_DEL_INDEX = COLOR_SIBLING+"Index"+COLOR_DEFAULT+": {0}"+NL
CL_DESC_TARGET = COLOR_SIBLING+"Target"+COLOR_DEFAULT+": {0}"+NL
CL_DESC_DESTINATION = COLOR_SIBLING+"Destination"+COLOR_DEFAULT+": {1}"+NL

CL_DESC_LIST_ALL = CL_DESC_TASK+"List all notes."+NL
CL_DESC_LIST_CORE = CL_DESC_TASK+"List Core notes."+NL
CL_DESC_LIST_LOCAL = CL_DESC_TASK+"List Local notes."+NL
CL_DESC_APPEND_CORE = CL_DESC_TASK+"Append new note to Core."+NL+CL_DESC_TEXT
CL_DESC_APPEND_LOCAL = CL_DESC_TASK+"Append new note to Local."+NL+CL_DESC_TEXT
CL_DESC_EDIT_MAJOR = CL_DESC_TASK+"Edit text and time of note."+NL+CL_DESC_TEXT+CL_DESC_INDEX
CL_DESC_EDIT_MINOR = CL_DESC_TASK+"Edit text only of note."+NL+CL_DESC_TEXT+CL_DESC_INDEX
CL_DESC_PROMOTE = CL_DESC_TASK+"Promote a note to the other file."+NL+CL_DESC_TARGET
CL_DESC_MOVE = CL_DESC_TASK+"Move a note from target index to destination index."+NL+CL_DESC_TARGET+CL_DESC_DESTINATION
CL_DESC_DELETE_SINGLE = CL_DESC_TASK+"Delete a single note."+NL+CL_DESC_DEL_INDEX
CL_DESC_DELETE_ALL = CL_DESC_TASK+"Delete all notes."+NL
CL_DESC_DELETE_CORE = CL_DESC_TASK+"Delete all notes in Core."+NL
CL_DESC_DELETE_LOCAL = CL_DESC_TASK+"Delete all notes in Local."+NL
CL_DESC_DEBUG_TASK = CL_DESC_TASK+"Set debug."+NL
CL_DESC_CONFIG = CL_DESC_TASK+COLOR_SUB+"Config"+COLOR_DEFAULT+" - "+COLOR_SIBLING+"{0}"+COLOR_DEFAULT+": {1}"+NL
CL_DESC_DELETED_NODE = "- "+COLOR_CANCEL+"Deleted"+COLOR_DEFAULT+" node: \"{0}\""+NL

TIME_READABLE = "%m/%d/%Y, %H:%M:%S"
TIME_EPOCH = "%s"

NOTE_DELIMITER = "`~`"
OOB = -1