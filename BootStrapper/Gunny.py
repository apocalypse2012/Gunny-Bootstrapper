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
Module Documentation: Bootstrapper/Gunny.py

This is a commandline interface for the toolchain bootstrapping. This is the main entry point for launching DCC tools and
pipeline utilities.

usage:  {StartMaya,StartMax,StartBlender,StartBFB,Pipeline_Loadout}
                                    ...
positional arguments:
  {StartMaya,StartMax,StartBlender,Pipeline_Loadout}
    StartMaya           Launch Maya with pipeline
    StartMax            Launch 3dsmax with pipeline
    StartBlender        Launch Blender with pipeline

optional arguments:
  -h, --help            show this help message and exit

"""

import argparse
import sys
import os
import site
import traceback

log_source = 'Gunny'
python_modules_lib = 'libs_gunny'


# -------------------------------------------------------------------------
def we_are_frozen():
    """Returns whether we are frozen via py2exe.
    This will affect how we find out where we are located."""

    return hasattr(sys, "frozen")
# -------------------------------------------------------------------------


# -------------------------------------------------------------------------
def module_path():
    """ This will get us the program's directory,
    even if we are frozen using py2exe."""

    if we_are_frozen():
        filePath = os.path.realpath(sys.executable)
        return os.path.dirname(unicode(filePath, sys.getfilesystemencoding()))
    filePath = os.path.realpath(__file__)
    return_path = os.path.dirname(filePath)
    return_path = os.path.dirname(unicode(return_path, sys.getfilesystemencoding())) # Getting Parent directory for SDK location of StartService.
    return return_path
# -------------------------------------------------------------------------


def get_all_subclasses(cls):
    """
    This function returns a list of all subclasses of the the given class. Will march the whole class hierarchy.
    :param cls: Class to inspect.
    :return: List of classes.
    """
    all_subclasses = []

    for subclass in cls.__subclasses__():
        all_subclasses.append(subclass)
        all_subclasses.extend(get_all_subclasses(subclass))

    return all_subclasses


# -------------------------------------------------------------------------
if __name__ == "__main__":
    # store known paths
    _knownPaths = site._init_pathinfo()

    # Get the location of 'this' script module
    setupLocation = module_path().encode(encoding='utf-8')
    pythonIncludePath = os.path.normpath(os.path.join(setupLocation, python_modules_lib))
    pythonIncludePath = os.path.realpath(pythonIncludePath)

    # verify pythonIncludePath exists and add it as a site dir
    if os.path.exists(pythonIncludePath):
        site.addsitedir(pythonIncludePath, _knownPaths)
        from libs_gunny import commands
        commands.util.Set_Executable(setupLocation)

        # set up argument parsing and options
        description='Start Service tool launcher.'
        parser = argparse.ArgumentParser(description)
        subparsers = parser.add_subparsers(dest='tools')

        try:
            # Get all classes that inheret from Command. Instantiate each command class with a subparser instance.
            # After parsing, the Parse args contains the validated launcher. Execute the launchers doCommand().
            baseToolLaunchClass = commands.baseCommand.Command
            for launchers in get_all_subclasses(baseToolLaunchClass):
                launchers(subparsers)
            args = parser.parse_args()
            launcher = args.func(args)
            retcode = launcher.doCommand()
            parser.exit(retcode)
        except Exception as err:
            print "~ {0}: Exit with: {1}".format(log_source, err)
            T, V, TB = sys.exc_info()
            print ''.join(traceback.format_exception(T,V,TB))
            parser.error("~ {0}: Unable to initialize all utilities...".format(log_source))


