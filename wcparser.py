from types import SimpleNamespace

import wcconstants as S
import sys

class CLP_Argument:
    def __init__(self, *name_or_tags, default=None, description="", optional=True, nargs=0, choices=None, hide=False, shaper=None):
        self.name = ""
        self.tags = []
        self.flag = False
        self.choices = choices
        self.default = default
        self.description = description
        self.hide = hide
        self.optional = optional
        self.nargs = nargs
        self.shaper = shaper
        self.value = self.default
        if self.choices:
            self.default = self.choices[0]
        self._decipher_name_or_tags(name_or_tags)

    def _decipher_name_or_tags(self, name_or_tags):

        self.tags = name_or_tags
        for tag in self.tags:
            if tag.startswith("-"):
                self.flag = True
            else:
                self.name = tag
            if tag.startswith("--"):
                self.flag = True
                self.name = tag[2:]
                break
        if self.name == "":
            self.name = "UNKNOWN"

    def set_value(self, value):
        if self.shaper:
            self.value = self.shaper(value)
        else:
            self.value = value

    def get_usage(self):
        usage_clr = S.COLOR_SUPER
        usage_str = ( "["+self.name+"]" if self.optional else self.name )
        if self.choices:
            usage_str = "{" + ", ".join(self.choices) + "}"
        elif self.flag:
            usage_str = ", ".join(self.tags)
            if self.optional:
                usage_str = "[" + usage_str + "]"
            usage_clr = S.COLOR_SIBLING
        return usage_clr + usage_str + S.COLOR_DEFAULT

    def print_help(self):
        return self.get_usage() + S.NL + S.DH + self.description + S.NL

    def check_arg(self, index, args):
        current_arg = args[index]
        if self.choices:
            if current_arg in self.choices:
                self.set_value(current_arg)
                return index+1
        elif current_arg in self.tags:
            if self.nargs == 0:
                self.set_value(True)
                return index + 1
            elif self.nargs == 1:
                if index+1 < len(args):
                    self.set_value(args[index+1])
                    return index+2
                else:
                    raise ValueError
            else:
                value = []
                offset = 1
                while offset <= self.nargs and offset + index < len(args):
                    value.append(args[index + offset])
                    offset += 1
                self.set_value(value)
                return index + offset
        return index

    def found(self):
        return self.value is None

class CLParser:
    def __init__(self, name=None, version=None, description=None, footer=None, include_usage=True):
        self.name = name
        self.version = version
        self.description = description
        self.footer = footer
        self.include_usage = include_usage
        self.args = []
        self.namespace = SimpleNamespace()

    def add_argument(self, *name_or_tags, default=None, description="", optional=True, nargs=0, choices=None, hide=False, shaper=None):
        self.args.append(CLP_Argument(*name_or_tags,
                     default=default,
                     description=description,
                     optional=optional,
                     nargs=nargs,
                     choices=choices,
                     hide=hide,
                     shaper=shaper))

    def parse_args(self, args):
        pos_args = []
        index = 1
        while index < len(args):
            found = False
            for arg in self.args:
                new_index = arg.check_arg(index, args)
                if not index == new_index:
                    found = True
                    index = new_index
                    break
            if not found:
                pos_args.append(args[index])
                index += 1
        if len(pos_args) > 0:
            target_arg = 0
            for arg in self.args:
                if not arg.flag and not arg.choices and target_arg < len(pos_args):
                    arg.set_value(pos_args[target_arg])
                    target_arg += 1
        return self._create_namespace()

    def _create_namespace(self):
        for arg in self.args:
            if not arg.found() and not arg.optional:
                sys.exit("Incorrect command line argument")
            setattr(self.namespace, arg.name, arg.value)
        if self.namespace.help:
            self.print_help()
            sys.exit(0)
        return self.namespace

    def print_help(self):
        print()
        # Usage line:
        # usage: [name] arg.usage
        if self.include_usage:
            print(self.get_usage())
        # Description
        if self.description:
            print(self.description)
        # Arguments:
        # positional arguments:
        # args.print_help(), self.flag == false
        print("Arguments: ")
        for arg in self.args:
            if not arg.flag and not arg.hide:
                print(arg.print_help())
        # Options:
        # options:
        # args.print_help(), self.flag == true
        print("Options: ")
        for arg in self.args:
            if arg.flag and not arg.hide:
                print(arg.print_help())
        # Footer
        if self.footer:
            print(self.footer)

    def print_version(self):
        if self.version:
            print(self.version)

    def get_usage(self):
        usage_str = "usage: "
        for arg in self.args:
            usage_str += arg.get_usage() + " "
        return usage_str

