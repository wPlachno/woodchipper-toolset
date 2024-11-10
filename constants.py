import wcconstants as S
from wcconstants import COLOR_DEFAULT, EMPTY

TAG_VERSION = "Version:"

# When the Controller operates in debug mode, it uses
# a different archive file.
class FILE_NAME:
    ARCHIVE = ".wctkArchive.txt"
    DEBUG = ".wctkArchive_debug.txt"

# Our application uses WoodchipperNamespaces for data transfer
# between the CLI and the Controller. These constants represent
# the keys added to the request (CLI->Cntl) and results (Cntl->CLI)
# namespaces.
class KEY:
    class REQUEST:
        MODE = "mode"
        DEBUG = "debug"
        TARGET = "target"
        PATH = "path"
        DATA = "data"

    class RESULTS:
        HANDLER = "handler"
        SUCCESS = "success"
        ERROR = "error"
        TOOLKITS = "toolkits"
        TOOLKIT = "toolkit"
        CLONES = "clones"
        CLONE = "clone"

    class TOOLKIT:
        NAME = "name"
        PATH = "path"
        VERSION = "version"
        STATE = "state"
        CLONES = "clones"
        OLD_VERSION = "old_version"

    class CLONE:
        NAME = "name"
        PATH = "path"
        VERSION = "version"
        STATE = "state"
        EXISTED = "existed"
        DIFF = "diff"
        REPLACED = "replaced"
        OLD_VERSION = "old_version"
        ERROR = "error"

# The HANDLER constants represent the different operations permissable by the Controller
# HANDLER.GENERIC will only appear during error states.
class HANDLER:
    GENERIC = "generic"
    class SHOW:
        ALL = "show.all"
        TOOLKIT = "show.toolkit"
        CLONE = "show.clone"

    class ADD:
        TOOLKIT = "add.toolkit"
        CLONE = "add.clone"

    class PUSH:
        TOOLKIT = "push.toolkit"
        CLONE = "push.clone"

    class GRAB:
        TOOLKIT = "grab.toolkit"
        CLONE = "grab.clone"

# MODE represents the operation represented in the request passed to the Controller
class MODE:
    NONE = "none"
    TEST = "test"
    ADD = "add"
    GRAB = "grab"
    PUSH = "push"
    SHOW = "show"
    MODES = ["show", "add", "grab", "push"]

# Flags are the command line flags permissible for the CLI of wctk.
# DEPRECATED: This was in use before we switched over to using the
# argparse library (which was subsequently replaced by wcparser.py
# when the number of optional arguments led to parsing errors by
# the argparse library. )
class FLAG:
    ADD = "-a"
    CLONE = "-c"
    REMOVE = "-r"
    DELETE = "-d"
    PUSH = "-p"
    GRAB = "-g"
    FORCE = "-f"

class DELIMITER:
    TOOLKIT = "|"
    CLONE = "~"

class STATE:
    UNKNOWN = "unknown"
    BEHIND_CORE = "behind_core"
    UP_TO_DATE = "up_to_date"
    AFTER_CORE = "after_core"
    HAS_LOCAL_CHANGES = "has_local_changes"


# In this implementation of the CLI, we associate certain colors with certain constructs.
# Note that this is based off of the profile colors presented by the wcutil construct
class COLOR:
    TOOLKIT = S.COLOR_SUPER
    CLONE = S.COLOR_SIBLING
    VERSION = S.COLOR_OPTION
    STATE = S.COLOR_ACTIVE
    PATH = S.COLOR_SUB
    SUCCESS = S.COLOR_GREEN
    ERROR = S.COLOR_RED
    WARNING = S.COLOR_DARK_YELLOW
    RESET = S.COLOR_DEFAULT
    class STATE_VAL:
        UNKNOWN = '\x1b[1;30;41m'           # Black (Red BG)
        BEHIND_CORE = '\x1b[1;30;44m'       # Black (Blue BG)
        UP_TO_DATE = '\x1b[0;30;45m'        # Black (Purple BG)
        AFTER_CORE = '\x1b[6;30;42m'        # Black (Lime Green BG)
        HAS_LOCAL_CHANGES = '\x1b[1;30;43m' # Black (Yellow BG)


def clr(text, color):
    return color + text + COLOR_DEFAULT

def clr_state(state_value):
    state_color = COLOR.STATE_VAL.UNKNOWN
    match state_value:
        case STATE.UP_TO_DATE:
            state_color = COLOR.STATE_VAL.UP_TO_DATE
        case STATE.AFTER_CORE:
            state_color = COLOR.STATE_VAL.AFTER_CORE
        case STATE.HAS_LOCAL_CHANGES:
            state_color = COLOR.STATE_VAL.HAS_LOCAL_CHANGES
        case STATE.BEHIND_CORE:
            state_color = COLOR.STATE_VAL.BEHIND_CORE
    return clr(" "+state_value+" ", state_color)

