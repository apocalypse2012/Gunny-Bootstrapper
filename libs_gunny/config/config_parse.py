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

    def __init__(self):
        """
        Initialization of a new Config Parser object. This is responsible for defining and initializing the current
        configuration which is stored as a class variable. This insures that the configuration state follows a Borg
        pattern that is guaranteed to remain common to all instances.
        :param dcc_vers: This is an input to identify the application and Version of for Digital Content Creation.
        """
        self._dcc_indx = None
        if not Config_Parser._CURRENT_CONFIG:
            self._default_config = config_defaults.DEFAULT_CONFIGURATION
            deep_update(Config_Parser._CURRENT_CONFIG, self._default_config)

            self._persistent_config = self._load_file_config()
            deep_update(Config_Parser._CURRENT_CONFIG, self._persistent_config)

            self._environment_config = self._get_env_config()
            deep_update(Config_Parser._CURRENT_CONFIG, self._environment_config, clean=True)

            self._applied_config = self._get_applied_config()
            deep_update(Config_Parser._CURRENT_CONFIG, self._applied_config, clean=True)

            self._generate_config_attributes()
        else:
            self._generate_config_attributes()

    def _find_dcc_indx(self, guid):
        for idx, dcc in enumerate(self._CURRENT_CONFIG[DESC_CONFIG_DCC]):
            if dcc[APP_ID] == guid:
                return idx
        return None

    def Add_DCC_Config(self, config, force=False):
        if force or self._dcc_indx is None or self._find_dcc_indx(config[APP_ID]) is None:
            self._dcc_indx = len(self._CURRENT_CONFIG[DESC_CONFIG_DCC])
            self._CURRENT_CONFIG[DESC_CONFIG_DCC].append(config)
            self._generate_config_attributes()
            self.SaveConfig()
        return self._dcc_indx

    def _marchParams(self):
        """
        This private generator method marches the objects current config state data yielding the next attribute name,
        value, and the config section it belongs to.
        :return: Tuple of attribute name, value, and parent. Value must be a ConfigPath data type.
        """
        for section, parms in Config_Parser._CURRENT_CONFIG.iteritems():
            if section == DESC_CONFIG_DCC:
                if self._dcc_indx is None:
                    continue
                for name, value in parms[self._dcc_indx].iteritems():
                    if isinstance(value, ConfigPath):
                        yield (name, value, section)
            elif not ignorable(section):
                for name, value in parms.iteritems():
                    if isinstance(value, ConfigPath):
                        yield (name, value, section)

    def _marchConfig(self, config):
        """
        This private generator method takes an Ordered Dict of config data and marches the data structure. Each call
        yields the next tuple consisting of an attribute name, value, section, and potentially an index. This is used
        to identify that there is configuration data supported to match the DCC application and version.
        :param config: Ordered Dict of config data
        :return: Tuple of attribute name, value, parent, and index. Returns a valid index when matches the dcc version.
        """
        for section, contents in config.iteritems():
            if isinstance(contents, Mapping):
                for name, value in contents.iteritems():
                    if not ignorable(name):
                        yield (name, value, section)
            elif isinstance(contents, Sequence):
                if section == DESC_CONFIG_DCC and not self._dcc_indx is None:
                    dcc_value = contents[self._dcc_indx]
                    for name, value in dcc_value.iteritems():
                        if not ignorable(name):
                            yield (name, value, section)

    def SaveConfig(self):
        """
        Save the current configuration state.
        :return:
        """
        default_path = str(Config_Parser._CURRENT_CONFIG[DESC_CONFIG_GUNNY][ENVAR_APPDATA].Paths[0])
        default_cfg_file = os.path.join(default_path, CONFIG_FILE_NAME)
        temp_file = default_cfg_file + '.TEMP'
        if os.path.exists(default_cfg_file):
            json.dump(Config_Parser._CURRENT_CONFIG,
                      open(temp_file.lower(),
                           mode='w'),
                      cls=ConfigEncoder,
                      sort_keys=False,
                      indent=4)
            EnsureBackup(temp_file, default_cfg_file)
        else:
            if not os.path.isdir(default_path):
                os.mkdir(default_path)
            json.dump(Config_Parser._CURRENT_CONFIG,
                      open(default_cfg_file.lower(),
                           mode='w'),
                      cls=ConfigEncoder,
                      sort_keys=False,
                      indent=4)

    def _load_file_config(self):
        """
        Load configuration data from file.
        :return: loaded configuration data as an OrderedDict()
        """
        default_path = Config_Parser._CURRENT_CONFIG[DESC_CONFIG_GUNNY][ENVAR_APPDATA].Paths[0]
        default_cfg_file = os.path.join(default_path, CONFIG_FILE_NAME)
        if os.path.exists(default_cfg_file):
            config_base = json.load(open(default_cfg_file.lower(), mode='r'), object_hook=ConfigEncoder.class_mapper)
        else:
            self.SaveConfig()
            config_base = Config_Parser._CURRENT_CONFIG
        return config_base

    def SetPythonPaths(self):
        """
        Public method to set python paths from config data. March the current config. Find all ConfigPath objects of
        type python_path. Add all path values to the sitedir in Python.
        :return: None
        """
        _knownPaths = site._init_pathinfo()
        for name, value, junk in self._marchParams():
            if isinstance(value, ConfigPath):
                if value.python_path:
                    for dirVal in value.Paths:
                        site.addsitedir(dirVal, _knownPaths)

    def SetEnvironmentVars(self):
        """
        Public method to set environment variables from config data.
        :return:
        """
        for name, value, junk in self._marchParams():
            self._set_env_prop(name, value)

    def _get_env_config(self):
        env_config = deep_update({}, self._default_config, punk=True)
        for name, value, section in self._marchParams():
            val = self._get_env_prop(name, value)
            if section == DESC_CONFIG_DCC:
                if self._dcc_indx is None:
                    continue
                env_config[section][self._dcc_indx][name] = val
            else:
                env_config[section][name] = val
        return env_config

    def _get_applied_config(self):
        return deep_update({}, self._default_config, punk=True)

    def _gettr_(self, name, section):
        # No need to trap self._dcc_indx. No setters and getters defined when there is no dcc context. See _make_property.
        if section == DESC_CONFIG_DCC:
            return Config_Parser._CURRENT_CONFIG[section][self._dcc_indx][name]
        else:
            return Config_Parser._CURRENT_CONFIG[section][name]

    def _settr_(self, v, name, section):
        # No need to trap self._dcc_indx. No setters and getters defined when there is no dcc context. See _make_property.
        if section == DESC_CONFIG_DCC:
            Config_Parser._CURRENT_CONFIG[DESC_CONFIG_DCC][self._dcc_indx][name] = v
        else:
            Config_Parser._CURRENT_CONFIG[section][name] = v
        self._set_env_prop(name, v)

    def _make_property(self, name, section):
        if section == DESC_CONFIG_DCC and self._dcc_indx is None:
            # Do not make attributes for DCC app if there is no DCC context.
            return
        setattr(Config_Parser, name, property(fget=lambda self, nm=name, scn=section: self._gettr_(nm, scn),
                                              fset=lambda self, v, nm=name, scn=section: self._settr_(v, nm, scn),
                                              fdel=lambda self, nm=name, scn=section: self._gettr_(nm, scn)))

    def _generate_config_attributes(self):
        for name, value, section in self._marchConfig(Config_Parser._CURRENT_CONFIG):
            self._make_property(name, section)

    def _set_env_prop(self, envName, pathVal):
        if isinstance(pathVal, ConfigPath):
            if pathVal.environment_variable:
                updateEnvironmentPath(envName, pathVal.Paths)
        else:
            updateEnvironmentPath(envName, pathVal)

    def _get_env_prop(self, envName, pathVal):
        if isinstance(pathVal, ConfigPath):
            if pathVal.relative:
                pathVal_root = pathVal.Root
                newPathsVal = getEnvironmentPath(envName, root=pathVal_root)
                newVal = ConfigPath(paths=newPathsVal,
                                    flags=pathVal.toDict(forceAbsolute=True)['flags'])
            else:
                newPathsVal = getEnvironmentPath(envName)
                newVal = ConfigPath(paths=newPathsVal,
                                    flags=pathVal.toDict(forceAbsolute=True)['flags'])
        else:
            newVal = os.getenv(envName)
        return newVal





