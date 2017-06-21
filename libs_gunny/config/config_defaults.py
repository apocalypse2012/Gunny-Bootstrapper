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
Module Documentation: MpPy\mp_config\config.py

Data descriptions and defaults for toolchain configuration. These are the building block of a configuration used for
various pipeline tools. We build these up using special collections objects: NamedTuple and OrderedDict.
We use namedtuple to create a type-like template object of a given spec (a dict of names and default values). These 
template objects can then be loaded with data for each respective attribute and cast to an orderedDict. These steps 
provide an abstraction for defaults, custom state data, and consistent serialization order.
"""

import sys
from collections import namedtuple
import config_file_defaults as defaults
import config_func
from config_marshall import ValidEnvars, ConfigPath, ConfigEncoder
from constants import *

CONFIG_VERSION = 1
JSON_ENCODER_SPEC = ConfigEncoder()


ENVAR_VALUES = {ENVAR_GUNNY_ROOT: config_func.FindRootMarker(__file__),
                ENVAR_TOOLS_PATH: '$' + ENVAR_GUNNY_ROOT + '\\' + 'tools',
                ENVAR_DCC_PATH: '$' + ENVAR_GUNNY_ROOT + '\\' + 'DCC',
                ENVAR_PY_PACKAGES_PATH: '$' + ENVAR_GUNNY_ROOT + '\\libs_gunny',
                ENVAR_PY_PACKAGES_3RDPARTY_PATH: '$' + ENVAR_GUNNY_ROOT + '\\libs_thirdparty\\native_2x',
                ENVAR_APPDATA: '%APPDATA%' + '\\' + 'Gunny'
                }
ENVAR_TYPE = namedtuple('ENVAR_TYPE', (ENVAR_GUNNY_ROOT, ENVAR_TOOLS_PATH, ENVAR_DCC_PATH, ENVAR_PY_PACKAGES_PATH,
                                       ENVAR_PY_PACKAGES_3RDPARTY_PATH, ENVAR_APPDATA))
config_func.ENVAR_DEFAULTS = CONFIG_ENVAR = ENVAR_TYPE(**ENVAR_VALUES)._asdict()
JSON_ENCODER_SPEC.add_mapping(ENVAR_TYPE)


# Shared state for Configuration.
CONFIG_INFO_DEFAULT = {
    COMMENT_QUALIFIER: defaults.INFO_CONFIG_COMMENT,
    ENVAR_COMPANY: 'GUNNY',
    'configVer': CONFIG_VERSION,
    'executable': sys.executable,
    'pyVersion': str(sys.version_info),
    'pyInstall': sys.exec_prefix,
    'platform': sys.platform,
    'osDataPath': ValidEnvars(ENVAR_APPDATA)
}
CONFIG_INFO_TYPE = namedtuple(CONFIG_INFO_TYPENAME, (COMMENT_QUALIFIER, ENVAR_COMPANY, 'configVer',
                                                   'executable', 'pyVersion', 'pyInstall', 'platform', 'osDataPath'))
CONFIG_INFO = CONFIG_INFO_TYPE(**CONFIG_INFO_DEFAULT)._asdict()
JSON_ENCODER_SPEC.add_mapping(CONFIG_INFO_TYPE)


CONFIG_GUNNY_DEFAULT = {
    COMMENT_QUALIFIER: defaults.MAX_PLAY_CONFIG_COMMENT,
    ENVAR_APPDATA: ConfigPath(paths=[ValidEnvars(ENVAR_APPDATA), ], flags=[
                               ABSOLUTE_PATH_FLAG]),
    ENVAR_GUNNY_ROOT: ConfigPath(paths=[ValidEnvars(ENVAR_GUNNY_ROOT), ], flags=[
                               ABSOLUTE_PATH_FLAG]),
    ENVAR_TOOLS_PATH: ConfigPath(paths=[ValidEnvars(ENVAR_TOOLS_PATH), ], flags=[
                               ABSOLUTE_PATH_FLAG,
                               ENV_VAR_FLAG]),
    ENVAR_PY_PACKAGES_PATH: ConfigPath(paths=[ValidEnvars(ENVAR_PY_PACKAGES_PATH), ], flags=[
                                     ABSOLUTE_PATH_FLAG,
                                     ENV_VAR_FLAG,
                                     PYTHON_PATH_FLAG]),
    ENVAR_PY_PACKAGES_3RDPARTY_PATH: ConfigPath(paths=[ValidEnvars(ENVAR_PY_PACKAGES_3RDPARTY_PATH), ], flags=[
                                              ABSOLUTE_PATH_FLAG,
                                              ENV_VAR_FLAG,
                                              PYTHON_PATH_FLAG]),
    TEMPLATE_QUALIFIER+str('1'): defaults.GUNNY_CONFIG_TEMPLATE1,
    TEMPLATE_QUALIFIER+str('2'): defaults.GUNNY_CONFIG_TEMPLATE2
}
CONFIG_GUNNY_TYPE = namedtuple(CONFIG_GUNNY_TYPENAME, (COMMENT_QUALIFIER, ENVAR_APPDATA, ENVAR_GUNNY_ROOT, ENVAR_TOOLS_PATH,
                                                       ENVAR_PY_PACKAGES_PATH, ENVAR_PY_PACKAGES_3RDPARTY_PATH,
                                                       TEMPLATE_QUALIFIER + str('1'), TEMPLATE_QUALIFIER + str('2')))
CONFIG_GUNNY = CONFIG_GUNNY_TYPE(**CONFIG_GUNNY_DEFAULT)._asdict()
JSON_ENCODER_SPEC.add_mapping(CONFIG_GUNNY_TYPE)


CONFIG_DCC_TYPE = namedtuple(CONFIG_DCC_TYPENAME, (APP_ID, DESC_CONFIG_DCC, APP_VERSION, EXECUTABLE_COMMAND, BOOTSTRAP_TYPE,
                                                 BOOTSTRAP_FILE, REG_ENTRY_INSTALL, REG_PATH_INSTALL, ENV_PATH_INSTALL,
                                                 APP_ROOT_TYPE, APP_CONFIG_PATH, APP_PY_PACKAGES))
JSON_ENCODER_SPEC.add_mapping(CONFIG_DCC_TYPE)


CONFIG_MAYA_2017_DEFAULT= {
    APP_ID: None,
    DESC_CONFIG_DCC: DESC_CONFIG_MAYA,
    APP_VERSION: STR_2017,
    EXECUTABLE_COMMAND: MAYA_RELATIVE_EXE_PATH,
    BOOTSTRAP_TYPE: PYTHON_PATH,
    BOOTSTRAP_FILE: MAYA_SETUP_FILE,
    REG_ENTRY_INSTALL: MAYA_REG_KEY,
    REG_PATH_INSTALL: MAYA_REG_PATH_2017,
    ENV_PATH_INSTALL: MAYA_ENV_PATH,
    APP_ROOT_TYPE: ENVAR_DCC_PATH,
    APP_CONFIG_PATH: ConfigPath(paths=[MAYA_PATH_SCRIPTS],
                                flags=[RELATIVE_PATH_FLAG]),
    APP_PY_PACKAGES: ConfigPath(paths=[DIR_MAYA],
                                flags=[ENVAR_DCC_PATH,
                                       RELATIVE_PATH_FLAG,
                                       PYTHON_PATH_FLAG]),
    MAYA_SCRIPT_PATH: ConfigPath(paths=[MAYA_PATH_SCRIPTS_2017,
                                        MAYA_PATH_MEL_2017,
                                        MAYA_PATH_PYTHON_2017,
                                        MAYA_PATH_SCRIPTS,
                                        MAYA_PATH_MEL,
                                        MAYA_PATH_PYTHON],
                                   flags=[ENVAR_DCC_PATH,
                                          RELATIVE_PATH_FLAG,
                                          ENV_VAR_FLAG,
                                          PYTHON_PATH_FLAG]),
    XBMLANG_PATH: ConfigPath(paths=[MAYA_PATH_ICONS],
                              flags=[ENVAR_DCC_PATH,
                                     RELATIVE_PATH_FLAG,
                                     ENV_VAR_FLAG]),
    MAYA_PLUG_IN_PATH: ConfigPath(paths=[MAYA_PATH_PLUGINS_2017],
                                    flags=[ENVAR_DCC_PATH,
                                           RELATIVE_PATH_FLAG,
                                           ENV_VAR_FLAG])
}
CONFIG_MAYA_TYPE = namedtuple(CONFIG_MAYA_TYPENAME, CONFIG_DCC_TYPE._fields+(MAYA_SCRIPT_PATH, XBMLANG_PATH,
                                                                           MAYA_PLUG_IN_PATH))
CONFIG_MAYA_2017 = CONFIG_MAYA_TYPE(**CONFIG_MAYA_2017_DEFAULT)._asdict()
JSON_ENCODER_SPEC.add_mapping(CONFIG_MAYA_TYPE)

"""
CONFIG_MAYA_2016_DEFAULT= {
    APP_ID: None,
    DESC_CONFIG_DCC: DESC_CONFIG_MAYA,
    APP_VERSION: STR_2016,
    EXECUTABLE_COMMAND: MAYA_RELATIVE_EXE_PATH,
    BOOTSTRAP_TYPE: PYTHON_PATH,
    BOOTSTRAP_FILE: MAYA_SETUP_FILE,
    REG_ENTRY_INSTALL: MAYA_REG_KEY,
    REG_PATH_INSTALL: MAYA_REG_PATH_2016,
    ENV_PATH_INSTALL: MAYA_ENV_PATH,
    APP_ROOT_TYPE: ENVAR_DCC_PATH,
    APP_CONFIG_PATH: ConfigPath(paths=[MAYA_PATH_SCRIPTS],
                                flags=[RELATIVE_PATH_FLAG]),
    APP_PY_PACKAGES: ConfigPath(paths=[DIR_MAYA],
                                flags=[ENVAR_DCC_PATH,
                                       RELATIVE_PATH_FLAG,
                                       PYTHON_PATH_FLAG]),
    MAYA_SCRIPT_PATH: ConfigPath(paths=[MAYA_PATH_SCRIPTS_2016,
                                        MAYA_PATH_MEL_2016,
                                        MAYA_PATH_PYTHON_2016,
                                        MAYA_PATH_SCRIPTS,
                                        MAYA_PATH_MEL,
                                        MAYA_PATH_PYTHON],
                                   flags=[ENVAR_DCC_PATH,
                                          RELATIVE_PATH_FLAG,
                                          ENV_VAR_FLAG,
                                          PYTHON_PATH_FLAG]),
    XBMLANG_PATH: ConfigPath(paths=[MAYA_PATH_ICONS],
                              flags=[ENVAR_DCC_PATH,
                                     RELATIVE_PATH_FLAG,
                                     ENV_VAR_FLAG]),
    MAYA_PLUG_IN_PATH: ConfigPath(paths=[MAYA_PATH_PLUGINS_2016],
                                    flags=[ENVAR_DCC_PATH,
                                           RELATIVE_PATH_FLAG,
                                           ENV_VAR_FLAG])
}
CONFIG_MAYA_TYPE = namedtuple(CONFIG_MAYA_TYPENAME, CONFIG_DCC_TYPE._fields+(MAYA_SCRIPT_PATH, XBMLANG_PATH,
                                                                           MAYA_PLUG_IN_PATH))
