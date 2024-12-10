"""
wcconstants.py
Created by Will Plachno on 09/07/24
Version 0.0.0.10

Woodchipper Constants
An assortment of helpful strings and other constants.
"""

EMPTY=""
NL="\n"     # New Line
FS="/"      # Forward Slash
BS="\\"     # Back Slash
QU="\""     # Quotes
CD=", "     # Comma Delimiter
SDL=":"     # IS THIS USED?
ES="."      # End Statement
EL=".\n"    # End line

CS=": "     # Colon Separator
DH=" - "    # Description Hyphen

OOB=-1

OP0="{0}"
OP1="{1}"
OP2="{2}"
OP3="{3}"
OP4="{4}"
OP5="{5}"

COLOR_RED='\033[0;31m'
COLOR_GREY='\033[90m'
COLOR_YELLOW='\033[93m'
COLOR_BLUE='\033[94m'
COLOR_DARK_YELLOW='\033[0;33m'
COLOR_GREEN='\033[0;32m'
COLOR_DARK_GREEN='\033[2;32m'
COLOR_PURPLE='\033[0;35m'
COLOR_BLACK='\033[0;30m'
COLOR_WHITE='\033[37m'
COLOR_DEFAULT='\033[0m'

COLOR_SUPER=COLOR_PURPLE
COLOR_SUB=COLOR_GREY
COLOR_SUBSIB=COLOR_DARK_GREEN
COLOR_SIBLING=COLOR_DARK_YELLOW
COLOR_OPTION=COLOR_BLUE
COLOR_QUOTE=COLOR_GREEN
COLOR_ACTIVE=COLOR_GREEN
COLOR_CANCEL=COLOR_RED

CL_DESC_ACTIVE = COLOR_ACTIVE+"Active"+COLOR_DEFAULT
CL_DESC_INACTIVE = COLOR_CANCEL+"Inactive"+COLOR_DEFAULT
CL_DESC_SUCCESS = COLOR_ACTIVE+"Success"+COLOR_DEFAULT
CL_DESC_FAILURE = COLOR_CANCEL+"Failure"+COLOR_DEFAULT

CL_DESC_ATTRIBUTE = COLOR_SIBLING+OP0+COLOR_DEFAULT+CS+OP1+NL
CL_DESC_TASK = COLOR_SUPER+"Task"+COLOR_DEFAULT+CS
CL_DESC_UNIMPLEMENTED = " ["+COLOR_CANCEL+"UNIMPLEMENTED"+COLOR_DEFAULT+"]"
CL_DESC_MODE_CONFIG = CL_DESC_TASK+COLOR_SUB+"Config"+COLOR_DEFAULT+DH+COLOR_SIBLING+OP0+COLOR_DEFAULT+CS+OP1+NL
CL_DESC_CONFIG_ERROR = CL_DESC_TASK+COLOR_SUB+"Config"+COLOR_DEFAULT+DH+COLOR_CANCEL+OP0+COLOR_DEFAULT+NL
CL_DESC_TEST_PASS = CL_DESC_TASK+COLOR_SUB+"Test Passed"+COLOR_DEFAULT+DH+COLOR_ACTIVE+OP0+COLOR_DEFAULT+NL
CL_DESC_TEST_FAIL = CL_DESC_TASK+COLOR_SUB+"Test Failed"+COLOR_DEFAULT+DH+COLOR_CANCEL+OP0+COLOR_DEFAULT+NL

READ = "r"
WRITE = "w"
EXCLUSIVE_CREATION = "x"

DEBUG = "debug"
VERBOSE = "verbose"
TEST = "test"
UNDEFINED = "undefined"
ON = "on"
OFF = "off"

FILE_NAME_SETTINGS = ".wcp_Settings.txt"
PREFERRED_TIME_FORMAT = "%m%d%y:%H:%M:%S"
TEST_TAG = "test: "

ON_SYNONYMS = list(("on", "true", "1", "yes",
                   "t", "y", "+", "active",
                   "positive", "a", "p"))

class Verbosity:
    SILENT = 0 # As little output as possible.
    RESULTS_ONLY = 1 # Only show requested
    NORMAL = 2 # Includes warnings and big errors
    DEBUG = 3 # Print all messages possible

