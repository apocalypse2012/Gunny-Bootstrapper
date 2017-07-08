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
Module Documentation: commands\blenderStartup.py

Blender Boostrapper command class for Gunny.
"""


import os
from .baseCommand import Command
from libs_gunny import config
from libs_gunny.config.constants import *
from libs_gunny.config.config_marshall import ConfigPath


class Blender(Command):

    PARSER_DESC = 'Launch Blender with pipeline'
    # default debugger
    DEBUGGER_TYPE = 'wing5'
    # supported choices
    DEBUGGER_CHOICES = [DEBUGGER_TYPE]

    def __init__(self, parser=None):
        self.blender_scripts_dir = None
        self.debug_spec = None
        self.root_config = None
        self.config_key = DESC_CONFIG_BLENDER
        super(Blender, self).__init__(parser)

    def _registerArguments(self, parser):

        # set up argument parsing and options
        parser.add_argument("-s",
                            "--scripts",
                            dest='blender_scripts_dir',
                            help="Blender script path")

        parser.add_argument("-d",
                            "--debug",
                            choices=self.DEBUGGER_CHOICES,
                            default=None,
                            dest='debug_spec',
                            help="python debugger",
                            required=False)

    def _setState(self, args):
        """ Use the args properties to set state into on the class. Return self. """
        self.blender_scripts_dir = args.blender_scripts_dir
        self.debug_spec = args.debug_spec
        return self


    def doCommand(self):
        """ execute the intended procedure. """

        if self.blender_scripts_dir:
            if os.path.isdir(self.blender_scripts_dir):
                scripts_dir = os.path.split(self.blender_scripts_dir)[0]
                configScriptsDir = (scripts_dir, ABSOLUTE_PATH_FLAG)
                setattr(self.root_config, APP_CONFIG_PATH, configScriptsDir)
            elif os.path.isfile(self.blender_scripts_dir):
                configScriptsDir = (self.blender_scripts_dir, ABSOLUTE_PATH_FLAG)
                setattr(self.root_config, APP_CONFIG_PATH, configScriptsDir)
            else:
                print ("Specified Blender userSetup script not found.")
                print ("Using fall back configuration.")

        return self.launch()