CONFIG_MAYA_2016 = CONFIG_MAYA_TYPE(**CONFIG_MAYA_2016_DEFAULT)._asdict()


CONFIG_MAYAPY_2016_DEFAULT = {
    APP_ID: None,
    DESC_CONFIG_DCC: DESC_CONFIG_MAYAPY,
    APP_VERSION: STR_2016,
    EXECUTABLE_COMMAND: MAYAPY_RELATIVE_EXE_PATH,
    BOOTSTRAP_TYPE: PYTHON_PATH,
    BOOTSTRAP_FILE: MAYA_SETUP_FILE,
    REG_ENTRY_INSTALL: MAYA_REG_KEY,
    REG_PATH_INSTALL: MAYA_REG_PATH,
    ENV_PATH_INSTALL: MAYA_ENV_PATH,
    APP_ROOT_TYPE: ENVAR_DCC_PATH,
    APP_CONFIG_PATH: ConfigPath(paths=[MAYA_PATH_SCRIPTS],
                                flags=[RELATIVE_PATH_FLAG]),
    APP_PY_PACKAGES: ConfigPath(paths=[DIR_MAYA],
                                flags=[ENVAR_DCC_PATH,
                                       RELATIVE_PATH_FLAG,
                                       PYTHON_PATH_FLAG]),
    MAYA_SCRIPT_PATH: ConfigPath(paths=[MAYA_PATH_SCRIPTS_2016,
                                        MAYA_PATH_MEL_2016,
                                        MAYA_PATH_PYTHON_2016,
                                        MAYA_PATH_SCRIPTS,
                                        MAYA_PATH_MEL,
                                        MAYA_PATH_PYTHON],
                                   flags=[ENVAR_DCC_PATH,
                                          RELATIVE_PATH_FLAG,
                                          ENV_VAR_FLAG,
                                          PYTHON_PATH_FLAG]),
    XBMLANG_PATH: ConfigPath(paths=[MAYA_PATH_ICONS],
                              flags=[ENVAR_DCC_PATH,
                                     RELATIVE_PATH_FLAG,
                                     ENV_VAR_FLAG]),
    MAYA_PLUG_IN_PATH: ConfigPath(paths=[MAYA_PATH_PLUGINS_2016],
                                    flags=[ENVAR_DCC_PATH,
                                           RELATIVE_PATH_FLAG,
                                           ENV_VAR_FLAG])
}
CONFIG_MAYAPY_2016 = CONFIG_MAYA_TYPE(**CONFIG_MAYAPY_2016_DEFAULT)._asdict()