class TAG: # .format() required

    class TOOLKIT: # All Describe a Toolkit
        NAME = clr(S.OP0, COLOR.TOOLKIT) # (NAME)
        ITEM = NAME+" ("+clr(S.OP1, COLOR.VERSION)+")" # (NAME, VERSION)
        STATE = ITEM+": "+clr(S.OP2, COLOR.STATE) # (NAME, VERSION, STATE)
        PATH = STATE+S.NL+clr(S.OP3, COLOR.PATH)+S.NL # (NAME, VERSION, STATE, PATH)

    class CLONE: # All Describe a Clone
        NAME = clr(S.OP0, COLOR.CLONE) # (NAME)
        ITEM = NAME+" ("+clr(S.OP1, COLOR.VERSION)+")" # (NAME, VERSION)
        STATE = ITEM+": "+clr(S.OP2, COLOR.STATE) # (NAME, VERSION, STATE)
        PATH = STATE+S.NL+clr(S.OP3, COLOR.PATH)+S.NL # (NAME, VERSION, STATE, PATH)
        IDENT = clr(S.OP0, COLOR.TOOLKIT)+"/"+clr(S.OP1, COLOR.CLONE) # (TOOLKIT_NAME, CLONE_NAME)

class ERROR:
    class COULD_NOT_RESOLVE:
        TOOLKIT = f"There exists no {clr("Toolkit", COLOR.TOOLKIT)} named '{S.OP0}'" # (target_toolkit)
        CLONE = f"There exists no {clr("Clone", COLOR.CLONE)} named '{S.OP0}' in toolkit {clr(S.OP1, COLOR.TOOLKIT)}." # (target_clone, target_toolkit)
    class ADD:
        class TOOLKIT:
            ALREADY_REGISTERED = f"{clr("Toolkit", COLOR.TOOLKIT)} '{S.OP0}' {clr("already exists", COLOR.ERROR)} at {clr(S.OP1, COLOR.PATH)}." # (toolkit.name, toolkit.path)
            IS_DIRECTORY = f"{clr("Toolkit", COLOR.TOOLKIT)} '{S.OP0}' cannot be registered because {clr(S.OP1, COLOR.PATH)} leads to a {clr("directory", COLOR.ERROR)}. Toolkits must consist of a specific file." # (toolkit.name, toolkit.path)
        class CLONE:
            INVALID_TOOLKIT = f"There exists no {clr("Toolkit", COLOR.TOOLKIT)} named '{S.OP0}'" # (target_toolkit)
            ALREADY_REGISTERED = f"{clr("Clone", COLOR.CLONE)} '{S.OP0}' {clr("already exists", COLOR.ERROR)} at {clr(S.OP1, COLOR.PATH)}." # (clone.name, clone.path)
            ALREADY_EXISTS = f"A file already exists at {clr(S.OP0, COLOR.PATH)}." # (Target_path)
    class SHOW:
        class TOOLKIT:
            INVALID_TOOLKIT = f"There exists no {clr("Toolkit", COLOR.TOOLKIT)} named '{S.OP0}'" # (target_toolkit)
        class CLONE:
            INVALID_TOOLKIT = f"There exists no {clr("Toolkit", COLOR.TOOLKIT)} named '{S.OP0}'" # (target_toolkit)
            INVALID_CLONE = f"There exists no {clr("Clone", COLOR.CLONE)} named '{S.OP0}'" # (target_clone)
            UNSUCCESSFUL_DIFF = f"An error occurred during the diffing process."
    class PUSH:
        class CLONE:
            TOOLKIT_NOT_PUSHABLE = f"The toolkit {clr(S.OP0, COLOR.TOOLKIT)} is not {clr_state(STATE.UP_TO_DATE)} and cannot be pushed." # (toolkit_name)
            UP_TO_DATE = f"{TAG.CLONE.IDENT} is already {clr_state(STATE.UP_TO_DATE)} and was skipped."

