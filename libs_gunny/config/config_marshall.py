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
Module Documentation: MpPy\mp_config\config_marshall.py

< document module here>
"""

from constants import *
import config_func


# Class to resolve environment references at runtime after the project root has been defined.
class ValidEnvars(object):
    def __init__(self, theEnVar=''):
        self._enVar = theEnVar

    @property
    def EnvVar(self):
        return config_func.GetEnvarDefaults(self._enVar)

    def __str__(self):
        return self.EnvVar

    def __repr__(self):
        return "ValidEnvars(theEnVar={})".format(self._enVar)


class ConfigPath(object):

    def __init__(self, paths=[], flags=[]):
        self._paths = paths
        if isinstance(paths, basestring):
            self._paths = [paths]
        if isinstance(flags, basestring):
            flags = [flags]
        self._relativeFlag = RELATIVE_PATH_FLAG in flags
        self._absoluteFlag = ABSOLUTE_PATH_FLAG in flags
        self._environmentFlag = ENV_VAR_FLAG in flags
        self._pythonFlag = PYTHON_PATH_FLAG in flags

        if ENVAR_GUNNY_ROOT in flags:
            self._rootType = ENVAR_GUNNY_ROOT
            self._root = ValidEnvars(ENVAR_GUNNY_ROOT)
        elif ENVAR_TOOLS_PATH in flags:
            self._rootType = ENVAR_TOOLS_PATH
            self._root = ValidEnvars(ENVAR_TOOLS_PATH)
        else:
            self._rootType = ENVAR_DCC_PATH
            self._root = ValidEnvars(ENVAR_DCC_PATH)

    def toDict(self, forceAbsolute=False):
        retDict = {}
        if forceAbsolute:
            self._absoluteFlag is True
            self._relativeFlag is False
        retDict['paths'] = self.Paths
        retDict['flags'] = self.Flags
        return retDict

    @property
    def Root(self):
        return str(self._root)

    @property
    def Flags(self):
        flags = []
        if self._environmentFlag:
            flags.append(ENV_VAR_FLAG)
        if self._pythonFlag:
            flags.append(PYTHON_PATH_FLAG)
        if self._absoluteFlag:
            flags.append(ABSOLUTE_PATH_FLAG)
        elif self._relativeFlag:
            flags.append(RELATIVE_PATH_FLAG)
            if self._rootType:
                flags.append(self._rootType)
        return flags

    @property
    def Paths(self):
        retPaths = []
        for path in self._paths:
            rPath = str(path)
            if self._relativeFlag:
                rPath = os.path.join(self.Root, rPath)
            rPath = os.path.normpath(rPath)
            retPaths.append(rPath)
        return retPaths

    @property
    def relative(self):
        return self._relativeFlag

    @property
    def absolute(self):
        return self._absoluteFlag

    @property
    def environment_variable(self):
        return self._environmentFlag

    @property
    def python_path(self):
        return self._pythonFlag

    @property
    def is_valid(self):
        return len(self._paths) > 0