CONFIG_MAYA_2015_DEFAULT= {
    APP_ID: None,
    DESC_CONFIG_DCC: DESC_CONFIG_MAYA,
    APP_VERSION: '2015',
    EXECUTABLE_COMMAND: 'bin\\maya.exe',
    BOOTSTRAP_TYPE: "PYTHONPATH",
    BOOTSTRAP_FILE: "userSetup.py",
    REG_ENTRY_INSTALL: 'MAYA_INSTALL_LOCATION',
    REG_PATH_INSTALL: 'SOFTWARE\\Autodesk\\Maya\\2015\\Setup\\InstallPath',
    ENV_PATH_INSTALL: 'MAYA_LOCATION',
    APP_ROOT_TYPE: ENVAR_DCC_PATH,
    APP_CONFIG_PATH: ConfigPath(paths=["Maya\\scripts"],
                                flags=[ENVAR_DCC_PATH,
                                       RELATIVE_PATH_FLAG]),
    APP_PY_PACKAGES: ConfigPath(paths=["Maya"],
                                flags=[ENVAR_DCC_PATH,
                                       RELATIVE_PATH_FLAG,
                                       PYTHON_PATH_FLAG]),
    "MAYA_SCRIPT_PATH": ConfigPath(paths=["Maya\\scripts"],
                                   flags=[ENVAR_DCC_PATH,
                                          RELATIVE_PATH_FLAG,
                                          ENV_VAR_FLAG]),
    "XBMLANGPATH": ConfigPath(paths=["Maya\\icons"],
                              flags=[ENVAR_DCC_PATH,
                                     RELATIVE_PATH_FLAG,
                                     ENV_VAR_FLAG]),
    "MAYA_PLUG_IN_PATH": ConfigPath(paths=["Maya\\2015\\plugins"],
                                    flags=[ENVAR_DCC_PATH,
                                           RELATIVE_PATH_FLAG,
                                           ENV_VAR_FLAG])
}
CONFIG_MAYA_2015 = CONFIG_MAYA_TYPE(**CONFIG_MAYA_2015_DEFAULT)._asdict()


