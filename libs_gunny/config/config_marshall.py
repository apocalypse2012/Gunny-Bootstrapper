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
import exceptions
import json


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


class Configuration_Signature_Error(exceptions.IndexError):
    pass


class ConfigEncoder(json.JSONEncoder):
    """
    Part of the JSON object Parsing mechanism. Implements as default function that returns the dictionary result of any
    object with an method 'toDict' or the baseclass default value. This is to guarantee output from the Ordered Dict
    Object type.
    """

    # This mapping associates a given signature of attributes with a type that can deserialize the data. For use with class_
    # mapper(). This mapping and the function (class_mapper) and class that follow (ConfigEncoder) provide an abstraction
    # between the config state data in the Config_Parser objects (which are stored in dictionaries) and the config_default
    # data templates which are defined in Named_Tuples to guarantee serialization order in the config file.
    JSON_MAPPING = {frozenset(('paths', 'flags')): ConfigPath, }

    @staticmethod
    def class_mapper(d):
        """
        Part of the JSON object hook parsing mechanism. Uses to JSON mapping types above to template the data structures
        parsed from file. This class guarantees parsing of objects to Named Tuple and output to dictionaries.
        :param d: JSON load object
        :return: The object itself or an instance of the correct data structure containing the parsed values.
        """
        obj = None
        for keys, cls in ConfigEncoder.JSON_MAPPING.items():
            if not keys.symmetric_difference(d.keys()):
                obj = cls(**d)
                if hasattr(obj, '_asdict'):
                    return obj._asdict()
                else:
                    return obj
        return d

    def add_mapping(self, new_type):
        mapping = frozenset(new_type._fields)
        if not mapping in ConfigEncoder.JSON_MAPPING:
            ConfigEncoder.JSON_MAPPING[mapping] = new_type
        else:
            raise Configuration_Signature_Error("JSON mapping already contains a data specification with that signature.")

    def remove_mapping(self, del_type):
        mapping = frozenset(del_type._fields)
        if mapping in ConfigEncoder.JSON_MAPPING:
            del(ConfigEncoder.JSON_MAPPING[mapping])
        else:
            raise Configuration_Signature_Error("Specified data spec not found.")

    def default(self, obj):
        if hasattr(obj,'toDict'):
            return obj.toDict()
        else:
            return json.JSONEncoder.default(self, obj)

