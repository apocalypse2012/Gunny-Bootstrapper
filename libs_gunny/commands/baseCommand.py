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
Module Documentation: commands\baseCommand.py

This is the base class from which all bootstrap 'Commands' are derived. All command common code resides here. This is an
ABC and requires several methods to be defined in the sub-class. This base class is primarily concerned with initializing
from a subparser returned by ArgParse. It registers itself with the subparser, calls its own registerArguments on the
instance returned, then registers a callback to another internal method that captures the parsed data.
"""

import abc
import os.path, os, time
import subprocess
from libs_gunny import config
from libs_gunny.commands import util
from libs_gunny.config.constants import *


def get_all_subclasses(cls):
    """
    This function returns a list of all subclasses of the the given class. Will march the whole class hierarchy.
    :param cls: Class to inspect.
    :return: List of classes.
    """
    all_subclasses = []

    for subclass in cls.__subclasses__():
        all_subclasses.append(subclass)
        all_subclasses.extend(get_all_subclasses(subclass))

    return all_subclasses


def Parse_Commands(parser):
    # Get all classes that inheret from Command. Instantiate each command class with a subparser instance.
    # After parsing, the Parse args contains the validated launcher. Execute the launchers doCommand().
    subparsers = parser.add_subparsers(dest='tools')
    for launchers in get_all_subclasses(Command):
        launchers(subparsers)
    args = parser.parse_args()
    launcher = args.func(args)
    retcode = launcher.doCommand()
    parser.exit(retcode)


class Command(object):

    __metaclass__ = abc.ABCMeta

    PARSER_DESC = 'Should never see this. Override in derived class.'

    def __init__(self, parser):
        self.proc = None
        setupLocation = util.GUNNY_ENTRYPOINT_PATH
        mp_root = config.config_func.FindRootMarker(setupLocation)
        config.config_func.SetEnvarDefaults(mp_root)
        self.root_config = config.config_parse.Config_Parser(self.config_key)

        if self.isValid:
            if parser is not None:
                parserInst = parser.add_parser(self.__class__.__name__, help=self.PARSER_DESC)
                self._registerArguments(parserInst)
                parserInst.set_defaults(func=self._setState)

    def isValid(self):
        dcc_file = config.bootstrap.GetInstalledApp(self.root_config)
        if os.path.isfile(dcc_file) and os.path.exists(dcc_file):
            return True
        return False

    @abc.abstractmethod
    def _registerArguments(self, parser):
        """ Add class specific Arguments to the parser to solicit state info required by the class. """
        return

    @abc.abstractmethod
    def _setState(self, args):
        """ Use the args properties to set state into on the class. Return self. """
        return

    @abc.abstractmethod
    def doCommand(self):
        """ execute the intended procedure. """
        return

    def launch(self):
        self.root_config.SetEnvironmentVars()
        self.root_config.SetPythonPaths()
        dccRunTime, new_env = config.bootstrap.BootstrapApp(self.root_config)
        retCode = subprocess.call(dccRunTime, env=new_env)
        return retCode

    def run(self):
        self.root_config.SetEnvironmentVars()
        self.root_config.SetPythonPaths()
        dcc_runtime, new_env = config.bootstrap.BootstrapApp(self.root_config)
        print('run: {}'.format(dcc_runtime))
        if self.proc is not None:
            self.proc.terminate()
        #TODO: Replace this hack with something more robust.
        DEVNULL = open(os.devnull, 'wb')
        self.proc = subprocess.Popen(dcc_runtime, stdout=DEVNULL, env=new_env)
        time.sleep(2)

    def stop(self):
        if self.proc is not None:
            self.proc.terminate()

