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

############
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


############ Shared state for Configuration.
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


############
CONFIG_GUNNY_DEFAULT = {
    COMMENT_QUALIFIER: defaults.MAX_PLAY_CONFIG_COMMENT,
    APPDATA: ConfigPath(paths=["", ],
                        flags=[ENVAR_APPDATA,
                               RELATIVE_PATH_FLAG, ]),
    GUNNY_ROOT: ConfigPath(paths=["", ],
                           flags=[ENVAR_GUNNY_ROOT,
                                  RELATIVE_PATH_FLAG, ]),
    TOOLS_PATH: ConfigPath(paths=["", ],
                           flags=[ENVAR_TOOLS_PATH,
                                  RELATIVE_PATH_FLAG, ]),
    PY_PACKAGES_PATH: ConfigPath(paths=["", ],
                                 flags=[ENVAR_PY_PACKAGES_PATH,
                                        RELATIVE_PATH_FLAG,
                                        PYTHON_PATH_FLAG]),
    PY_PACKAGES_3RDPARTY_PATH: ConfigPath(paths=["", ],
                                          flags=[ENVAR_PY_PACKAGES_3RDPARTY_PATH,
                                                 RELATIVE_PATH_FLAG,
                                                 PYTHON_PATH_FLAG]),
    TEMPLATE_QUALIFIER+str('1'): defaults.GUNNY_CONFIG_TEMPLATE1,
    TEMPLATE_QUALIFIER+str('2'): defaults.GUNNY_CONFIG_TEMPLATE2
}
CONFIG_GUNNY_TYPE = namedtuple(CONFIG_GUNNY_TYPENAME, (COMMENT_QUALIFIER, APPDATA, GUNNY_ROOT, TOOLS_PATH,
                                                       PY_PACKAGES_PATH, PY_PACKAGES_3RDPARTY_PATH,
                                                       TEMPLATE_QUALIFIER + str('1'), TEMPLATE_QUALIFIER + str('2')))
CONFIG_GUNNY = CONFIG_GUNNY_TYPE(**CONFIG_GUNNY_DEFAULT)._asdict()
JSON_ENCODER_SPEC.add_mapping(CONFIG_GUNNY_TYPE)


############
CONFIG_DCC_TYPE = namedtuple(CONFIG_DCC_TYPENAME, (APP_ID, DESC_CONFIG_DCC, APP_VERSION, EXECUTABLE_COMMAND, BOOTSTRAP_TYPE,
                                                 BOOTSTRAP_FILE, REG_ENTRY_INSTALL, REG_PATH_INSTALL, ENV_PATH_INSTALL,
                                                 APP_ROOT_TYPE, APP_CONFIG_PATH, APP_PY_PACKAGES))
JSON_ENCODER_SPEC.add_mapping(CONFIG_DCC_TYPE)


############
CONFIG_MAYA_TYPE = namedtuple(CONFIG_MAYA_TYPENAME, CONFIG_DCC_TYPE._fields+(MAYA_SCRIPT_PATH, XBMLANG_PATH, MAYA_PLUG_IN_PATH))
JSON_ENCODER_SPEC.add_mapping(CONFIG_MAYA_TYPE)


############
CONFIG_3DSMAX_TYPE = namedtuple(CONFIG_3DSMAX_TYPENAME, CONFIG_DCC_TYPE._fields+(MAX_PLUGIN_PATH,))
JSON_ENCODER_SPEC.add_mapping(CONFIG_3DSMAX_TYPE)



