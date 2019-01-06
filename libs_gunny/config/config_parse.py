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
Module Documentation: MpPy\mp_config\config_parse.py

< document module here>
"""

import filecmp
import json
import site
import shutil
import exceptions
import copy
from collections import Mapping, Sequence, OrderedDict
from config_marshall import ConfigPath, ValidEnvars, ConfigEncoder
from config_func import updateEnvironmentPath, getEnvironmentPath, GetEnvarDefaults
import config_defaults
from constants import *


_IGNORE_DESCRIPTORS = [COMMENT_QUALIFIER, TEMPLATE_QUALIFIER]
def ignorable(descriptor):
    """
    Check is a string matches any of the ignorable string constants in the list.
    :param descriptor: Any String
    :return: True is descriptor is ignorable.
    """
    found = False
    for name in _IGNORE_DESCRIPTORS:
        if name in descriptor:
            found = True
    return found


def deep_update(d, u, punk=False, clean=False):
    """
    Recursive function to update a nested data set.
    :param d: Dataset to update.
    :param u: Dataset to update from.
    :param punk: If true, replicate the hierarchy of u, but do not populate data.
    :param clean: If true, data structure parameters will not update where there are no valid update values. Default is false.
    :return: The updated dataset containing the structure if not the data of the input.
    """
    if isinstance(u, Mapping):
        for k, v in u.iteritems():
            dv = d.get(k, type(v)()) if v else None
            r = deep_update(dv, v, punk, clean)
            if r or not clean:
                d[k] = r
    elif isinstance(u, Sequence) and not isinstance(u, basestring):
        new_d = []
        for i, v in enumerate(u):
            tv = type(v)() if v else None
            dv = tv if len(d) != len(u) else d[i]
            r = deep_update(dv, v, punk, clean)
            if r or not clean:
                new_d.append(r)
        d = new_d
    elif punk:
        d = None
    elif isinstance(u, (basestring, ValidEnvars)):
        d = str(u)
    elif isinstance(u, ConfigPath):
        d = u if u.is_valid else d
    elif u or not clean:
        d = u
    else:
        return None
    return d


def EnsureBackup(temp_file, save_file):
    """
    Diff file and save with backup if changed... Remove the temp file.
    :param temp_file: Updated file to be saved
    :param save_file: Final save file.
    :return: None
    """
    temp_file = temp_file.lower()
    save_file = save_file.lower()
    bakFile = save_file + '.bak'
    sameFileData = filecmp.cmp(temp_file, save_file, shallow=0)
    if not sameFileData:
        shutil.copyfile(save_file, bakFile)
        shutil.copyfile(temp_file, save_file)
    os.remove(temp_file)


class Unspecified_DCC(exceptions.IndexError):
    pass


class Config_Parser(object):
    """
    This is the core class of the config system. It is primarily a data container used by any system that needs to query
    the configuration data. This is a smart object intended to manage state changed in the system configuration as well
    as initiating loading, saving, and persistance of managed data in the OS environment.
    """

    _CURRENT_CONFIG = OrderedDict()

    def _set_CURRENT_CONFIG__(self, new_val, clean=False):
        the_config = type(self)._CURRENT_CONFIG
        deep_update(the_config, new_val, clean=clean)
        self._generate_config_attributes()

    def __init__(self, key=None):
        """
        Initialization of a new Config Parser object. This is responsible for defining and initializing the current
        configuration which is stored as a class variable. This insures that the configuration state follows a Borg
        pattern that is guaranteed to remain common to all instances.
        :param dcc_vers: This is an input to identify the application and Version of for Digital Content Creation.
        """
        self._current_dcc = key
        self._naming_spec = dict()
        self._default_config = config_defaults.DEFAULT_CONFIGURATION

        if type(self)._CURRENT_CONFIG == OrderedDict():
            self._set_CURRENT_CONFIG__(config_defaults.DEFAULT_CONFIGURATION)
            self._set_CURRENT_CONFIG__(self._load_file_config())
            self._set_CURRENT_CONFIG__(self._get_env_config(), clean=True)

        self.SaveConfig()

    def GetAttrByStructName(self, name):
        fetch_name = self._get_param_name(name, self._current_dcc)
        if hasattr(self, fetch_name):
            return getattr(self, fetch_name)

    def _marchConfig(self, config=None):
        """
        This private generator method takes an Ordered Dict of config data and marches the data structure. Each call
        yields the next tuple consisting of an attribute name, value, section. This is used
        to identify that there is configuration data supported to match the DCC application and version.
        :param config: Ordered Dict of config data
        :return: Tuple of attribute name, value, parent. Returns a valid index when matches the dcc version.
        """
        if config is None:
            config = type(self)._CURRENT_CONFIG
        for section, contents in config.iteritems():
            if contents is None:
                raise Exception
            for name, value in contents.iteritems():
                if not ignorable(name):
                    yield (name, value, section)

    def _fill_namespec(self):
        ignore_section = config_defaults.IGNORE_CONFIG_BLOCK
        for nm, val, stn in self._marchConfig():
            if stn in ignore_section:
                key = nm
            elif isinstance(val, ConfigPath) and val.environment_variable:
                key = nm
            else:
                key = nm + '_' + stn
            value = (nm, stn)
            self._naming_spec[key] = value

    def GetConfigNames(self):
        include_section = config_defaults.IGNORE_CONFIG_BLOCK
        if len(self._naming_spec) is 0:
            self._fill_namespec()
        for key, value in self._naming_spec.iteritems():
            nm, stn = value
            if stn == self._current_dcc:
                yield key
            elif stn not in key and stn in include_section:
                yield key

    def _get_param_name(self, name, section):
        if len(self._naming_spec) is 0:
            self._fill_namespec()
        fetch_name = name + '_' + section
        if fetch_name in self._naming_spec:
            return fetch_name
        else:
            return name

    def _get_structure_name(self, fetch_name):
        if len(self._naming_spec) is 0:
            self._fill_namespec()
        if fetch_name in self._naming_spec:
            return self._naming_spec[fetch_name]

    def SaveConfig(self, *args, **kwargs):
        """
        Save the current configuration state.
        :return:
        """
        config_value = getattr(self, APPDATA)
        path_value = config_value.AbsolutePaths[0]
        default_cfg_file = os.path.join(path_value, CONFIG_FILE_NAME)
        temp_file = default_cfg_file + '.TEMP'
        if os.path.exists(default_cfg_file):
            json.dump(type(self)._CURRENT_CONFIG,
                      open(temp_file.lower(),
                           mode='w'),
                      cls=ConfigEncoder,
                      sort_keys=False,
                      indent=4)
            EnsureBackup(temp_file, default_cfg_file)
        else:
            if not os.path.isdir(path_value):
                os.mkdir(path_value)
            json.dump(type(self)._CURRENT_CONFIG,
                      open(default_cfg_file.lower(),
                           mode='w'),
                      cls=ConfigEncoder,
                      sort_keys=False,
                      indent=4)

    def _load_file_config(self, *args, **kwargs):
        """
        Load configuration data from file. Method may be overridden with a different signature.
        :return: loaded configuration data as an OrderedDict()
        """
        config_value = getattr(self, APPDATA)
        path_value = config_value.AbsolutePaths[0]
        default_cfg_file = os.path.join(path_value, CONFIG_FILE_NAME)
        config_base = None
        if os.path.exists(default_cfg_file):
            config_base = json.load(open(default_cfg_file.lower(), mode='r'), object_hook=ConfigEncoder.class_mapper)
        if config_base is None or self._current_dcc not in config_base:
            self.SaveConfig()
            config_base = type(self)._CURRENT_CONFIG
        return config_base

    def SetPythonPaths(self):
        """
        Public method to set python paths from config data. March the current config. Find all ConfigPath objects of
        type python_path. Add all path values to the sitedir in Python.
        :return: None
        """
        _knownPaths = site._init_pathinfo()
        for name, value, junk in self._marchConfig():
            if isinstance(value, ConfigPath):
                if value.python_path:
                    for dirVal in value.Paths:
                        site.addsitedir(dirVal, _knownPaths)

    def SetEnvironmentVars(self):
        """
        Public method to set environment variables from config data.
        :return:
        """
        for name, value, section in self._marchConfig():
            fetch_name = self._get_param_name(name, section)
            self._set_env_prop(fetch_name, value)

    def _get_env_config(self):
        env_config = deep_update(OrderedDict(), self._default_config, punk=True)
        for name, value, section in self._marchConfig():
            fetch_name = self._get_param_name(name, section)
            val = self._get_env_prop(fetch_name, value)
            env_config[section][name] = val
        return env_config

    def _gettr_(self, name, section):
        return type(self)._CURRENT_CONFIG[section][name]

    def _settr_(self, v, name, section):
        type(self)._CURRENT_CONFIG[section][name] = v
        fetch_name = self._get_param_name(name, section)
        self._set_env_prop(fetch_name, v)

    def _deltr_(self, name, section):
        self._settr_(None, name, section)

    def _make_property(self, name, section):
        fetch_name = self._get_param_name(name, section)
        if not hasattr(self, fetch_name):
            setattr(type(self), fetch_name, property(fget=lambda self, nm=name, scn=section: self._gettr_(nm, scn),
                                                        fset=lambda self, v, nm=name, scn=section: self._settr_(v, nm, scn),
                                                        fdel=lambda self, nm=name, scn=section: self._gettr_(nm, scn),
                                                        doc="Property \'{}\' on \'{}\'".format(name, section)))

    def _generate_config_attributes(self):
        for name, value, section in self._marchConfig():
            self._make_property(name, section)

    def _set_env_prop(self, envName, pathVal):
        if isinstance(pathVal, ConfigPath):
            if pathVal.environment_variable:
                updateEnvironmentPath(envName, pathVal.Paths)

    def _get_env_prop(self, envName, pathVal):
        if isinstance(pathVal, ConfigPath):
            if pathVal.relative:
                pathVal_root = pathVal.Root
                newPathsVal = getEnvironmentPath(envName, root=pathVal_root)
                newVal = ConfigPath(paths=newPathsVal,
                                    flags=pathVal.toDict()['flags'])
            else:
                newPathsVal = getEnvironmentPath(envName)
                newVal = ConfigPath(paths=newPathsVal,
                                    flags=pathVal.toDict(forceAbsolute=True)['flags'])
        else:
            newVal = os.getenv(envName)
        return newVal