class OUT:
    ERROR = clr("ERROR: ", COLOR.ERROR)+S.OP0+S.NL
    class SHOW:
        class ALL:
            NO_TOOLKITS = "No registered "+clr("toolkits", COLOR.TOOLKIT)+S.EL
            HEADER = "Registered "+clr("toolkits", COLOR.TOOLKIT)+S.CS+S.OP0 # (NUM_TOOLKITS)
            LIST_ITEM = [
                S.EMPTY,                        # V0: SILENT
                S.OP0+S.CD,                     # V1: RESULTS_ONLY, will need to remove the last comma
                S.DH+TAG.TOOLKIT.STATE+S.NL,     # V2: NORMAL
                S.DH+TAG.TOOLKIT.PATH]     # V3: DEBUG
        class TOOLKIT:
            NO_CLONES = "No registered " + clr("clones", COLOR.CLONE)+"."
            HEADER = [
                S.EMPTY,                         # SILENT
                S.EMPTY,                         # RESULTS_ONLY
                f"{clr(S.OP0, COLOR.TOOLKIT)} ({clr(S.OP1, COLOR.VERSION)}): {clr(S.OP2, COLOR.STATE)}", # (tk.name, tk.version)
                f"{clr(S.OP0, COLOR.TOOLKIT)} ({clr(S.OP1, COLOR.VERSION)}): {clr(S.OP2, COLOR.STATE)}\n{clr(S.OP3, COLOR.PATH)}" ] #(tk.name, tk.version, tk.path) ]
            LIST_ITEM = [
                S.EMPTY,
                S.OP0+S.CD,
                S.DH+TAG.CLONE.STATE+S.NL,
                S.DH+TAG.CLONE.PATH ]
        class CLONE:
            NO_CHANGES = "No registered " + clr("changes", COLOR.CLONE)+"."
            DESCRIPTION = [
                S.EMPTY,                         # SILENT
                S.EMPTY,                         # RESULTS_ONLY
                f"{TAG.CLONE.IDENT} ({clr(S.OP2, COLOR.VERSION)}): {clr(S.OP3, COLOR.STATE)}", # (tk.name, cl.name, cl.version, cl.state)
                f"{TAG.CLONE.IDENT} ({clr(S.OP2, COLOR.VERSION)}): {clr(S.OP3, COLOR.STATE)}\n{clr(S.OP4, COLOR.PATH)}" ] #  (tk.name, cl.name, cl.version, cl.state, cl.path)
            DIFF_HEADER = [
                S.EMPTY, S.EMPTY,
                f"{clr('(*)', S.COLOR_GREEN)}{clr(S.OP0, COLOR.TOOLKIT)} -> {clr('(-)', S.COLOR_RED)}{clr(S.OP0, COLOR.TOOLKIT)}/{clr(S.OP1, COLOR.CLONE)}", #tk.name, cl.name
                f"{clr('(*)', S.COLOR_GREEN)}{clr(S.OP0, COLOR.TOOLKIT)}{clr(S.OP2, COLOR.PATH)}\n{clr('(-)', S.COLOR_RED)}{clr(S.OP0, COLOR.TOOLKIT)}/{clr(S.OP1, COLOR.CLONE)}{clr(S.OP3, COLOR.PATH)}" ] # tk.name, cl.name, tk.path, cl.path
    class ADD:
        TOOLKIT = [
            None, clr("SUCCESS", COLOR.SUCCESS),
            f"{clr("REGISTERED", COLOR.SUCCESS)}: {clr(S.OP0, COLOR.TOOLKIT)}",
            f"{clr("REGISTERED", COLOR.SUCCESS)}: {clr(S.OP0, COLOR.TOOLKIT)} at {clr(S.OP1, COLOR.PATH)}."]
        class CLONE:
            REGISTERED = [
                None, clr("SUCCESS", COLOR.SUCCESS),
                f"{clr("REGISTERED", COLOR.SUCCESS)}: {TAG.CLONE.IDENT}",
                f"{clr("REGISTERED", COLOR.SUCCESS)}: {TAG.CLONE.IDENT} at {clr(S.OP2, COLOR.PATH)}."] # (TK.name, Clone.name, Clone.path)
            DUPLICATED = [
                None, clr("SUCCESS", COLOR.SUCCESS),
                f"{clr("REGISTERED", COLOR.SUCCESS)}: {TAG.CLONE.IDENT}",
                f"{clr("REGISTERED", COLOR.SUCCESS)}: {TAG.CLONE.IDENT} /n{clr(S.OP2, COLOR.PATH)} copied from {clr(S.OP3, COLOR.PATH)}."] # (TK.name, Clone.name, Clone.path)
    class PUSH:
        class TOOLKIT:
            HEADER = [ # tk.name, tk.path
                None, clr("SUCCESS", COLOR.SUCCESS),
                f"{clr("PUSHED", COLOR.SUCCESS)}: {clr(S.OP0, COLOR.TOOLKIT)}",
                f"{clr("PUSHED", COLOR.SUCCESS)}: {clr(S.OP0, COLOR.TOOLKIT)} from {clr(S.OP1, COLOR.PATH)}."]
            class ITEM:
                SUCCESS = [ # (clone_name, clone_path)
                    None, None,
                    f"{S.DH}{clr(S.OP0, COLOR.CLONE)}: {clr("REPLACED",COLOR.SUCCESS)}", # (clone_name)
                    f"{S.DH}{clr(S.OP0, COLOR.CLONE)}: {clr("REPLACED",COLOR.SUCCESS)} at {clr(S.OP1, COLOR.PATH)}"] # (clone_name, clone_path)
                FAILED = [ # clone_name, clone_path, clone_error
                    None, None,
                    f"{S.DH}{clr(S.OP0, COLOR.CLONE)}: {clr("SKIPPED",COLOR.WARNING)}\n{S.OP2}", # (clone_name)
                    f"{S.DH}{clr(S.OP0, COLOR.CLONE)}: {clr("SKIPPED",COLOR.WARNING)} at {clr(S.OP1, COLOR.PATH)}\n{S.OP2}"] # (clone_name, clone_path, clone_error)
        class CLONE:
            SUCCESS = [ # (clone_name, clone_path)
                None, f"{clr("SUCCESS",COLOR.SUCCESS)}",
                f"{clr(S.OP0, COLOR.CLONE)}: {clr("SUCCESS",COLOR.SUCCESS)}", # (clone_name)
                f"{clr(S.OP0, COLOR.CLONE)}: {clr("SUCCESS",COLOR.SUCCESS)} at {clr(S.OP1, COLOR.PATH)}"] # (clone_name, clone_path)
            FAILED = [ # (clone_name, clone_path, clone_error)
                None, f"{clr("SKIPPED",COLOR.WARNING)}",
                f"{clr(S.OP0, COLOR.CLONE)}: {clr("SKIPPED",COLOR.WARNING)}\n{S.OP2}", # (clone_name)
                f"{clr(S.OP0, COLOR.CLONE)}: {clr("SKIPPED",COLOR.WARNING)} at {clr(S.OP1, COLOR.PATH)}\n{S.OP2}"] # (clone_name, clone_path, clone_error)