############
CONFIG_3DSMAX_2018_DEFAULT = {
    APP_ID: 'b4d31e56-5b75-4020-9474-b5fcb1c6c7e7',
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
CONFIG_3DSMAX = CONFIG_3DSMAX_TYPE(**CONFIG_3DSMAX_2018_DEFAULT)._asdict()


############
CONFIG_MAYA_2017_DEFAULT= {
    APP_ID: 'a5472549-704d-4505-a50d-ef3baeee87b2',
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
                                flags=[ENVAR_DCC_PATH,
                                       RELATIVE_PATH_FLAG]),
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
CONFIG_MAYA = CONFIG_MAYA_TYPE(**CONFIG_MAYA_2017_DEFAULT)._asdict()


############
CONFIG_BLENDER_DEFAULT = {
    APP_ID: '1b986ef9-72bf-4c21-8e0c-06df8e5acaa9',
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



############
CONFIGURATION_DEFAULT = {DESC_ENVAR: CONFIG_ENVAR, DESC_CONFIG_INFO: CONFIG_INFO, DESC_CONFIG_GUNNY: CONFIG_GUNNY,
                         DESC_CONFIG_BLENDER: CONFIG_BLENDER_DEFAULT, DESC_CONFIG_MAYA: CONFIG_MAYA_2017_DEFAULT,
                         DESC_CONFIG_3DSMAX: CONFIG_3DSMAX_2018_DEFAULT
                         }
CONFIGURATION_TYPE = namedtuple(CONFIG_DATA_TYPENAME, (DESC_ENVAR, DESC_CONFIG_INFO, DESC_CONFIG_GUNNY, DESC_CONFIG_BLENDER,
                                                       DESC_CONFIG_MAYA, DESC_CONFIG_3DSMAX))
DEFAULT_CONFIGURATION = CONFIGURATION_TYPE(**CONFIGURATION_DEFAULT)._asdict()
JSON_ENCODER_SPEC.add_mapping(CONFIGURATION_TYPE)

IGNORE_CONFIG_BLOCK = [DESC_ENVAR, DESC_CONFIG_INFO, DESC_CONFIG_GUNNY]



CONFIG_PROJECT_DEFAULT = {
    PROJECT_ROOT: ConfigPath(paths=["", ],
                        flags=[ABSOLUTE_PATH_FLAG, ]),
    ASSET_ROOT: ConfigPath(paths=["", ],
                        flags=[PROJECT_ROOT, ]),
    EXPORT_ROOT: ConfigPath(paths=["", ],
                        flags=[ABSOLUTE_PATH_FLAG, ]),
    EXPORT_RELATIVE: ConfigPath(paths=["", ],
                        flags=[EXPORT_ROOT, ]),
    ASSET_COMMON: ConfigPath(paths=["", ],
                        flags=[ASSET_ROOT, ]),
    DCC_PROJECT: ConfigPath(paths=["", ],
                        flags=[ABSOLUTE_PATH_FLAG, ]),
    MAX_FILE_TYPE: ConfigPath(paths=["b4d31e56-5b75-4020-9474-b5fcb1c6c7e7", ],
                        flags=[DESC_CONFIG_3DSMAX, ]),
    MAYA_FILE_TYPE: ConfigPath(paths=["a5472549-704d-4505-a50d-ef3baeee87b2", ],
                              flags=[DESC_CONFIG_MAYA, ]),
    BLENDER_FILE_TYPE: ConfigPath(paths=["1b986ef9-72bf-4c21-8e0c-06df8e5acaa9", ],
                              flags=[DESC_CONFIG_BLENDER, ]),
    # TGA_FILE_TYPE: ConfigPath(paths=["", ],
    #                           flags=[]),
    # BMP_FILE_TYPE: ConfigPath(paths=["", ],
    #                           flags=[]),
    # PNG_FILE_TYPE: ConfigPath(paths=["", ],
    #                           flags=[]),
    # PSD_FILE_TYPE: ConfigPath(paths=["", ],
    #                           flags=[]),
}
CONFIG_PROJECT_TYPE = namedtuple(CONFIG_PROJECT_TYPENAME, (PROJECT_ROOT, ASSET_ROOT, EXPORT_ROOT, EXPORT_RELATIVE,
                                                           ASSET_COMMON, DCC_PROJECT, MAX_FILE_TYPE, MAYA_FILE_TYPE,
                                                           BLENDER_FILE_TYPE))
CONFIG_PROJECT = CONFIG_PROJECT_TYPE(**CONFIG_PROJECT_DEFAULT)._asdict()
JSON_ENCODER_SPEC.add_mapping(CONFIG_PROJECT_TYPE)
