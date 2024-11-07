import pytest

import wctk_request as WCParser
from wcutil import WoodchipperSettingsFile as WCProfile
from wctk_printer import WoodchipperToolkitPrinter as WCPrinter
from wcconstants import Verbosity
from constants import MODE, TEST

class Test_Parser:
    @staticmethod
    def do_parse(args):
        parser = WCParser.build_parser()
        WCProfile.setup_argparse_parser_with_config(parser)
        ns = parser.parse_args(args)
        proceed = Test_Parser.check_parser(ns)
        if not proceed:
            ns.mode = MODE.NONE
        return ns

    @staticmethod
    def check_parser(argparse_args):
        proceed = not argparse_args.config
        if not argparse_args.test is None:
            proceed = False
        return proceed

    def test_parser_wctk(self):
        args = ['/home/osboxes/Documents/Code/woodchipper-toolset/wctk.py']
        results = Test_Parser.do_parse(args)
        assert results.mode == MODE.SHOW
        assert str(results.path) == '/home/osboxes/Documents/Code/woodchipper-toolset'
        assert results.target is None

    def test_parser_wctk_jimmy(self):
        args = ['/home/osboxes/Documents/Code/woodchipper-toolset/wctk.py', 'jimmy']
        results = Test_Parser.do_parse(args)
        assert results.mode == MODE.SHOW
        assert str(results.path) == '/home/osboxes/Documents/Code/woodchipper-toolset'
        assert results.target == 'jimmy'

    def test_parser_wctk_jimmyjack(self):
        args = ['/home/osboxes/Documents/Code/woodchipper-toolset/wctk.py', 'jimmy/jack']
        results = Test_Parser.do_parse(args)
        assert results.mode == MODE.SHOW
        assert str(results.path) == '/home/osboxes/Documents/Code/woodchipper-toolset'
        assert results.target == 'jimmy/jack'

    def test_parser_wctk_add_jimmy(self):
        args = ['/home/osboxes/Documents/Code/woodchipper-toolset/wctk.py', 'add', 'jimmy']
        results = Test_Parser.do_parse(args)
        assert results.mode == MODE.ADD
        assert str(results.path) == '/home/osboxes/Documents/Code/woodchipper-toolset'
        assert results.target == 'jimmy'

    def test_parser_wctk_add_jimmyjack(self):
        args = ['/home/osboxes/Documents/Code/woodchipper-toolset/wctk.py', 'add', 'jimmy/jack']
        results = Test_Parser.do_parse(args)
        assert results.mode == MODE.ADD
        assert str(results.path) == '/home/osboxes/Documents/Code/woodchipper-toolset'
        assert results.target == 'jimmy/jack'

    def test_parser_wctk_add_jimmy_jimmytxt(self):
        args = ['/home/osboxes/Documents/Code/woodchipper-toolset/wctk.py', 'add', 'jimmy', 'jimmy.txt']
        results = Test_Parser.do_parse(args)
        assert results.mode == MODE.ADD
        assert str(results.path) == '/home/osboxes/Documents/Code/woodchipper-toolset/jimmy.txt'
        assert results.target == 'jimmy'

    def test_parser_wctk_add_jimmyjack_jacktxt(self):
        args = ['/home/osboxes/Documents/Code/woodchipper-toolset/wctk.py', 'add', 'jimmy/jack', 'jack.txt']
        results = Test_Parser.do_parse(args)
        assert results.mode == MODE.ADD
        assert str(results.path) == '/home/osboxes/Documents/Code/woodchipper-toolset/jack.txt'
        assert results.target == 'jimmy/jack'

    def test_parser_wctk_push_jimmy(self):
        args = ['/home/osboxes/Documents/Code/woodchipper-toolset/wctk.py', 'push', 'jimmy']
        results = Test_Parser.do_parse(args)
        assert results.mode == MODE.PUSH
        assert str(results.path) == '/home/osboxes/Documents/Code/woodchipper-toolset'
        assert results.target == 'jimmy'
        assert results.force == False

    def test_parser_wctk_push_jimmyjohn(self):
        args = ['/home/osboxes/Documents/Code/woodchipper-toolset/wctk.py', 'push', 'jimmy/john']
        results = Test_Parser.do_parse(args)
        assert results.mode == MODE.PUSH
        assert str(results.path) == '/home/osboxes/Documents/Code/woodchipper-toolset'
        assert results.target == 'jimmy/john'
        assert results.force == False

    def test_parser_wctk_push_jimmy_f(self):
        args = ['/home/osboxes/Documents/Code/woodchipper-toolset/wctk.py', 'push', 'jimmy', '-f']
        results = Test_Parser.do_parse(args)
        assert results.mode == MODE.PUSH
        assert str(results.path) == '/home/osboxes/Documents/Code/woodchipper-toolset'
        assert results.target == 'jimmy'
        assert results.force == True

    def test_parser_wctk_push_jimmyjohn_f(self):
        args = ['/home/osboxes/Documents/Code/woodchipper-toolset/wctk.py', 'push', 'jimmy/john', '-f']
        results = Test_Parser.do_parse(args)
        assert results.mode == MODE.PUSH
        assert str(results.path) == '/home/osboxes/Documents/Code/woodchipper-toolset'
        assert results.target == 'jimmy/john'
        assert results.force == True

    def test_parser_wctk_grab_jimmy(self):
        args = ['/home/osboxes/Documents/Code/woodchipper-toolset/wctk.py', 'grab', 'jimmy']
        results = Test_Parser.do_parse(args)
        assert results.mode == MODE.GRAB
        assert str(results.path) == '/home/osboxes/Documents/Code/woodchipper-toolset'
        assert results.target == 'jimmy'
        assert results.force == False

    def test_parser_wctk_grab_jimmyjohn(self):
        args = ['/home/osboxes/Documents/Code/woodchipper-toolset/wctk.py', 'grab', 'jimmy/john']
        results = Test_Parser.do_parse(args)
        assert results.mode == MODE.GRAB
        assert str(results.path) == '/home/osboxes/Documents/Code/woodchipper-toolset'
        assert results.target == 'jimmy/john'
        assert results.force == False

    def test_parser_wctk_grab_jimmy_f(self):
        args = ['/home/osboxes/Documents/Code/woodchipper-toolset/wctk.py', 'grab', 'jimmy', '-f']
        results = Test_Parser.do_parse(args)
        assert results.mode == MODE.GRAB
        assert str(results.path) == '/home/osboxes/Documents/Code/woodchipper-toolset'
        assert results.target == 'jimmy'
        assert results.force == True

    def test_parser_wctk_grab_jimmyjohn_f(self):
        args = ['/home/osboxes/Documents/Code/woodchipper-toolset/wctk.py', 'grab', 'jimmy/john', '-f']
        results = Test_Parser.do_parse(args)
        assert results.mode == MODE.GRAB
        assert str(results.path) == '/home/osboxes/Documents/Code/woodchipper-toolset'
        assert results.target == 'jimmy/john'
        assert results.force == True

    def test_parser_wctk_config(self):
        args = ['/home/osboxes/Documents/Code/woodchipper-toolset/wctk.py', '--config']
        results = Test_Parser.do_parse(args)
        assert results.mode == MODE.NONE
        assert str(results.path) == '/home/osboxes/Documents/Code/woodchipper-toolset'
        assert results.target is None
        assert results.config == True
        assert results.verbosity is None
        assert results.debug is None

    def test_parser_wctk_config_verbosity(self):
        with pytest.raises(ValueError):
            args = ['/home/osboxes/Documents/Code/woodchipper-toolset/wctk.py', '--config', '--verbosity']
            results = Test_Parser.do_parse(args)
            assert results.mode == MODE.NONE
            assert str(results.path) == '/home/osboxes/Documents/Code/woodchipper-toolset'
            assert results.target is None
            assert results.config == True
            assert results.verbosity is None
            assert results.debug is None

    def test_parser_wctk_config_verbosity_2(self):
        args = ['/home/osboxes/Documents/Code/woodchipper-toolset/wctk.py', '--config', '--verbosity', '2']
        results = Test_Parser.do_parse(args)
        assert results.mode == MODE.NONE
        assert str(results.path) == '/home/osboxes/Documents/Code/woodchipper-toolset'
        assert results.target is None
        assert results.config == True
        assert results.verbosity ==2
        assert results.debug is None

    def test_parser_wctk_config_debug(self):
        with pytest.raises(ValueError):
            args = ['/home/osboxes/Documents/Code/woodchipper-toolset/wctk.py', '--config', '--debug']
            results = Test_Parser.do_parse(args)
            assert results.mode == MODE.NONE
            assert str(results.path) == '/home/osboxes/Documents/Code/woodchipper-toolset'
            assert results.target is None
            assert results.config == True
            assert results.verbosity is None
            assert results.debug is None

    def test_parser_wctk_config_debug_off(self):
        args = ['/home/osboxes/Documents/Code/woodchipper-toolset/wctk.py', '--config', '--debug', 'off']
        results = Test_Parser.do_parse(args)
        assert results.mode == MODE.NONE
        assert str(results.path) == '/home/osboxes/Documents/Code/woodchipper-toolset'
        assert results.target is None
        assert results.config == True
        assert results.verbosity is None
        assert results.debug == False

    def test_parser_wctk_verbosity(self):
        with pytest.raises(ValueError):
            args = ['/home/osboxes/Documents/Code/woodchipper-toolset/wctk.py', '--verbosity']
            results = Test_Parser.do_parse(args)
            assert results.mode == MODE.SHOW
            assert str(results.path) == '/home/osboxes/Documents/Code/woodchipper-toolset'
            assert results.target is None
            assert results.config == False
            assert results.verbosity is None
            assert results.debug is None

    def test_parser_wctk_verbosity_2(self):
        args = ['/home/osboxes/Documents/Code/woodchipper-toolset/wctk.py', '--verbosity', '2']
        results = Test_Parser.do_parse(args)
        assert results.mode == MODE.SHOW
        assert str(results.path) == '/home/osboxes/Documents/Code/woodchipper-toolset'
        assert results.target is None
        assert results.config == False
        assert results.verbosity ==2
        assert results.debug is None

    def test_parser_wctk_debug(self):
        with pytest.raises(ValueError):
            args = ['/home/osboxes/Documents/Code/woodchipper-toolset/wctk.py', '--debug']
            results = Test_Parser.do_parse(args)
            assert results.mode == MODE.SHOW
            assert str(results.path) == '/home/osboxes/Documents/Code/woodchipper-toolset'
            assert results.target is None
            assert results.config == False
            assert results.verbosity is None
            assert results.debug is None

    def test_parser_wctk_debug_off(self):
        args = ['/home/osboxes/Documents/Code/woodchipper-toolset/wctk.py', '--debug', 'off']
        results = Test_Parser.do_parse(args)
        assert results.mode == MODE.SHOW
        assert str(results.path) == '/home/osboxes/Documents/Code/woodchipper-toolset'
        assert results.target is None
        assert results.config == False
        assert results.verbosity is None
        assert results.debug == False

    def test_parser_wctk_add_jimmy_jimmytxt_config_verbosity_2(self):
        args = ['/home/osboxes/Documents/Code/woodchipper-toolset/wctk.py', 'add', 'jimmy', 'jimmy.txt', '--config', '--verbosity', '2']
        results = Test_Parser.do_parse(args)
        assert results.mode == MODE.NONE
        assert str(results.path) == '/home/osboxes/Documents/Code/woodchipper-toolset/jimmy.txt'
        assert results.target == 'jimmy'
        assert results.config == True
        assert results.verbosity ==2
        assert results.debug is None

    def test_parser_wctk_add_jimmy_jimmytxt_verbosity_2(self):
        args = ['/home/osboxes/Documents/Code/woodchipper-toolset/wctk.py', 'add', 'jimmy', 'jimmy.txt', '--verbosity', '2']
        results = Test_Parser.do_parse(args)
        assert results.mode == MODE.ADD
        assert str(results.path) == '/home/osboxes/Documents/Code/woodchipper-toolset/jimmy.txt'
        assert results.target == 'jimmy'
        assert results.config == False
        assert results.verbosity ==2
        assert results.debug is None


