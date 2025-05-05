from utilities import wcconstants as S

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
        TARGET = "target"
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

    class TARGET:
        ALL = "all"
        TOOLKIT = "toolkit"
        CLONE = "clone"

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
    TOOLKIT = S.COLOR.SUPER
    CLONE   = S.COLOR.SIBLING
    VERSION = S.COLOR.OPTION
    STATE   = S.COLOR.ACTIVE
    PATH    = S.COLOR.SUB
    SUCCESS = S.COLOUR.GREEN
    ERROR   = S.COLOUR.RED
    WARNING = S.COLOUR.DARK_YELLOW
    RESET   = S.COLOUR.DEFAULT

    class STATE_VAL:
        UNKNOWN = '\x1b[1;30;41m'           # Black (Red BG)
        BEHIND_CORE = '\x1b[1;30;44m'       # Black (Blue BG)
        UP_TO_DATE = '\x1b[0;30;45m'        # Black (Purple BG)
        AFTER_CORE = '\x1b[6;30;42m'        # Black (Lime Green BG)
        HAS_LOCAL_CHANGES = '\x1b[1;30;43m' # Black (Yellow BG)

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
    return S.clr(" "+state_value+" ", state_color)

class TAG: # .format() required

    class TOOLKIT: # All Describe a Toolkit
        NAME = S.clr(S.OP[0], COLOR.TOOLKIT) # (NAME)
        ITEM = NAME+" ("+S.clr(S.OP[1], COLOR.VERSION)+")" # (NAME, VERSION)
        STATE = ITEM+": "+S.clr(S.OP[2], COLOR.STATE) # (NAME, VERSION, STATE)
        PATH = STATE+S.KEY.NL+S.clr(S.OP[3], COLOR.PATH)+S.KEY.NL # (NAME, VERSION, STATE, PATH)

    class CLONE: # All Describe a Clone
        NAME = S.clr(S.OP[0], COLOR.CLONE) # (NAME)
        ITEM = NAME+" ("+S.clr(S.OP[1], COLOR.VERSION)+")" # (NAME, VERSION)
        STATE = ITEM+": "+S.clr(S.OP[2], COLOR.STATE) # (NAME, VERSION, STATE)
        PATH = STATE+S.KEY.NL+S.clr(S.OP[3], COLOR.PATH)+S.KEY.NL # (NAME, VERSION, STATE, PATH)
        IDENT = S.clr(S.OP[0], COLOR.TOOLKIT)+"/"+S.clr(S.OP[1], COLOR.CLONE) # (TOOLKIT_NAME, CLONE_NAME)

class ERROR:
    class COULD_NOT_RESOLVE:
        TOOLKIT = f"There exists no {S.clr("Toolkit", COLOR.TOOLKIT)} named '{S.OP[0]}'." # (target_toolkit)
        CLONE = f"There exists no clone '{S.clr(S.OP[0], COLOR.CLONE)}' in toolkit {S.clr(S.OP[1], COLOR.TOOLKIT)}." # (target_clone, target_toolkit)
    class ADD:
        class TOOLKIT:
            ALREADY_REGISTERED = f"{S.clr("Toolkit", COLOR.TOOLKIT)} '{S.OP[0]}' {S.clr("already exists", COLOR.ERROR)} at {S.clr(S.OP[1], COLOR.PATH)}." # (toolkit.name, toolkit.path)
            IS_DIRECTORY = f"{S.clr("Toolkit", COLOR.TOOLKIT)} '{S.OP[0]}' cannot be registered because {S.clr(S.OP[1], COLOR.PATH)} leads to a {S.clr("directory", COLOR.ERROR)}. Toolkits must consist of a specific file." # (toolkit.name, toolkit.path)
        class CLONE:
            INVALID_TOOLKIT = f"There exists no {S.clr("Toolkit", COLOR.TOOLKIT)} named '{S.OP[0]}'." # (target_toolkit)
            ALREADY_REGISTERED = f"{S.clr("Clone", COLOR.CLONE)} '{S.OP[0]}' {S.clr("already exists", COLOR.ERROR)} at {S.clr(S.OP[1], COLOR.PATH)}." # (clone.name, clone.path)
            ALREADY_EXISTS = f"A file already exists at {S.clr(S.OP[0], COLOR.PATH)}." # (Target_path)
    class SHOW:
        class TOOLKIT:
            INVALID_TOOLKIT = f"There exists no {S.clr("Toolkit", COLOR.TOOLKIT)} named '{S.OP[0]}'." # (target_toolkit)
        class CLONE:
            INVALID_TOOLKIT = f"There exists no {S.clr("Toolkit", COLOR.TOOLKIT)} named '{S.OP[0]}'." # (target_toolkit)
            INVALID_CLONE = f"There exists no {S.clr("Clone", COLOR.CLONE)} named '{S.OP[0]}'." # (target_clone)
            UNSUCCESSFUL_DIFF = f"An error occurred during the diffing process."
    class PUSH:
        class TOOLKIT:
            NO_CLONES = f"The toolkit {S.clr(S.OP[0], COLOR.TOOLKIT)} has no clones registered and cannot be successfully pushed."
        class CLONE:
            TOOLKIT_NOT_PUSHABLE = f"The toolkit {S.clr(S.OP[0], COLOR.TOOLKIT)} is not {clr_state(STATE.UP_TO_DATE)} and cannot be pushed." # (toolkit_name)
            UP_TO_DATE = f"{TAG.CLONE.IDENT} is {S.OP[2]} and was skipped."
    class GRAB:
        class TOOLKIT:
            NO_CHANGES = f"The toolkit {S.clr(S.OP[0], COLOR.TOOLKIT)} is already {clr_state(STATE.UP_TO_DATE)}."
        class CLONE:
            TOOLKIT_HAS_CHANGES = f"The toolkit {S.clr(S.OP[0], COLOR.TOOLKIT)} is not {clr_state(STATE.UP_TO_DATE)} and cannot be replaced safely." # (toolkit_name)
            NO_NEW_VERSION = f"{TAG.CLONE.IDENT} is not {clr_state(STATE.AFTER_CORE)}." # (tk.name, clone.name)

