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
import time
import types
import inspect
from .baseCommand import Command, get_all_subclasses
from libs_gunny import config
from libs_gunny.config.constants import *
from libs_gunny.config.config_marshall import ConfigPath


class InteractiveShell(cmd.Cmd):
    """Accepts commands via the normal interactive prompt or on the command line."""

    prompt = 'Gunny: '
    intro = "Configuration and launch environment for Pipeline applications."

    #doc_header = 'doc_header'
    #misc_header = 'misc_header'
    #undoc_header = 'undoc_header'

    ruler = '-'

    def __init__(self, **kwargs):
        cmd.Cmd.__init__(self, **kwargs)
        self._commands = [obj() for obj in get_all_subclasses(Command) if obj is not Shell]
        self._current = None

    def hold_and_clr(self, duration=3):
        time.sleep(duration)
        absolutely_unused_variable = os.system('cls')

    def precmd(self, line):
        self.hold_and_clr(0)
        print(self.intro)
        return line

    def do_Select(self, command):
        command = command.lower()
        if 'none' in command:
            self._current = None
            self.prompt = 'Gunny: '
            return
        for object in self._commands:
            if object.__class__.__name__.lower() in command:
                self._current = object
                self.prompt = object.__class__.__name__ + ': '
                return
        print('\nWarning, DCC application selection not recognized: {}\n'.format(command))

    def help_Select(self):
        print('\nSelect [launcher]\n')
        for object in self._commands:
            helpStr = getattr(object, 'PARSER_DESC')
            padStr = '                    '
            nameStr = object.__class__.__name__
            nameStr = nameStr + ':' + padStr[len(nameStr):]
            print('\t{}\t\t{}'.format(nameStr, helpStr))
        print('\n')

    def do_Launch(self, command):
        if self._current is not None:
            getattr(self._current, 'doCommand')()
        else:
            print('\nNo selected DCC Application to Launch...\nPlease use \'Select\' first.\n')

    def help_Launch(self):
        print('\nLaunch the currently selected DCC application: {}\n'.format(self._current.__class__.__name__))

    # TODO: Make Setter and Getters for config attributes. Also Help and Save.
    # TODO: Also, current shell does not filter for valid command classes.
    # def _listCurAttributes(self):
    #     config = self._current.root_config
    #     propnames = [name for (name, value) in inspect.getmembers(config, lambda o: isinstance(o, property))]
    #     return propnames
    #
    # def do_GetConfig(self, param):
    #     if self._current is not None:
    #         config = self._current.root_config
    #         if hasattr(config, param):
    #             selName = self._current.__class__.__name__
    #             value = getattr(config, param)
    #             print('{}, {}, {}'.format(selName, param, value))
    #     else:
    #         print('\nNo selected DCC Application to configure...\nPlease use \'Select\' first.\n')
    #
    # def help_GetConfig(self):
    #     props = self._listCurAttributes()
    #     print('\nGetConfig [Attribute]\n')
    #     for name in props:
    #         padStr = '                    '
    #         nameStr = name + ':' + padStr[len(name):]
    #         print('\t{}'.format(nameStr))
    #     print('\n')
    #
    # def do_SetConfig(self, param):
    #     if self._current is not None:
    #         config = self._current.root_config
    #     else:
    #         print('\nNo selected DCC Application to configure...\nPlease use \'Select\' first.\n')

    def default(self, line):
        if 'select' in line:
            args = line[len('select'):].lstrip()
            self.do_Select(args)
        elif 'launch' in line:
            args = line[len('launch'):].lstrip()
            self.do_Launch(args)
        elif 'quit' in line or 'exit' in line or 'end' in line:
            self.hold_and_clr(0)
            return True
        elif 'Help' in line:
            pass
        else:
            print('\nWarning, Unrecognized command: {}\n'.format(line))

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
        absolutely_unused_variable = os.system('cls')
        InteractiveShell().cmdloop()
