import os
import pathlib

from utilities.wcparser import CLParser as WCParser

def build_parser():
    parser = WCParser("wctk",
                      version="0.0.0.1",
                      description="A script for maintaining several copies of a toolkit between several projects.",
                      footer="Created by Will Plachno. Copyright 2024.")
    parser.add_argument("mode", choices=["show", "add", "grab", "push"], default="show",
                        description="The mode we are operating in. If none are explicitly provided, we assume show mode. Add mode will add a new toolkit at a path or a new clone. Grab mode will grab the clone to overwrite the core. Push mode will push from the core to the clones. Show mode shows all information regarding the target.")
    parser.add_argument("target",
                        description="The target for the script. Should either be a toolkit name or the combination of a 'toolkit/clone' name of one of the clones belonging to that toolkit.")
    parser.add_argument("path", default=os.getcwd(), shaper=path_shaper,
                        description="The path for the target. Only necessary when adding a new toolkit or clone.")
    parser.add_argument("-f", "--force", default=False,
                        description="Modifies push or grab tasks to ignore the status of the destination.")
    parser.add_argument("--version")
    parser.add_argument("--help", "-h")
    return parser

def path_shaper(text):
    return pathlib.Path(text).resolve()