class DEPRECATED_OUT: # Command-line output, .format() required for SOME
    class LIST:
        class TOOLKITS:
            HEADER = "Registered "+COLOR.TOOLKIT+"toolkits"+COLOR.RESET+S.CS+S.OP0+S.NL # (NUM_TOOLKITS)
            ITEM = S.DH+TAG.TOOLKIT.ITEM+S.NL # (TOOLKIT_NAME, TOOLKIT_VERSION)
            EMPTY = S.COLOR_CANCEL+"No registered "+COLOR.TOOLKIT+"toolkits"+COLOR.RESET+S.EL
        class CLONES:
            HEADER = TAG.TOOLKIT.PATH # (TOOLKIT_NAME, TOOLKIT_VERSION, TOOLKIT_STATE, TOOLKIT_PATH)
            ITEM = S.DH+TAG.CLONE.STATE+S.NL # (CLONE_NAME, CLONE_VERSION, CLONE_STATE)


OUT_TAG_NAME = S.COLOR_SIBLING+S.OP0+S.COLOR_DEFAULT
OUT_TAG_ITEM = OUT_TAG_NAME+S.CS+S.COLOR_OPTION+S.OP1+S.COLOR_DEFAULT #   '[NAME]: [VERSION]'
OUT_TAG_STATE_ITEM = OUT_TAG_ITEM+" ("+S.COLOR_SUPER+S.OP2+S.COLOR_DEFAULT+")"
OUT_HEADER_ITEM = OUT_TAG_STATE_ITEM+S.NL+S.OP3+S.NL #   '[NAME]: [VERSION] ([STATE])\n[PATH]\n'
OUT_LIST_ITEM = "- "+OUT_TAG_STATE_ITEM+S.NL      # '- [NAME]: [VERSION] ([STATE])\n'

class COMPARE:
    LESSER_THAN = -1
    EQUAL_TO = 0
    GREATER_THAN = 1

OUT_ADDED_TOOLKIT = "Added new toolkit "+TAG.TOOLKIT.NAME+S.EL
OUT_ADDED_CLONE = "Added new clone "+TAG.CLONE.IDENT+" at path "+COLOR.PATH+S.OP2+COLOR.RESET+S.EL
OUT_UPDATED_CLONE = "Successfully updated clone "+TAG.CLONE.IDENT+S.EL
OUT_CLONE_HAS_LOCAL = TAG.CLONE.IDENT+" has local changes"+S.EL
OUT_CLONE_UP_TO_DATE = TAG.CLONE.IDENT+" is up to date"+S.EL
OUT_GRABBED_CLONE = "Grabbed "+TAG.CLONE.IDENT+S.EL

OUT_CANT_RESOLVE_TOOLKIT = "'"+TAG.TOOLKIT.NAME+"' could "+S.COLOR_CANCEL+"not"+S.COLOR_DEFAULT+" be resolved to a toolkit"+S.EL
OUT_CANT_RESOLVE_CLONE = "'"+TAG.CLONE.IDENT+"' could "+S.COLOR_CANCEL+"not"+COLOR.RESET+" be resolved to a clone"+S.EL



