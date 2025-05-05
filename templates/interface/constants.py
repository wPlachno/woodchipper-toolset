from utilities import wcconstants as S
from utilities.wcconstants import COLOR_DEFAULT


# Our application uses WoodchipperNamespaces for data transfer
# between the CLI and the Controller. These constants represent
# the keys added to the request (CLI->Cntl) and results (Cntl->CLI)
# namespaces.
class KEY:
    class REQUEST:
        MODE = "mode"
        DEBUG = "debug"
        PATH = "path"
        DATA = "data"

    class RESULTS:
        SUCCESS = "success"
        ERROR = "error"
        DEBUG = "debug"
        FILES = "files"
        CONTROL = "control"
        EXPANDER = "expander"

    class FILE:
        NAME = "name"
        PATH = "path"
        CONTENT = "content"

# MODE represents the operation represented in the request passed to the Controller
class MODE:
    NONE = "none"
    TEST = "test"
    NORMAL = "normal"


# In this implementation of the CLI, we associate certain colors with certain constructs.
# Note that this is based off of the profile colors presented by the wcutil construct
class COLOR:
    NAME = S.COLOR_SUPER
    PATH = S.COLOR_SIBLING
    CONTENT = S.COLOR_OPTION
    SUCCESS = S.COLOR_GREEN
    ERROR = S.COLOR_RED
    WARNING = S.COLOR_DARK_YELLOW
    RESET = S.COLOR_DEFAULT


def clr(text, color):
    return color + text + COLOR_DEFAULT

class TAG: # .format() required

    class FILE:
        NAME = clr(S.OP0, COLOR.NAME)
        PATH = clr(S.OP1, COLOR.PATH)
        CONTENT = clr(S.OP2, COLOR.CONTENT)

    SUCCESS = clr("SUCCESS", COLOR.SUCCESS)
    FAILURE = clr("FAILURE", COLOR.ERROR)
    ERROR = clr("ERROR:", COLOR.ERROR)

class ERROR:
    class NO_CONTROL_FILE:
        CODE = "786770"
        DESCRIPTION = [
                S.EMPTY,                        # V0: SILENT
                TAG.FAILURE,                    # V1: RESULTS_ONLY, either SUCCESS or FAILURE
                f"{TAG.ERROR} Please provide the path to a {clr("Control", COLOR.NAME)} file.",     # V2: Normal user
                f"{TAG.ERROR} No {clr("Control", COLOR.NAME)} file provided."]     # V3: DEBUG
    class WOULD_OVERWRITE_FILE:
        CODE = "877970"
        DESCRIPTION = [
                S.EMPTY,                        # V0: SILENT
                TAG.FAILURE,                    # V1: RESULTS_ONLY, either SUCCESS or FAILURE
                f"{TAG.ERROR} Would overwrite {clr(S.OP0, COLOR.NAME)} file. Use {clr('-f', COLOR.PATH)} to force the overwrite.",     # V2: Normal user
                f"{TAG.ERROR} Would overwrite {clr(S.OP0, COLOR.NAME)}."]     # V3: DEBUG
    class IMPROPER_TOKEN_SYNTAX:
        CODE = "738483"
        DESCRIPTION = [
                S.EMPTY,                        # V0: SILENT
                TAG.FAILURE,                    # V1: RESULTS_ONLY, either SUCCESS or FAILURE
                f"{TAG.ERROR} The file is formatted incorrectly. The tokens cannot be translated. Double check that for each '#{{}}{{{{', there exists a corresponding '}}}}' and no more.",     # V2: Normal user
                f"{TAG.ERROR} Incorrect token syntax with the control file."]     # V3: DEBUG

    CODE = {
        "786770": NO_CONTROL_FILE.DESCRIPTION,
        "877970": WOULD_OVERWRITE_FILE.DESCRIPTION
    }

class OUT:
    ERROR = clr("ERROR: ", COLOR.ERROR)+S.OP0+S.NL
    class FILE:
            NO_FILES = "No "+clr("files", COLOR.NAME)+S.EL
            LIST_ITEM = [
                S.EMPTY,                        # V0: SILENT
                S.OP0+S.CD,                     # V1: RESULTS_ONLY, will need to remove the last comma
                S.DH+TAG.FILE.NAME+S.NL,     # V2: NORMAL
                S.DH+TAG.FILE.PATH]     # V3: DEBUG