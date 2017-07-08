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
from collections import OrderedDict
from .baseCommand import Command, get_all_subclasses
from libs_gunny import config
from libs_gunny.config.constants import *
from libs_gunny.config.config_marshall import ConfigPath


class InteractiveShell(cmd.Cmd):
    """Accepts commands via the normal interactive prompt or on the command line."""

    _prompt = 'Gunny: '
    intro = "Configuration and launch environment for Pipeline applications."

    #doc_header = 'doc_header'
    #misc_header = 'misc_header'
    #undoc_header = 'undoc_header'

    ruler = '-'

    def __init__(self, **kwargs):
        cmd.Cmd.__init__(self, **kwargs)
        self._commands = [obj() for obj in get_all_subclasses(Command) if obj is not Shell]
        self._selection = OrderedDict()

    @property
    def _current(self):
        keys = self._selection.keys()
        if len(keys)>0:
            lastKey = keys[-1]
            return self._selection.get(lastKey)
        else:
            return None

    @property
    def prompt(self):
        if self._current is None:
            return 'Gunny: '
        else:
            present = '>'.join(self._selection.keys())
            prompt = '{}: '.format(present)
            return prompt

    def _listCurAttributes(self):
        propnames = []
        if self._current in self._commands:
            config = self._current.root_config
            propnames = [key for key in config.GetConfigNames()]
            propnames.sort()
        elif type(self._current) is ConfigPath:
            propnames = ['Paths', 'Flags']
        return propnames

    def hold_and_clr(self, duration=3):
        time.sleep(duration)
        absolutely_unused_variable = os.system('cls')

    def precmd(self, line):
        self.hold_and_clr(0)
        print(self.intro)
        return line

    def do_Select(self, line):
        selected = line.lower()
        names = self._listCurAttributes()
        if self._current is None:
            for launcher in self._commands:
                if launcher.__class__.__name__.lower() in selected:
                    self._selection[line] = launcher
                    return
        else:
            if isinstance(self._current, Command):
                config = self._current.root_config
            else:
                config = self._current
            if line in names:
                new_selection = getattr(config, line)
                if isinstance(new_selection, ConfigPath):
                    self._selection[line] = new_selection
                    return
        print('\nWarning, DCC application selection not recognized: {}\n'.format(line))

    def do_Deselect(self, trash):
        if self._current is not None:
            self._selection.popitem()

    def help_Deselect(self):
        return "Stuff and things"

    def help_Select(self):
        print('\nSelect [object/attribute]\n')
        padStr = '                         '
        nameStr = helpStr = ''
        if self._current is None:
            for object in self._commands:
                helpStr = getattr(object, 'PARSER_DESC')
                nameStr = object.__class__.__name__
                nameStr = nameStr + ':' + padStr[len(nameStr):]
                print('\t{}\t\t{}'.format(nameStr, helpStr))
        else:
            names = self._listCurAttributes()
            for name in names:
                if isinstance(self._current, Command):
                    config = self._current.root_config
                    value = getattr(config, name)
                    helpStr = config.__class__.__name__ + '.' + getattr(config, '_current_dcc')
                    if type(value) is ConfigPath:
                        nameStr = name + ':' + padStr[len(name):]
                        print('\t{}\t\t{}'.format(nameStr, helpStr))
        print('\n')

    def do_Run(self, line):
        launcher = None
        if self._current in self._commands:
            launcher = self._current
        else:
            for command_object in self._selection.values():
                if command_object in self._commands:
                    launcher = command_object
        if launcher is not None:
            getattr(launcher, 'run')()
        else:
            print('\nNo selected DCC Application to Run...\nPlease use \'Select\' first.\n')

    def help_Run(self):
        print('\nRun the currently selected DCC application: {}\n'.format(self._current.__class__.__name__))

    def do_Stop(self, line):
        launcher = None
        if self._current in self._commands:
            launcher = self._current
        else:
            for command_object in self._selection.values():
                if command_object in self._commands:
                    launcher = command_object
        if launcher is not None:
            getattr(launcher, 'stop')()
        else:
            print('\nNo selected DCC Application to Stop...\nPlease use \'Select\' first.\n')

    def help_Stop(self):
        print('\nStop the currently selected DCC application: {}\n'.format(self._current.__class__.__name__))

    def do_Get(self, line):
        selName = param = value = None
        if self._current is not None:
            names = self._listCurAttributes()
            selName = self._current.__class__.__name__
            if line in names:
                if isinstance(self._current, Command):
                    config = self._current.root_config
                    if hasattr(config, line):
                        value = getattr(config, line)
                elif isinstance(self._current, ConfigPath):
                    if hasattr(self._current, line):
                        valueList = getattr(self._current, line)
                        value = ';'.join(valueList)
                else:
                    if hasattr(self._current, line):
                        value = getattr(self._current, line)
        if value is not None:
            print('The value of {} in {} is \n\n\t{}\n'.format(line, selName, value))
        else:
            print('Attribute name not recognized or supported on the currently selected object.')

    def help_Get(self):
        print('Get the value of the requested configuration attribute.')

    def do_Attributes(self, line):
        if self._current is not None:
            props = self._listCurAttributes()
            if self._current in self._commands:
                config = self._current.root_config
            else:
                config = self._current
            presentData = ''
            for name in props:
                value = getattr(config, name)
                if type(value) is ConfigPath:
                    continue
                padStr = '                              '
                nameStr = name + ':' + padStr[len(name):]
                newValue = '\t{}{}\n'.format(nameStr, value)
                presentData += newValue
            print('\nGetConfig [Attribute]\n')
            print(presentData)
            print('\n')
        else:
            print('\nNo selected DCC Application to configure...\nPlease use \'Select\' first.\n')

    def help_Attributes(self):
        print('Get editable attribute names for the selected DCC application config.')

    def do_Set(self, line):
        args = line.split()
        if len(args) > 1:
            param, value = args[:2]
        else:
            return
        if self._current is not None:
            props = self._listCurAttributes()
            if param in props:
                if type(self._current) is ConfigPath:
                    old_param, old_value = self._selection.popitem()
                    old_path = old_value.toDict()
                    fix_Param_Case = param.lower()
                    old_path[fix_Param_Case] = value.split(';')
                    new_path = ConfigPath(**old_path)
                    setattr(self._current.root_config, old_param, new_path)
                    self._selection[old_param] = new_path
                else:
                    config = self._current if self._current not in self._commands else self._current.root_config
                    old = getattr(config, param)
                    value = type(old)(value)
                    setattr(config, param, value)
            else:
                print('\nConfiguration attribute is not assignable...\n')
        else:
            print('\nNo selected DCC Application to configure...\nPlease use \'Select\' first.\n')

    def help_Set(self):
        print('Assign a value to the referenced attribute for the selected DCC application config.')

    def do_Save(self, line):
        if self._current is not None:
            searchSet = set(self._selection.values())
            sourceSet = set(self._commands)
            saveObj = searchSet.intersection(sourceSet).pop()
            saveObj.root_config.SaveConfig()
            print('Modified Config attributes are now saved to Gunny AppData.')
        else:
            print('\nNo selected DCC Application to configure...\nPlease use \'Select\' first.\n')

    def help_Save(self):
        print('Save configuration changes to file.')

    def default(self, line):
        try:
            if 'deselect' in line.lower():
                args = line[len('deselect'):].lstrip()
                self.do_Deselect(args)
            elif 'select' in line.lower():
                args = line[len('select'):].lstrip()
                self.do_Select(args)
            elif 'launch' in line.lower():
                args = line[len('launch'):].lstrip()
                self.do_Run(args)
            elif 'get' in line.lower():
                args = line[len('get'):].lstrip()
                self.do_Get(args)
            elif 'attributes' in line.lower():
                args = line[len('attributes'):].lstrip()
                self.do_Attributes(args)
            elif 'set' in line.lower():
                args = line[len('set'):].lstrip()
                self.do_Set(args)
            elif 'save' in line.lower():
                args = line[len('save'):].lstrip()
                self.do_Save(args)
            elif 'quit' in line.lower() or 'exit' in line.lower() or 'end' in line.lower():
                self.hold_and_clr(0)
                return True
            elif 'help' in line.lower():
                pass
            else:
                print('\nWarning, Unrecognized command: {}\n'.format(line))
        except TypeError:
            print('\nNo selected DCC Application to configure...\nPlease use \'Select\' first.\n')

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
        self.config_key = DESC_CONFIG_BLENDER
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
