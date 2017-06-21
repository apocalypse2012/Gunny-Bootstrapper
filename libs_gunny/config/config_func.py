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
Module Documentation: MpPy\mp_config\config_func.py

< document module here>
"""
import os
import re
import exceptions
import _winreg
from constants import *

FIND_PATH = re.compile(ur'([\w\:\\\w /]+\w+\.\w+|[\w\:\\\w /]+\w+)')


class RootNotFound(exceptions.RuntimeError):
    pass


# registry helpers
def getRegKeyVal(pathToKey, valToQuery, regView64):
    """
    For a given path and key, return a windows registry value. Allows you to check the value of any known registry entry.
    :param pathToKey: Windows Registry Path
    :param valToQuery: The Key whose value we are checking.
    :param regView64: Switch for 64 or 32 bit registry path.
    :return: The value of the queried registry key.
    """
    aReg = None
    aKey = None
    keyConst = None
    regVal = None

    if regView64 is '64bit':
        keyConst = _winreg.KEY_WOW64_64KEY
    else:
        keyConst = _winreg.KEY_WOW64_32KEY

    try:
        aReg = _winreg.ConnectRegistry(None, _winreg.HKEY_LOCAL_MACHINE)
        aKey = _winreg.OpenKey(aReg, pathToKey, 0, keyConst|_winreg.KEY_READ)
        regVal = _winreg.QueryValueEx(aKey, valToQuery)
    except:
        pass
    if aKey:
        _winreg.CloseKey(aKey)
    if aReg:
        _winreg.CloseKey(aReg)

    return regVal


def updateEnvironmentPath(envar, newpath):
    """
    Creates or adds a path string to an existing environment variable without damaging the existing path data.
    *This function assumes that the given environment variable takes path string values.
    :param envar: Environment variable to update.
    :param newpath: The new path to assign to the variable.
    :return: None
    """
    delimiter = ';'
    pathStr = os.getenv(envar)
    if not pathStr is None and delimiter in pathStr:
        pathList = set(pathStr.split(delimiter))
        pathList.update(set(newpath))
        pathStr = ';'.join(pathList)
    else:
        pathStr = newpath if isinstance(newpath, basestring) else ';'.join(newpath)
    os.environ[envar] = pathStr


def getEnvironmentPath(envar, root):
    """
    For the given environment variable, return all paths with the given root.
    :param envar: environment variable to query.
    :param root: common parent relative to all paths returned.
    :return: list of commonly rooted paths stored in the environment variable.
    """
    delimiter = ';'
    pathStr = os.getenv(envar)
    if isinstance(pathStr, (str, bytes)):
        if delimiter in pathStr:
            pathList = set(pathStr.split(delimiter))
            collected = set()
            for path in pathList:
                if root in path:
                    collected.add(path)
            return list(collected)
        else:
            if root in pathStr:
                return list(pathStr)
    return list()


def FindRootMarker(curr_path=os.path.dirname(__file__), file_marker = PIPELINEFOLDER_FILEMARKER):
    """
    Recursive function that traverses up directory tree from curr_path looking for a file of a given name matching the
    Marker string. If it finds the file it returns the directory path that contains the file.
    :param curr_path: The current path in the search loop. The default is the system path to this script file.
    :return: The path string for the location verified to contain the file.
    """

    if os.path.isfile(os.path.join(curr_path, file_marker)):
        return curr_path

    # get the parent of the curr directory
    parentPath = os.path.dirname(curr_path)

    # if there is no parent we have hit the drive root and didn't find the file
    if not parentPath:
        # check to see if we already didn't find this file
        raise RootNotFound('parentPath: {}, curr_path: {}'.format(parentPath, curr_path))

    return FindRootMarker(parentPath, file_marker)


def filterPath(value):
    """
    This function parses a string to find and existing path using regular expressions.
    :param value: String value to search.
    :return: Verified existing path string.
    """
    valueList = re.findall(FIND_PATH, value)
    for tex in valueList:
        if os.path.exists(tex):
            return tex
    return None


# Set in Config_Defaults
ENVAR_DEFAULTS = None

def GetEnvarDefaults(var):
    """ Get and return the value of var from either the system environment or the module global dictionary. This dictionary
    provides a simple way to decouple the getter implementation, basically like a function pointer, except these resolve
    to specific values at import time. Environment variables trump these defaults.
    :param var:
    :return: Some value for the variable, current or default.
    """
    var = str(var)
    val = os.getenv(var)
    if not val:
        val = ENVAR_DEFAULTS.get(var)
    if val is not None:
        val = os.path.expandvars(val)
    return val


def SetEnvarDefaults(root=None, envals=None):
    """
    Set Environment Variables for each default that is not already set with a value. Will not over-write. Must be safe
    to run at any time.
    :return: None
    """
    if not envals:
        global ENVAR_DEFAULTS
        envals = ENVAR_DEFAULTS
    if root and os.path.exists(root):
        os.environ[ENVAR_GUNNY_ROOT] = root
        envals[ENVAR_GUNNY_ROOT] = root
    else:
        raise ValueError("Root is not valid: {}".format(root))
    for var in envals.iterkeys():
        var = str(var)
        val = os.getenv(var)
        if not val:
            val = envals[var]
            if val is not None:
                os.environ[var] = os.path.expandvars(val)