class OUT:
    ERROR = S.clr("ERROR: ", COLOR.ERROR)+S.OP[0]+S.KEY.NL
    class SHOW:
        class ALL:
            NO_TOOLKITS = "No registered "+S.clr("toolkits", COLOR.TOOLKIT)+S.KEY.EL
            HEADER = "Registered "+S.clr("toolkits", COLOR.TOOLKIT)+S.KEY.CS+S.OP[0] # (NUM_TOOLKITS)
            LIST_ITEM = [
                S.KEY.EMPTY,                        # V0: SILENT
                S.OP[0]+S.KEY.CD,                     # V1: RESULTS_ONLY, will need to remove the last comma
                S.KEY.DH+TAG.TOOLKIT.STATE+S.KEY.NL,     # V2: NORMAL
                S.KEY.DH+TAG.TOOLKIT.PATH]     # V3: DEBUG
        class TOOLKIT:
            NO_CLONES = "No registered " + S.clr("clones", COLOR.CLONE)+"."
            HEADER = [
                S.KEY.EMPTY,                         # SILENT
                S.KEY.EMPTY,                         # RESULTS_ONLY
                f"{S.clr(S.OP[0], COLOR.TOOLKIT)} ({S.clr(S.OP[1], COLOR.VERSION)}): {S.clr(S.OP[2], COLOR.STATE)}", # (tk.name, tk.version)
                f"{S.clr(S.OP[0], COLOR.TOOLKIT)} ({S.clr(S.OP[1], COLOR.VERSION)}): {S.clr(S.OP[2], COLOR.STATE)}\n{S.clr(S.OP[3], COLOR.PATH)}" ] #(tk.name, tk.version, tk.path) ]
            LIST_ITEM = [
                S.KEY.EMPTY,
                S.OP[0]+S.KEY.CD,
                S.KEY.DH+TAG.CLONE.STATE+S.KEY.NL,
                S.KEY.DH+TAG.CLONE.PATH ]
        class CLONE:
            NO_CHANGES = "No registered " + S.clr("changes", COLOR.CLONE)+"."
            DESCRIPTION = [
                S.KEY.EMPTY,                         # SILENT
                S.KEY.EMPTY,                         # RESULTS_ONLY
                f"{TAG.CLONE.IDENT} ({S.clr(S.OP[2], COLOR.VERSION)}): {S.clr(S.OP[3], COLOR.STATE)}", # (tk.name, cl.name, cl.version, cl.state)
                f"{TAG.CLONE.IDENT} ({S.clr(S.OP[2], COLOR.VERSION)}): {S.clr(S.OP[3], COLOR.STATE)}\n{S.clr(S.OP[4], COLOR.PATH)}" ] #  (tk.name, cl.name, cl.version, cl.state, cl.path)
            DIFF_HEADER = [
                S.KEY.EMPTY, S.KEY.EMPTY,
                f"{S.clr('(*)', S.COLOUR.GREEN)}{S.clr(S.OP[0], COLOR.TOOLKIT)} -> {S.clr('(-)', S.COLOUR.RED)}{S.clr(S.OP[0], COLOR.TOOLKIT)}/{S.clr(S.OP[1], COLOR.CLONE)}", #tk.name, cl.name
                f"{S.clr('(*)', S.COLOUR.GREEN)}{S.clr(S.OP[0], COLOR.TOOLKIT)}{S.clr(S.OP[2], COLOR.PATH)}\n{S.clr('(-)', S.COLOUR.RED)}{S.clr(S.OP[0], COLOR.TOOLKIT)}/{S.clr(S.OP[1], COLOR.CLONE)}{S.clr(S.OP[3], COLOR.PATH)}" ] # tk.name, cl.name, tk.path, cl.path
    class ADD:
        TOOLKIT = [
            None, S.clr("SUCCESS", COLOR.SUCCESS),
            f"{S.clr("REGISTERED", COLOR.SUCCESS)}: {S.clr(S.OP[0], COLOR.TOOLKIT)}",
            f"{S.clr("REGISTERED", COLOR.SUCCESS)}: {S.clr(S.OP[0], COLOR.TOOLKIT)} at {S.clr(S.OP[1], COLOR.PATH)}."]
        class CLONE:
            REGISTERED = [
                None, S.clr("SUCCESS", COLOR.SUCCESS),
                f"{S.clr("REGISTERED", COLOR.SUCCESS)}: {TAG.CLONE.IDENT}",
                f"{S.clr("REGISTERED", COLOR.SUCCESS)}: {TAG.CLONE.IDENT} at {S.clr(S.OP[2], COLOR.PATH)}."] # (TK.name, Clone.name, Clone.path)
            DUPLICATED = [
                None, S.clr("SUCCESS", COLOR.SUCCESS),
                f"{S.clr("REGISTERED", COLOR.SUCCESS)}: {TAG.CLONE.IDENT}",
                f"{S.clr("REGISTERED", COLOR.SUCCESS)}: {TAG.CLONE.IDENT} /n{S.clr(S.OP[2], COLOR.PATH)} copied from {S.clr(S.OP[3], COLOR.PATH)}."] # (TK.name, Clone.name, Clone.path)
    class PUSH:
        class TOOLKIT:
            HEADER = [ # tk.name, tk.path
                None, S.clr("SUCCESS", COLOR.SUCCESS),
                f"{S.clr("PROPAGATED", COLOR.SUCCESS)}: {S.clr(S.OP[0], COLOR.TOOLKIT)}",
                f"{S.clr("PROPAGATED", COLOR.SUCCESS)}: {S.clr(S.OP[0], COLOR.TOOLKIT)} from {S.clr(S.OP[1], COLOR.PATH)}."]
            class ITEM:
                SUCCESS = [ # (clone_name, clone_path)
                    None, None,
                    f"{S.KEY.DH}{S.clr(S.OP[0], COLOR.CLONE)}: {S.clr("REPLACED",COLOR.SUCCESS)}", # (clone_name)
                    f"{S.KEY.DH}{S.clr(S.OP[0], COLOR.CLONE)}: {S.clr("REPLACED",COLOR.SUCCESS)} at {S.clr(S.OP[1], COLOR.PATH)}"] # (clone_name, clone_path)
                FAILED = [ # clone_name, clone_path, clone_error
                    None, None,
                    f"{S.KEY.DH}{S.clr(S.OP[0], COLOR.CLONE)}: {S.clr("SKIPPED",COLOR.WARNING)}\n{S.OP[2]}", # (clone_name)
                    f"{S.KEY.DH}{S.clr(S.OP[0], COLOR.CLONE)}: {S.clr("SKIPPED",COLOR.WARNING)} at {S.clr(S.OP[1], COLOR.PATH)}\n{S.OP[2]}"] # (clone_name, clone_path, clone_error)

        class CLONE:
            SUCCESS = [ # (clone_name, clone_path)
                None, f"{S.clr("SUCCESS",COLOR.SUCCESS)}",
                f"{S.clr(S.OP[0], COLOR.CLONE)}: {S.clr("SUCCESS",COLOR.SUCCESS)}", # (clone_name)
                f"{S.clr(S.OP[0], COLOR.CLONE)}: {S.clr("SUCCESS",COLOR.SUCCESS)} at {S.clr(S.OP[1], COLOR.PATH)}"] # (clone_name, clone_path)
            FAILED = [ # (clone_name, clone_path, clone_error)
                None, f"{S.clr("SKIPPED",COLOR.WARNING)}",
                f"{S.clr(S.OP[0], COLOR.CLONE)}: {S.clr("SKIPPED",COLOR.WARNING)}\n{S.OP[2]}", # (clone_name)
                f"{S.clr(S.OP[0], COLOR.CLONE)}: {S.clr("SKIPPED",COLOR.WARNING)} at {S.clr(S.OP[1], COLOR.PATH)}\n{S.OP[2]}"] # (clone_name, clone_path, clone_error)
    class GRAB:
        TOOLKIT = [ # (toolkit_name, new_version, old_version)
            None, S.clr("SUCCESS", COLOR.SUCCESS),
            f"{S.clr("UPDATED", COLOR.SUCCESS)}: {S.clr(S.OP[0], COLOR.TOOLKIT)} to {S.clr(S.OP[1], COLOR.VERSION)}",
            f"{S.clr("UPDATED", COLOR.SUCCESS)}: {S.clr(S.OP[0], COLOR.TOOLKIT)} to {S.clr(S.OP[1], COLOR.VERSION)} from {S.clr(S.OP[2], COLOR.VERSION)}"]
        CLONE = [
            None, S.clr("SUCCESS", COLOR.SUCCESS),
            f"{S.clr("UPDATED", COLOR.SUCCESS)}: {S.clr(S.OP[0], COLOR.TOOLKIT)} from {TAG.CLONE.IDENT}",
            f"{S.clr("UPDATED", COLOR.SUCCESS)}: {S.clr(S.OP[0], COLOR.TOOLKIT)} from {S.clr(S.OP[2], COLOR.PATH)} ({S.clr(S.OP[3], COLOR.VERSION)})."] # (TK.name, Clone.name, Clone.path, clone.version)

