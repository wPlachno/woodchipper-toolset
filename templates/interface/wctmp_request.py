import pathlib

from utilities.wcparser import CLParser as WCParser

def build_parser():
    parser = WCParser("wctmp",
                      version="0.0.0.1",
                      description="A script for extracting pieces out of one file to other files.",
                      footer="Created by Will Plachno. Copyright 2024.")
    parser.add_argument("path", default=None, shaper=path_shaper,
                        description="The path for the target file.")
    parser.add_argument("mode", default="normal")
    parser.add_argument("--version")
    parser.add_argument("--help", "-h")
    return parser

def path_shaper(text):
    return pathlib.Path(text).resolve()
