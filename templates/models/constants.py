# Our application uses WoodchipperNamespaces for data transfer
# between the CLI and the Controller. These constants represent
# the keys added to the request (CLI->Cntl) and results (Cntl->CLI)
# namespaces.
class KEY:

    class FILE:
        NAME = "name"
        PATH = "path"
        CONTENT = "content"
        CONTROL = "control"