class DEPRECATED_OUT: # Command-line output, .format() required for SOME
    class LIST:
        class TOOLKITS:
            HEADER = "Registered "+COLOR.TOOLKIT+"toolkits"+COLOR.RESET+S.KEY.CS+S.OP[0]+S.KEY.NL # (NUM_TOOLKITS)
            ITEM = S.KEY.DH+TAG.TOOLKIT.ITEM+S.KEY.NL # (TOOLKIT_NAME, TOOLKIT_VERSION)
            EMPTY = S.COLOR.CANCEL+"No registered "+COLOR.TOOLKIT+"toolkits"+COLOR.RESET+S.KEY.EL
        class CLONES:
            HEADER = TAG.TOOLKIT.PATH # (TOOLKIT_NAME, TOOLKIT_VERSION, TOOLKIT_STATE, TOOLKIT_PATH)
            ITEM = S.KEY.DH+TAG.CLONE.STATE+S.KEY.NL # (CLONE_NAME, CLONE_VERSION, CLONE_STATE)


OUT_TAG_NAME = S.COLOR.SIBLING+S.OP[0]+S.COLOUR.DEFAULT
OUT_TAG_ITEM = OUT_TAG_NAME+S.KEY.CS+S.COLOR.OPTION+S.OP[1]+S.COLOUR.DEFAULT #   '[NAME]: [VERSION]'
OUT_TAG_STATE_ITEM = OUT_TAG_ITEM+" ("+S.COLOR.SUPER+S.OP[2]+S.COLOUR.DEFAULT+")"
OUT_HEADER_ITEM = OUT_TAG_STATE_ITEM+S.KEY.NL+S.OP[3]+S.KEY.NL #   '[NAME]: [VERSION] ([STATE])\n[PATH]\n'
OUT_LIST_ITEM = "- "+OUT_TAG_STATE_ITEM+S.KEY.NL      # '- [NAME]: [VERSION] ([STATE])\n'

