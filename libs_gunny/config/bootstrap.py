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
Module Documentation: MpPy\mp_config\environment_lib.py

< document module here>
"""

import exceptions
from constants import *
import config_func

class executableNotFound(exceptions.RuntimeError):
    pass

class BootstrapNotFound(exceptions.RuntimeError):
    pass

_FLAGS = [PYTHON_PATH_FLAG,
          ENV_VAR_FLAG,
          ABSOLUTE_PATH_FLAG,
          RELATIVE_PATH_FLAG,
          PROJECT_RELATIVE_FLAG,
          ROOT_PATH_FLAG]


def GetInstalledApp(app_config):
    """
    For a given application configuration, return a complete executable filepath.
    :param app_config:
    :return:
    """
    executables = set()
    env = app_config.GetAttrByStructName(ENV_PATH_INSTALL)
    location = config_func.GetEnvarDefaults(env)
    if location and os.path.exists(location):
        executables.add(location)

    rg_pth = app_config.GetAttrByStructName(REG_PATH_INSTALL)
    rg_loc = config_func.getRegKeyVal(rg_pth, app_config.GetAttrByStructName(REG_ENTRY_INSTALL), '64bit')
    path = config_func.filterPath(rg_loc[0])
    if not path:
        raise executableNotFound("Could not produce a valid executable from {}, located at {}".format(rg_pth, rg_loc))

    if os.path.isfile(path):
        path = os.path.dirname(path)
    if os.path.isdir(path):
        executables.add(path)
    filePathName = os.path.join(executables.pop(), app_config.GetAttrByStructName(EXECUTABLE_COMMAND))
    return filePathName


def GetBootStrapScript(app_config):
    filename = app_config.GetAttrByStructName(BOOTSTRAP_FILE)
    appConfigPath = app_config.GetAttrByStructName(APP_CONFIG_PATH)
    validPaths = list()
    for path in appConfigPath.Paths:
        if os.path.exists(os.path.join(path, filename)):
            validPaths.append(path)
    return validPaths


def BootstrapApp(app_config):
    pathsvar = app_config.GetAttrByStructName(BOOTSTRAP_TYPE)
    startPath = GetBootStrapScript(app_config)
    config_func.updateEnvironmentPath(pathsvar, startPath)
    new_env = os.environ.copy()
    dccRunTime = GetInstalledApp(app_config)
    return dccRunTime, new_env

