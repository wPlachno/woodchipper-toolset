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
        HANDLER = "handler"
        SUCCESS = "success"
        ERROR = "error"
        FILES = "files"
        CONTROL = "control"

    class EXPANDER:
        HANDLER = "handler"
        SUCCESS = "success"
        ERROR = "error"
        FILES = "files"
        CONTROL = "control"



class TOKEN:
    START = '@{'
    DELIMITER = '|'
    TEXT = "}{{"
    END = '}}'