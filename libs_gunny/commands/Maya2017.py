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


CONFIG_MAYA_2017_DEFAULT= {
    APP_ID: 'a5472549-704d-4505-a50d-ef3baeee87b2',
    DESC_CONFIG_DCC: DESC_CONFIG_MAYA,
    APP_VERSION: STR_2017,
    EXECUTABLE_COMMAND: MAYA_RELATIVE_EXE_PATH,
    BOOTSTRAP_TYPE: PYTHON_PATH,
    BOOTSTRAP_FILE: MAYA_SETUP_FILE,
    REG_ENTRY_INSTALL: MAYA_REG_KEY,
    REG_PATH_INSTALL: MAYA_REG_PATH_2017,
    ENV_PATH_INSTALL: MAYA_ENV_PATH,
    APP_ROOT_TYPE: ENVAR_DCC_PATH,
    APP_CONFIG_PATH: ConfigPath(paths=[MAYA_PATH_SCRIPTS],
                                flags=[ENVAR_DCC_PATH,
                                       RELATIVE_PATH_FLAG]),
    APP_PY_PACKAGES: ConfigPath(paths=[DIR_MAYA],
                                flags=[ENVAR_DCC_PATH,
                                       RELATIVE_PATH_FLAG,
                                       PYTHON_PATH_FLAG]),
    MAYA_SCRIPT_PATH: ConfigPath(paths=[MAYA_PATH_SCRIPTS_2017,
                                        MAYA_PATH_MEL_2017,
                                        MAYA_PATH_PYTHON_2017,
                                        MAYA_PATH_SCRIPTS,
                                        MAYA_PATH_MEL,
                                        MAYA_PATH_PYTHON],
                                   flags=[ENVAR_DCC_PATH,
                                          RELATIVE_PATH_FLAG,
                                          ENV_VAR_FLAG,
                                          PYTHON_PATH_FLAG]),
    XBMLANG_PATH: ConfigPath(paths=[MAYA_PATH_ICONS],
                              flags=[ENVAR_DCC_PATH,
                                     RELATIVE_PATH_FLAG,
                                     ENV_VAR_FLAG]),
    MAYA_PLUG_IN_PATH: ConfigPath(paths=[MAYA_PATH_PLUGINS_2017],
                                    flags=[ENVAR_DCC_PATH,
                                           RELATIVE_PATH_FLAG,
                                           ENV_VAR_FLAG])
}
CONFIG_MAYA = config.config_defaults.CONFIG_MAYA_TYPE(**CONFIG_MAYA_2017_DEFAULT)._asdict()


class StartMaya_2017(Command):

    PARSER_DESC = 'Launch Maya with pipeline'

    # default debugger
    DEBUGGER_TYPE = 'wing5'
    # supported choices
    DEBUGGER_CHOICES = [DEBUGGER_TYPE]

    def __init__(self, parser=None):
        self.maya_scripts_dir = None
        self.debug_spec = None
        global CONFIG_MAYA
        self.dcc_default_config = CONFIG_MAYA
        super(StartMaya_2017, self).__init__(parser)

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

