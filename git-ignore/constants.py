import utilities.wcconstants as S

class MODE:
    SETUP = "setup"
    SHOW = "show"
    ADD = "add"
    REMOVE = "remove"
    CLEAR = "clear"

class RESPONSE:
    class KEY:
        NAME = "name"
        STATUS = "status"
    class STATUS:
        ADDED = "added"
        EXISTS = "exists"
        REMOVED = "removed"
        MISSING = "missing"

STATUS_TEMPLATES = {
    "added": f"{S.clr("+ Added", S.COLOR.ACTIVE)}: {S.OP[0]}",
    "exists": f"{S.clr("= Exists", S.COLOR.SIBLING)}: {S.OP[0]}",
    "removed": f"{S.clr("- Removed", S.COLOR.CANCEL)}: {S.OP[0]}",
    "missing": f"{S.clr("! Missing", S.COLOR.SUB)}: {S.OP[0]}"
}

def NODE(name, status):
    return STATUS_TEMPLATES[status].format(name)

FILE_NAME_GIT_IGNORE = ".gitignore"

class CL_DESC:
    FILENAME = S.COLOR.SUPER+FILE_NAME_GIT_IGNORE+S.COLOUR.DEFAULT
    FILE_CONTAINS = FILENAME+" contains: "+S.KEY.NL
    NODE_LIST = " - "+S.COLOR.SIBLING+"{0}"+S.COLOUR.DEFAULT+S.KEY.NL
    FILE_HAS_BEEN_CLEARED = FILENAME+" has been cleared."+S.KEY.NL
    NODE_ADDED = " - "+S.COLOR.SIBLING+"{0}"+S.COLOUR.DEFAULT+" has been added to " +FILENAME+S.KEY.NL
    NODE_REMOVED = " - "+S.COLOR.SIBLING+"{0}"+S.COLOUR.DEFAULT+" has been removed from " +FILENAME+S.KEY.NL
    NODE_DOES_NOT_EXIST = " - "+S.COLOR.SIBLING+"{0}"+S.COLOUR.DEFAULT+" was not found in " +FILENAME+S.KEY.NL

class ERROR:
    FILE_DOES_NOT_EXIST = CL_DESC.FILENAME+" does not exist."+S.KEY.NL
    FILE_IS_EMPTY = CL_DESC.FILENAME+" is empty."+S.KEY.NL

FLAG_SETUP = "-s"
FLAG_CLEAR = "-c"
FLAG_ADD = "-a"
FLAG_PYTHON = "Python"
FLAG_REMOVE = "-r"
FLAG_DEBUG = "-debug"
FLAG_VERBOSE = "-verbose"
FLAG_CONFIG = "-config"
FLAG_HELP = "-help"

CL_DESC_HELP = (S.KEY.NL+S.COLOR.SIBLING+"Welcome to "+S.COLOR.SUPER+"gignore.py"+S.COLOR.SIBLING+"!"+S.KEY.NL+S.KEY.NL+
                S.COLOUR.DEFAULT+"This script is designed to allow command-line edits of "+
                S.COLOR.SUPER+".gitignore"+S.COLOUR.DEFAULT+" files."+S.KEY.NL+S.KEY.NL+
                S.COLOR.SUB+"It is highly suggested to alias this script as "+
                S.COLOR.SUBSIB+"gignore"+S.COLOUR.DEFAULT+" or "+S.COLOR.SUBSIB+"gig."+S.COLOUR.DEFAULT+S.KEY.NL+S.KEY.NL+
                "Usage: "+S.KEY.NL+
                S.COLOR.QUOTE+"gignore"+S.COLOUR.DEFAULT+": Lists all nodes in your "+CL_DESC.FILENAME+" file."+S.KEY.NL+
                S.COLOR.QUOTE+"gignore -a \"[NODE]\""+S.COLOUR.DEFAULT+": Adds the given node to your "+CL_DESC.FILENAME+" file."+S.KEY.NL+
                S.COLOR.QUOTE+"gignore -r \"[NODE]\""+S.COLOUR.DEFAULT+": Removes the given node from your "+CL_DESC.FILENAME+" file."+S.KEY.NL+
                S.COLOR.QUOTE+"gignore -s \"[LANG]\""+S.COLOUR.DEFAULT+": Sets up your "+CL_DESC.FILENAME+" file and populates it with the standard nodes of the given language. If the language cannot be deciphered or is a language currently not supported, the .gitignore file will be created and populated oS.KEY.NLy with the \".wcn*\" node."+S.KEY.NL+
                S.COLOR.QUOTE+"gignore -c"+S.COLOUR.DEFAULT+": Removes all nodes from your "+CL_DESC.FILENAME+" file."+S.KEY.NL+S.KEY.NL+
                "Currently supported setup packages: "+S.KEY.NL+
                "- "+S.COLOR.SIBLING+"Python"+S.COLOUR.DEFAULT+S.KEY.NL+S.KEY.NL+
                "If you have any suggestions, feel free to send an email to the developer, Will, at "+S.COLOR.SUPER+"wjplachno@gmail.com"+S.COLOUR.DEFAULT+S.KEY.NL)




RESULT_SUCCESS = True
RESULT_FAILURE = False

DISPLAY_COMMAND = "display_command"
TAG_ON = "on"
TAG_OFF = "off"

OOB = -1