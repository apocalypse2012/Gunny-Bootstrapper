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
Module Documentation: commands\maxStartup.py

3dsmax Boostrapper command class for StartService.
"""


import os
from .baseCommand import Command
from libs_gunny import config
from libs_gunny.config.constants import *
from libs_gunny.commands import util


class StartMax(Command):

    PARSER_DESC = 'Launch 3dsmax with MGDS pipeline'
    # default max version if one is not specified
    MAX_VERSION = '2016'
    # supported choices
    MAX_VER_CHOICES = {'2015': '17000', MAX_VERSION: '18000'}

    # default debugger
    DEBUGGER_TYPE = 'wing5'
    # supported choices
    DEBUGGER_CHOICES = [DEBUGGER_TYPE]

    def __init__(self, subParsers):
        self.max_scripts_dir = None
        self.max_version = None
        self.debug_spec = None
        super(StartMax, self).__init__(subParsers)

    def registerArguments(self, parser):

        # set up argument parsing and options
        parser.add_argument("-s",
                            "--scripts",
                            dest='max_scripts_dir',
                            help="3dsmax script path")

        parser.add_argument("-v",
                            "--version",
                            choices=self.MAX_VER_CHOICES.keys(),
                            default=self.MAX_VERSION,
                            dest='max_version',
                            help="3dsmax version number")

        parser.add_argument("-d",
                            "--debug",
                            choices=self.DEBUGGER_CHOICES,
                            default=None,
                            dest='debug_spec',
                            help="python debugger",
                            required=False)

    def setState(self, args):
        """ Use the args properties to set state into on the class. Return self. """
        self.max_scripts_dir = args.max_scripts_dir
        self.max_version = args.max_version
        self.debug_spec = args.debug_spec
        return self

    def doCommand(self):
        """ execute the intended procedure. """

        setupLocation = util.STARTSERVICE_PATH
        mp_root = config.config_func.FindMaxPlayRoot(setupLocation)
        config.config_envar_defaults.SetEnvarDefaults(mp_root)

        max_version = self.MAX_VER_CHOICES[self.max_version]
        dcc_vers = (DESC_CONFIG_3DSMAX, max_version)
        MpConfig = config.config_parse.Config_Parser(dcc_vers)
        if self.max_scripts_dir:
            if os.path.isdir(self.max_scripts_dir):
                scripts_dir = os.path.split(self.max_scripts_dir)[0]
                configScriptsDir = (scripts_dir, ABSOLUTE_PATH_FLAG)
                setattr(MpConfig, APP_CONFIG_PATH, configScriptsDir)
            elif os.path.isfile(self.max_scripts_dir):
                configScriptsDir = (self.maya_scripts_dir, ABSOLUTE_PATH_FLAG)
                setattr(MpConfig, APP_CONFIG_PATH, configScriptsDir)
            else:
                print ("Specified 3dsmax userSetup script not found.")
                print ("Using fall back configuration.")

        MpConfig.SetEnvironmentVars()
        MpConfig.SetPythonPaths()
        retCode = config.bootstrap.BootstrapApp(MpConfig)
        return retCode

