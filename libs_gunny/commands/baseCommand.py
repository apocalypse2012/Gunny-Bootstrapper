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

class Command(object):

    __metaclass__ = abc.ABCMeta

    PARSER_DESC = 'Should never see this. Override in derived class.'

    def __init__(self, subParsers):

        parserInst = subParsers.add_parser(self.__class__.__name__, help=self.PARSER_DESC)
        self.registerArguments(parserInst)
        parserInst.set_defaults(func=self.setState)

    @abc.abstractmethod
    def registerArguments(self, parser):
        """ Add class specific Arguments to the parser to solicit state info required by the class. """
        return

    @abc.abstractmethod
    def setState(self, args):
        """ Use the args properties to set state into on the class. Return self. """
        return

    @abc.abstractmethod
    def doCommand(self):
        """ execute the intended procedure. """
        return


