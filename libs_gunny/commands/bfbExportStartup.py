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
Module Documentation: MpPy\mp_command\bfbExportStartup.py

Startup class to manage the BFB export subparser for Gunny.

"""


import os
from .baseCommand import Command
from libs_gunny import config
from libs_gunny.config.constants import *
from libs_gunny.commands import util


class StartBFB(Command):

    PARSER_DESC = 'Export from Maya with BFB pipeline'
    # default maya version if one is not specified
    MAYA_VERSION = '2016'
    MAYAPY_RUNSCRIPT = 'BFB_ExportScene.py'
    EXPORT_INFILE = 'INFILE'
    EXPORT_OUTFILE = 'OUTFILE'
    ASCII_STATE = 'ascii'

    def __init__(self, subParsers):
        self.export_inputfile = None
        self.export_outputfile = None
        self.export_ASCII = False
        super(StartBFB, self).__init__(subParsers)

    def registerArguments(self, parser):

        parser.add_argument(self.EXPORT_INFILE,
                            help="Supply the full pathname to the input file.")

        parser.add_argument(self.EXPORT_OUTFILE,
                            help="Path to the export dir or target filename. No suffix.")

        parser.add_argument("-a",
                            "--ascii",
                            help="Export ascii for debugging.",
                            default=self.export_ASCII,
                            dest=self.ASCII_STATE,
                            action="store_true")


    def setState(self, args):
        """ Use the args properties to set state into on the class. Return self. """
        print(args)
        dictArgs = vars(args)
        self.export_ASCII = dictArgs.get(self.ASCII_STATE, None)
        self.export_inputfile = dictArgs.get(self.EXPORT_INFILE, None)
        self.export_outputfile = dictArgs.get(self.EXPORT_OUTFILE, False)
        return self

    def doCommand(self):
        """ execute the intended procedure. """

        setupLocation = util.GUNNY_ENTRYPOINT_PATH
        mp_root = config.config_func.FindRootMarker(setupLocation)
        config.config_func.SetEnvarDefaults(mp_root)

        if self.export_inputfile and os.path.exists(self.export_inputfile) and self.export_outputfile:
            dcc_vers = (DESC_CONFIG_MAYAPY, self.MAYA_VERSION)
            MpConfig = config.config_parse.Config_Parser(dcc_vers)

            script_path_obj = getattr(MpConfig, MAYA_SCRIPT_PATH)
            print("~ {0}: MAYA_SCRIPT_PATH \"{1}\"".format(__file__, script_path_obj))
            for loc in script_path_obj.Paths:
                export_script = os.path.join(loc, self.MAYAPY_RUNSCRIPT)
                print("~ {0}: export_script \"{1}\"".format(__file__, export_script))
                if os.path.isfile(export_script):
                    cmd_value = getattr(MpConfig, EXECUTABLE_COMMAND)
                    print("~ {0}: cmd_value \"{1}\"".format(__file__, cmd_value))
                    cmd_script_call = ' '.join([cmd_value,
                                                export_script,
                                                self.export_inputfile,
                                                self.export_outputfile,
                                                str(self.export_ASCII)])
                    setattr(MpConfig, EXECUTABLE_COMMAND, cmd_script_call)
                    print("~ {0}: cmd_script_call \"{1}\"".format(__file__, cmd_script_call))
                    break

            MpConfig.SetEnvironmentVars()
            MpConfig.SetPythonPaths()
            retCode = config.bootstrap.BootstrapApp(MpConfig)
        else:
            retCode = os.EX_USAGE
        return retCode

