#!/usr/bin/env python
#coding:utf-8
# -- This line is 75 characters -------------------------------------------
__author__ = "Raymond Stewart"
__copyright__ = "Copyright 2017"
__credits__ = ["Raymond Stewart"]
__license__ = "EULA"
__version__ = "1.0.0"
__maintainer__ = "Raymond Stewart"
__email__ = "raymond.stewart@raymond-stewart.com"
__status__ = "development"

"""
Module Documentation: commands\Gunny_REPL.py

REPL for Gunny.
"""


import os
import cmd
from .baseCommand import Command, get_all_subclasses
from libs_gunny import config
from libs_gunny.config.constants import *
from libs_gunny.config.config_marshall import ConfigPath


class InteractiveShell(cmd.Cmd):
    """Accepts commands via the normal interactive prompt or on the command line."""

    def __init__(self, **kwargs):
        cmd.Cmd.__init__(self, **kwargs)
        self._Commands = get_all_subclasses(Command)

    def do_greet(self, line):
        print 'hello,', line

    def default(self, line):
        if '-h' in line:
            print('\n'.join([i.__name__ for i in self._Commands if not i.__name__ == 'Shell']))
        for obj in self._Commands:
            if obj.__name__ in line:
                obj().doCommand()


    def do_EOF(self, line):
        return True



class Shell(Command):

    PARSER_DESC = 'Enter Gunny Commandline'
    # default max version if one is not specified

    # default debugger
    DEBUGGER_TYPE = 'wing5'
    # supported choices
    DEBUGGER_CHOICES = [DEBUGGER_TYPE]

    def __init__(self, parser=None):
        self.debug_spec = None
        self.root_config = None
        self.dcc_default_config = None
        super(Shell, self).__init__(parser)


    def _registerArguments(self, parser):

        # set up argument parsing and options
        parser.add_argument("-d",
                            "--debug",
                            choices=self.DEBUGGER_CHOICES,
                            default=None,
                            dest='debug_spec',
                            help="python debugger",
                            required=False)

    def _setState(self, args):
        """ Use the args properties to set state into on the class. Return self. """
        self.debug_spec = args.debug_spec
        return self

    def isValid(self):
        return True

    def doCommand(self):
        """ execute the intended procedure. """

        InteractiveShell().cmdloop()