CONFIG_MAYA_2014_DEFAULT= {
    APP_ID: None,
    DESC_CONFIG_DCC: DESC_CONFIG_MAYA,
    APP_VERSION: '2014',
    EXECUTABLE_COMMAND: 'bin\\maya.exe',
    BOOTSTRAP_TYPE: "PYTHONPATH",
    BOOTSTRAP_FILE: "userSetup.py",
    REG_ENTRY_INSTALL: 'MAYA_INSTALL_LOCATION',
    REG_PATH_INSTALL: 'SOFTWARE\\Autodesk\\Maya\\2014\\Setup\\InstallPath',
    ENV_PATH_INSTALL: 'MAYA_LOCATION',
    APP_ROOT_TYPE: ENVAR_DCC_PATH,
    APP_CONFIG_PATH: ConfigPath(paths=["Maya\\scripts"],
                                flags=[ENVAR_DCC_PATH,
                                       RELATIVE_PATH_FLAG]),
    APP_PY_PACKAGES: ConfigPath(paths=["Maya"],
                                flags=[ENVAR_DCC_PATH,
                                       RELATIVE_PATH_FLAG,
                                       PYTHON_PATH_FLAG]),
    "MAYA_SCRIPT_PATH": ConfigPath(paths=["Maya\\scripts"],
                                   flags=[ENVAR_DCC_PATH,
                                          RELATIVE_PATH_FLAG,
                                          ENV_VAR_FLAG]),
    "XBMLANGPATH": ConfigPath(paths=["Maya\\icons"],
                              flags=[ENVAR_DCC_PATH,
                                     RELATIVE_PATH_FLAG,
                                     ENV_VAR_FLAG]),
    "MAYA_PLUG_IN_PATH": ConfigPath(paths=["Maya\\2014\\plugins"],
                                    flags=[ENVAR_DCC_PATH,
                                           RELATIVE_PATH_FLAG,
                                           ENV_VAR_FLAG])
}
CONFIG_MAYA_2014 = CONFIG_MAYA_TYPE(**CONFIG_MAYA_2014_DEFAULT)._asdict()
"""

CONFIG_3DSMAX_2018_DEFAULT = {
    APP_ID: None,
    DESC_CONFIG_DCC: DESC_CONFIG_3DSMAX,
    APP_VERSION: '20000',
    EXECUTABLE_COMMAND: '3dsmax.exe -U PythonHost startup.py',
    BOOTSTRAP_TYPE: "path",
    BOOTSTRAP_FILE: "startup.ms",
    REG_ENTRY_INSTALL: 'Installdir',
    REG_PATH_INSTALL: 'SOFTWARE\\Autodesk\\3dsMax\\20.0',
    ENV_PATH_INSTALL: 'ADSK_3DSMAX_X64_2018',
    APP_ROOT_TYPE: ENVAR_DCC_PATH,
    APP_CONFIG_PATH: ConfigPath(paths=["Max\\scripts",
                                       "Max\\2018\\scripts"],
                                flags=[ENVAR_DCC_PATH,
                                       RELATIVE_PATH_FLAG]),
    APP_PY_PACKAGES: ConfigPath(paths=["Max",
                                       "Max\\2018"],
                                flags=[ENVAR_DCC_PATH,
                                       RELATIVE_PATH_FLAG,
                                       PYTHON_PATH_FLAG]),
    MAX_PLUGIN_PATH: ConfigPath(paths=["Max\\2018\\plugins"],
                                     flags=[ENVAR_DCC_PATH,
                                            RELATIVE_PATH_FLAG,
                                            ENV_VAR_FLAG])
}
CONFIG_3DSMAX_TYPE = namedtuple(CONFIG_3DSMAX_TYPENAME, CONFIG_DCC_TYPE._fields+(MAX_PLUGIN_PATH,))
CONFIG_3DSMAX_2018 = CONFIG_3DSMAX_TYPE(**CONFIG_3DSMAX_2018_DEFAULT)._asdict()
JSON_ENCODER_SPEC.add_mapping(CONFIG_3DSMAX_TYPE)


"""
CONFIG_3DSMAX_2016_DEFAULT = {
    APP_ID: None,
    DESC_CONFIG_DCC: DESC_CONFIG_3DSMAX,
    APP_VERSION: '18000',
    EXECUTABLE_COMMAND: '3dsmax.exe -U PythonHost startup.py',
    BOOTSTRAP_TYPE: "path",
    BOOTSTRAP_FILE: "startup.ms",
    REG_ENTRY_INSTALL: 'Installdir',
    REG_PATH_INSTALL: 'SOFTWARE\\Autodesk\\3dsMax\\18.0',
    ENV_PATH_INSTALL: 'ADSK_3DSMAX_X64_2016',
    APP_ROOT_TYPE: ENVAR_DCC_PATH,
    APP_CONFIG_PATH: ConfigPath(paths=["Max\\scripts",
                                       "Max\\2016\\scripts"],
                                flags=[ENVAR_DCC_PATH,
                                       RELATIVE_PATH_FLAG]),
    APP_PY_PACKAGES: ConfigPath(paths=["Max",
                                       "Max\\2016"],
                                flags=[ENVAR_DCC_PATH,
                                       RELATIVE_PATH_FLAG,
                                       PYTHON_PATH_FLAG]),
    MAX_PLUGIN_PATH: ConfigPath(paths=["Max\\2016\\plugins"],
                                     flags=[ENVAR_DCC_PATH,
                                            RELATIVE_PATH_FLAG,
                                            ENV_VAR_FLAG])
}
CONFIG_3DSMAX_TYPE = namedtuple(CONFIG_3DSMAX_TYPENAME, CONFIG_DCC_TYPE._fields+(MAX_PLUGIN_PATH,))
CONFIG_3DSMAX_2016 = CONFIG_3DSMAX_TYPE(**CONFIG_3DSMAX_2016_DEFAULT)._asdict()