class COMPARE:
    LESSER_THAN = -1
    EQUAL_TO = 0
    GREATER_THAN = 1

OUT_ADDED_TOOLKIT = "Added new toolkit "+TAG.TOOLKIT.NAME+S.KEY.EL
OUT_ADDED_CLONE = "Added new clone "+TAG.CLONE.IDENT+" at path "+COLOR.PATH+S.OP[2]+COLOR.RESET+S.KEY.EL
OUT_UPDATED_CLONE = "Successfully updated clone "+TAG.CLONE.IDENT+S.KEY.EL
OUT_CLONE_HAS_LOCAL = TAG.CLONE.IDENT+" has local changes"+S.KEY.EL
OUT_CLONE_UP_TO_DATE = TAG.CLONE.IDENT+" is up to date"+S.KEY.EL
OUT_GRABBED_CLONE = "Grabbed "+TAG.CLONE.IDENT+S.KEY.EL

OUT_CANT_RESOLVE_TOOLKIT = "'"+TAG.TOOLKIT.NAME+"' could "+S.COLOR.CANCEL+"not"+S.COLOUR.DEFAULT+" be resolved to a toolkit"+S.KEY.EL
OUT_CANT_RESOLVE_CLONE = "'"+TAG.CLONE.IDENT+"' could "+S.COLOR.CANCEL+"not"+COLOR.RESET+" be resolved to a clone"+S.KEY.EL



