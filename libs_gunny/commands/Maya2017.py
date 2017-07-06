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
Module Documentation: commands\mayaStartup.py

Maya Boostrapper command class for Gunny.
"""


import os
from .baseCommand import Command
from libs_gunny import config
from libs_gunny.config.constants import *
from libs_gunny.config.config_marshall import ConfigPath


class Maya_2017(Command):

    PARSER_DESC = 'Launch Maya with pipeline'

    # default debugger
    DEBUGGER_TYPE = 'wing5'
    # supported choices
    DEBUGGER_CHOICES = [DEBUGGER_TYPE]

    def __init__(self, parser=None):
        self.maya_scripts_dir = None
        self.debug_spec = None
        self.root_config = None
        self.config_key = DESC_CONFIG_MAYA
        super(Maya_2017, self).__init__(parser)

    def _registerArguments(self, parser):

        # set up argument parsing and options
        parser.add_argument("-s",
                            "--scripts",
                            dest='maya_scripts_dir',
                            help="Maya script path")

        parser.add_argument("-d",
                            "--debug",
                            choices=self.DEBUGGER_CHOICES,
                            default=None,
                            dest='debug_spec',
                            help="python debugger",
                            required=False)

    def _setState(self, args):
        """ Use the args properties to set state into on the class. Return self. """
        self.maya_scripts_dir = args.maya_scripts_dir
        self.debug_spec = args.debug_spec
        return self

    def doCommand(self):
        """ execute the intended procedure. """

        if self.maya_scripts_dir:
            if os.path.isfile(self.maya_scripts_dir):
                scripts_dir = os.path.split(self.maya_scripts_dir)[0]
                configScriptsDir = config.config_marshall.ConfigPath(scripts_dir, ABSOLUTE_PATH_FLAG)
                setattr(self.root_config, APP_CONFIG_PATH, configScriptsDir.toDict())
            elif os.path.isdir(self.maya_scripts_dir):
                configScriptsDir = config.config_marshall.ConfigPath(self.maya_scripts_dir, ABSOLUTE_PATH_FLAG)
                setattr(self.root_config, APP_CONFIG_PATH, configScriptsDir.toDict())
            else:
                print ("~ {0}: Specified Maya userSetup script not found.".format(__file__))
                print ("~ {0}: Using fall back configuration.".format(__file__))

        self.root_config.SetEnvironmentVars()
        self.root_config.SetPythonPaths()
        retCode = config.bootstrap.BootstrapApp(self.root_config)
        return retCode