CONFIG_3DSMAX_2015_DEFAULT = {
    APP_ID: None,
    DESC_CONFIG_DCC: DESC_CONFIG_3DSMAX,
    APP_VERSION: '17000',
    EXECUTABLE_COMMAND: '3dsmax.exe -U PythonHost startup.py',
    BOOTSTRAP_TYPE: "path",
    BOOTSTRAP_FILE: "startup.ms",
    REG_ENTRY_INSTALL: 'Installdir',
    REG_PATH_INSTALL: 'SOFTWARE\\Autodesk\\3dsMax\\17.0',
    ENV_PATH_INSTALL: 'ADSK_3DSMAX_X64_2015',
    APP_ROOT_TYPE: ENVAR_DCC_PATH,
    APP_CONFIG_PATH: ConfigPath(paths=["Max\\scripts"],
                                flags=[ENVAR_DCC_PATH,
                                       RELATIVE_PATH_FLAG]),
    APP_PY_PACKAGES: ConfigPath(paths=["Max,Max\\2015"],
                                flags=[ENVAR_DCC_PATH,
                                       RELATIVE_PATH_FLAG,
                                       PYTHON_PATH_FLAG]),
    "MAX_PLUGIN_PATH": ConfigPath(paths=["Max\\2015\\plugins"],
                                  flags=[ENVAR_DCC_PATH,
                                         RELATIVE_PATH_FLAG,
                                         ENV_VAR_FLAG])
}
CONFIG_3DSMAX_2015 = CONFIG_3DSMAX_TYPE(**CONFIG_3DSMAX_2015_DEFAULT)._asdict()
"""

CONFIG_BLENDER_DEFAULT = {
    APP_ID: None,
    DESC_CONFIG_DCC: DESC_CONFIG_BLENDER,
    APP_VERSION: '',
    EXECUTABLE_COMMAND: 'blender.exe',
    BOOTSTRAP_TYPE: "BLENDER_USER_SCRIPTS",
    BOOTSTRAP_FILE: "startup\\startup.py",
    REG_ENTRY_INSTALL: '',
    REG_PATH_INSTALL: 'SOFTWARE\\Classes\\blendfile\\shell\\open\\command',
    ENV_PATH_INSTALL: '',
    APP_ROOT_TYPE: ENVAR_DCC_PATH,
    APP_CONFIG_PATH: ConfigPath(paths=["Blender\\scripts"],
                                flags=[ENVAR_DCC_PATH,
                                       RELATIVE_PATH_FLAG]),
    APP_PY_PACKAGES: ConfigPath(paths=["Blender"],
                                flags=[ENVAR_DCC_PATH,
                                       RELATIVE_PATH_FLAG,
                                       PYTHON_PATH_FLAG])
}
CONFIG_BLENDER = CONFIG_DCC_TYPE(**CONFIG_BLENDER_DEFAULT)._asdict()


# CONFIG_USER_DEFAULTS = defaults.USER_CONFIG_DEFAULTS
# CONFIG_USER_TYPE = namedtuple('CONFIG_USER_TYPE', (COMMENT_QUALIFIER, TEMPLATE_QUALIFIER, TEMPLATE_QUALIFIER+'1',
#                                                        TEMPLATE_QUALIFIER+'2', TEMPLATE_QUALIFIER+'3'))
# CONFIG_USER = CONFIG_USER_TYPE(**CONFIG_USER_DEFAULTS)._asdict()


CONFIGURATION_DEFAULT = {DESC_ENVAR: CONFIG_ENVAR,
                         DESC_CONFIG_INFO: CONFIG_INFO,
                         DESC_CONFIG_GUNNY: CONFIG_GUNNY,
                         DESC_CONFIG_DCC: [CONFIG_MAYA_2017,
                                           CONFIG_3DSMAX_2018,
                                           CONFIG_BLENDER]
                         }
CONFIGURATION_TYPE = namedtuple(CONFIG_DATA_TYPENAME, (DESC_ENVAR, DESC_CONFIG_INFO, DESC_CONFIG_GUNNY, DESC_CONFIG_DCC))
DEFAULT_CONFIGURATION = CONFIGURATION_TYPE(**CONFIGURATION_DEFAULT)._asdict()
JSON_ENCODER_SPEC.add_mapping(CONFIGURATION_TYPE)

