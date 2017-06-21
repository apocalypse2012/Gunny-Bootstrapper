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
from libs_gunny.config.constants import *
from libs_gunny import config
from libs_gunny.commands import util


class StartMaya(Command):

    PARSER_DESC = 'Launch Maya with pipeline'
    # default maya version if one is not specified
    MAYA_VERSION = '2017'
    # supported choices
    MAYA_VER_CHOICES = ['2015', '2016', MAYA_VERSION]

    # default debugger
    DEBUGGER_TYPE = 'wing5'
    # supported choices
    DEBUGGER_CHOICES = [DEBUGGER_TYPE]

    def __init__(self, subParsers):
        self.maya_scripts_dir = None
        self.maya_version = None
        self.debug_spec = None
        super(StartMaya, self).__init__(subParsers)

    def registerArguments(self, parser):

        # set up argument parsing and options
        parser.add_argument("-s",
                            "--scripts",
                            dest='maya_scripts_dir',
                            help="Maya script path")

        parser.add_argument("-v",
                            "--version",
                            choices=self.MAYA_VER_CHOICES,
                            default=self.MAYA_VERSION,
                            dest='maya_version',
                            help="Maya version number")

        parser.add_argument("-d",
                            "--debug",
                            choices=self.DEBUGGER_CHOICES,
                            default=None,
                            dest='debug_spec',
                            help="python debugger",
                            required=False)

    def setState(self, args):
        """ Use the args properties to set state into on the class. Return self. """
        self.maya_scripts_dir = args.maya_scripts_dir
        self.maya_version = args.maya_version
        self.debug_spec = args.debug_spec
        return self

    def doCommand(self):
        """ execute the intended procedure. """

        setupLocation = util.GUNNY_ENTRYPOINT_PATH
        mp_root = config.config_func.FindRootMarker(setupLocation)
        config.config_func.SetEnvarDefaults(mp_root)

        dcc_vers = (DESC_CONFIG_MAYA, self.maya_version)
        MpConfig = config.config_parse.Config_Parser(dcc_vers)
        if self.maya_scripts_dir:
            if os.path.isfile(self.maya_scripts_dir):
                scripts_dir = os.path.split(self.maya_scripts_dir)[0]
                configScriptsDir = config.config_marshall.ConfigPath(scripts_dir, ABSOLUTE_PATH_FLAG)
                setattr(MpConfig, APP_CONFIG_PATH, configScriptsDir.toDict())
            elif os.path.isdir(self.maya_scripts_dir):
                configScriptsDir = config.config_marshall.ConfigPath(self.maya_scripts_dir, ABSOLUTE_PATH_FLAG)
                setattr(MpConfig, APP_CONFIG_PATH, configScriptsDir.toDict())
            else:
                print ("~ {0}: Specified Maya userSetup script not found.".format(__file__))
                print ("~ {0}: Using fall back configuration.".format(__file__))

        MpConfig.SetEnvironmentVars()
        MpConfig.SetPythonPaths()
        retCode = config.bootstrap.BootstrapApp(MpConfig)
        return retCode

