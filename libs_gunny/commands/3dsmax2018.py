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

3dsmax Boostrapper command class for Gunny.
"""


import os
from .baseCommand import Command
from libs_gunny import config
from libs_gunny.config.constants import *
from libs_gunny.config.config_marshall import ConfigPath


CONFIG_3DSMAX_2018_DEFAULT = {
    APP_ID: 'b4d31e56-5b75-4020-9474-b5fcb1c6c7e7',
    DESC_CONFIG_DCC: DESC_CONFIG_3DSMAX,
    APP_VERSION: '20000',
    EXECUTABLE_COMMAND: '3dsmax.exe -U PythonHost startup.py',
    BOOTSTRAP_TYPE: "path",
    BOOTSTRAP_FILE: "startup.ms",
    REG_ENTRY_INSTALL: 'Installdir',
    REG_PATH_INSTALL: 'SOFTWARE\\Autodesk\\3dsMax\\20.0',
    ENV_PATH_INSTALL: 'ADSK_3DSMAX_X64_2018',
    APP_ROOT_TYPE: ENVAR_DCC_PATH,
    APP_CONFIG_PATH: ConfigPath(paths=["Max\\scripts",
                                       "Max\\2018\\scripts"],
                                flags=[ENVAR_DCC_PATH,
                                       RELATIVE_PATH_FLAG]),
    APP_PY_PACKAGES: ConfigPath(paths=["Max",
                                       "Max\\2018"],
                                flags=[ENVAR_DCC_PATH,
                                       RELATIVE_PATH_FLAG,
                                       PYTHON_PATH_FLAG]),
    MAX_PLUGIN_PATH: ConfigPath(paths=["Max\\2018\\plugins"],
                                     flags=[ENVAR_DCC_PATH,
                                            RELATIVE_PATH_FLAG,
                                            ENV_VAR_FLAG])
}
CONFIG_3DSMAX = config.config_defaults.CONFIG_3DSMAX_TYPE(**CONFIG_3DSMAX_2018_DEFAULT)._asdict()


class StartMax_2018(Command):

    PARSER_DESC = 'Launch 3dsmax with pipeline'
    # default max version if one is not specified

    # default debugger
    DEBUGGER_TYPE = 'wing5'
    # supported choices
    DEBUGGER_CHOICES = [DEBUGGER_TYPE]

    def __init__(self, parser=None):
        self.max_scripts_dir = None
        self.debug_spec = None
        self.root_config = None
        global CONFIG_3DSMAX
        self.dcc_default_config = CONFIG_3DSMAX

        ## DONE TODO: Make parser optional on instantiation.
        ## DONE TODO: only run the parent __init__ if the class validation function passes or parser is not none.
        ## DONE TODO: set default state of state variables is parser is none.-*
        super(StartMax_2018, self).__init__(parser)


    def _registerArguments(self, parser):

        # set up argument parsing and options
        parser.add_argument("-s",
                            "--scripts",
                            dest='max_scripts_dir',
                            help="3dsmax script path")

        parser.add_argument("-d",
                            "--debug",
                            choices=self.DEBUGGER_CHOICES,
                            default=None,
                            dest='debug_spec',
                            help="python debugger",
                            required=False)

    def _setState(self, args):
        """ Use the args properties to set state into on the class. Return self. """
        self.max_scripts_dir = args.max_scripts_dir
        self.debug_spec = args.debug_spec
        return self

## DONE TODO: Move root setup to __init__
## DONE TODO: Move Config instantiation to __init__
## Done TODO: Create a validation function to test the executable state (bootstrap.GetInstalledApp)
## TODO: Modify bootstrap to reference a pipe object that is managed in this class through some kind of callback
## TODO: Create a StartCommand function to run doCommand from a thread. Or optionally modify Bootstrap to be non-blocking.
## TODO: Add getters and setters for state variables.

    def doCommand(self):
        """ execute the intended procedure. """

        if self.max_scripts_dir:
            if os.path.isdir(self.max_scripts_dir):
                scripts_dir = os.path.split(self.max_scripts_dir)[0]
                configScriptsDir = (scripts_dir, ABSOLUTE_PATH_FLAG)
                setattr(MpConfig, APP_CONFIG_PATH, configScriptsDir)
            elif os.path.isfile(self.max_scripts_dir):
                configScriptsDir = (self.max_scripts_dir, ABSOLUTE_PATH_FLAG)
                setattr(MpConfig, APP_CONFIG_PATH, configScriptsDir)
            else:
                print ("Specified 3dsmax userSetup script not found.")
                print ("Using fall back configuration.")

        self.root_config.SetEnvironmentVars()
        self.root_config.SetPythonPaths()
        retCode = config.bootstrap.BootstrapApp(self.root_config)
        return retCode

