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
import os.path
from libs_gunny import config
from libs_gunny.commands import util
from libs_gunny.config.constants import *


class Command(object):

    __metaclass__ = abc.ABCMeta

    PARSER_DESC = 'Should never see this. Override in derived class.'

    def __init__(self, parser):

        setupLocation = util.GUNNY_ENTRYPOINT_PATH
        mp_root = config.config_func.FindRootMarker(setupLocation)
        config.config_func.SetEnvarDefaults(mp_root)
        self.root_config = config.config_parse.Config_Parser()

        if self.isValid:
            self.root_config.Add_DCC_Config(self.dcc_default_config)

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


