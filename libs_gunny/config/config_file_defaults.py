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
Module Documentation: MpPy\mp_config\config_file_defaults.py

< document module here>
"""
from constants import *


USER_CONFIG_DEFAULTS = {
    COMMENT_QUALIFIER: ''.join(('_template keys will be ignored, these are examples.',
                                 'User can add additional sections/blocks with unique names,',
                                 ' this allows for setting up multiple roots.')),
    TEMPLATE_QUALIFIER:  (
        "example_value",
        "addEnv"
    ),
    TEMPLATE_QUALIFIER+'1': (
        "c:\\absolute\\example\\path",
        "addPySiteDir"
    ),
    TEMPLATE_QUALIFIER+'2': (
        "c:\\example\\rootpath",
        "root",
        "addEnv",
        "addSysPath"
    ),
    TEMPLATE_QUALIFIER+'3': (
        "another\\path\\example",
        "relative",
        "setEnv",
        "setSysPath"
    )
}

INFO_CONFIG_COMMENT = ''.join(('This info section is protected.',
                                ' These Key:Value pairs are generated every time the file',
                                ' is written. Any changes will be ignored/purged when',
                                ' Config is read from disk!'))

PROPERTIES_CONFIG_COMMENT = ''.join(('This Properties section is not protected.',
                                      ' If a Value is changed, when the config is read it will',
                                      ' be set to that.',
                                      ' _WINGHOME is an absolute path for wing install location.',
                                      ' Key:Value pairs may be added by User for use with Config.',
                                      ' Any Key starting with _template is ignored, it is',
                                      ' used here as an example of adding User Properties.'))

MAX_PLAY_CONFIG_COMMENT = ''.join(('First non _comment entry in the block should be the',
                                    ' ROOT path for the block. All paths in this block share',
                                    ' the common root MP_ROOT... unless you mark the path as',
                                    ' absolute.  By default we do not dump MP_ROOT here.',
                                    ' We store the MP_ROOT in the info section, each time',
                                    ' the config is generated (so we know where you were',
                                    ' running from) however if you DO include a MP_ROOT',
                                    ' definition in this MaxPlay section - we will use that',
                                    ' to override the MP_ROOT before continuing the boostrap.',
                                    ' The defaults here are already added to the',
                                    ' environment, it is recommended to not remove the addEnv,',
                                    ' for these existing defaults.',
                                    ' If adding new paths, you can set the flags:',
                                    ' root/absolute/relative ...',
                                    ' and if you include the addEnv those Key:path values',
                                    ' will be added to the environment as well',
                                    ' Flags: addEnv will add the Key:Value to the environment,',
                                    ' setEnv will set and persist in user environment -',
                                    ' (currently not supported),',
                                    ' addSysPath will add the path to sys.path,',
                                    ' setSysPath will set and persist the path in the os -',
                                    ' (currently not supported),',
                                    ' addPySiteDir will add the path as a python sitedir'))

GUNNY_CONFIG_TEMPLATE1 = ("c:\\example\\path",
                              "absolute",
                              "addEnv",
                              "addSysPath",
                              "addPySiteDir")

GUNNY_CONFIG_TEMPLATE2 = ("another\\path\\example",
                              "relative",
                              "addEnv",
                              "addSysPath",
                              "addPySiteDir")

