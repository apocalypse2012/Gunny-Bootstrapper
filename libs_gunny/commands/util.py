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
PackageDocumentation: util

Helpers for start service
"""

import ctypes
import os
import sys
import traceback

GUNNY_ENTRYPOINT_PATH = None


def Set_Executable(start_path):
    global GUNNY_ENTRYPOINT_PATH
    GUNNY_ENTRYPOINT_PATH = start_path


def islink_ms(path):
    """
    detect if a directory is a symlink on Windows
    :param path:
    :return:
    """
    FILE_ATTRIBUTE_REPARSE_POINT = 0x0400

    if os.path.isdir(path) and \
            (ctypes.windll.kernel32.GetFileAttributesW(unicode(path)) & FILE_ATTRIBUTE_REPARSE_POINT):
        return True
    else:
        return False


def symlink_ms(source, link_name):
    """
    this script makes a link under windows if the user has a privilage to do so, otherwise it just doesn't make a link
    :param source:
    :param link_name:
    :return:
    """
    csl = ctypes.windll.kernel32.CreateSymbolicLinkW
    csl.argtypes = (ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_uint32)
    csl.restype = ctypes.c_ubyte
    flags = 1 if os.path.isdir(source) else 0
    try:
        if csl(link_name, source.replace('/', '\\'), flags) == 0:
            raise ctypes.WinError()
    except Exception as err:
        print "~ {0}: Exit with: {1}".format(__file__, err)
        T, V, TB = sys.exc_info()
        print ''.join(traceback.format_exception(T,V,TB))

