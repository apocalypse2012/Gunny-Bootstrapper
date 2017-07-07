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
Module Documentation: MpPy\mp_config\constants.py

< document module here>
"""

import os

# String Literals
bitDepth64 = str('64bit')

# Pipeline filesystem root markers. Stub file names.
DCCFOLDER_FILEMARKER = str('dcc_root')
PIPELINEFOLDER_FILEMARKER = str('pipeline_root')
PROJECTFOLDER_FILEMARKER = str('project_root')
CONFIG_FILE_NAME = str('config.json')

# Environment Variables - In use
ENVAR_GUNNY_ROOT = str('GUNNY_ROOT')
ENVAR_TOOLS_PATH = str('GUNNY_TOOLS')
ENVAR_DCC_PATH = str('GUNNY_DCC')
ENVAR_PY_PACKAGES_PATH = str('GUNNY_PY_PACKAGES')
ENVAR_PY_PACKAGES_3RDPARTY_PATH = str('GUNNY_PY_PACKAGES_3RDPARTY')
ENVAR_APPDATA = str('GUNNY_APPDATA')
ENVAR_COMPANY = str('GUNNY_COMPANY')

# Gunny Path Config
GUNNY_ROOT = str('gunny_root')
TOOLS_PATH = str('gunny_tools')
DCC_PATH = str('gunny_dcc')
PY_PACKAGES_PATH = str('gunny_py_packages')
PY_PACKAGES_3RDPARTY_PATH = str('gunny_py_packages_3rdparty')
APPDATA = str('gunny_appdata')

# Config keys
DESC_ENVAR = str('env_variables')
DESC_CONFIG_INFO = str('info')
DESC_CONFIG_PROPERTIES = str('properties')
DESC_CONFIG_GUNNY = str('Gunny')
DESC_CONFIG_PROJECT = str('project')
DESC_CONFIG_DCC = str('dcc_Application')
DESC_CONFIG_MAYA = str('dcc_Maya')
DESC_CONFIG_MAYAPY = str('dcc_Mayapy')
DESC_CONFIG_3DSMAX = str('dcc_3dsmax')
DESC_CONFIG_BLENDER = str('dcc_Blender')
DESC_CONFIG_USER = str('userConfig')

# Config types
CONFIG_INFO_TYPENAME = str('CONFIG_INFO_TYPE')
CONFIG_GUNNY_TYPENAME = str('CONFIG_GUNNY_TYPE')
CONFIG_DCC_TYPENAME = str('CONFIG_DCC_TYPE')
#CONFIG_MAYAPY_TYPENAME = str('CONFIG_MAYAPY_TYPE')
CONFIG_MAYA_TYPENAME = str('CONFIG_MAYA_TYPE')
CONFIG_3DSMAX_TYPENAME = str('CONFIG_3DSMAX_TYPE')
CONFIG_DATA_TYPENAME = str('CONFIGURATION_TYPE')

# DCC Config keys, bootstrap process
EXECUTABLE_COMMAND = str('executableFile')
REG_ENTRY_INSTALL = str('installRegKey')
REG_PATH_INSTALL = str('installRegPaths')
ENV_PATH_INSTALL = str('installEnvPaths')
BOOTSTRAP_TYPE = str('startScriptVar')
BOOTSTRAP_FILE = str('startScriptVal')
APP_ROOT_TYPE = str('appRoot')
APP_CONFIG_PATH = str('appConfigPath')
APP_VERSION = str('appVersion')
APP_ID = str('appguid')
APP_PY_PACKAGES = str('appPyPackage')

# Parser qualifiers. Blocks mapped to these indices have a special case association.
COMMENT_QUALIFIER = str('user_comment')
TEMPLATE_QUALIFIER = str('metadata_template')

# ConfigPath Block flags. The presence of these descriptors in a block specifies a use case.
PYTHON_PATH_FLAG = str('addPySiteDir')
ENV_VAR_FLAG = str('addEnv')
ABSOLUTE_PATH_FLAG = str('absolute')  # absolute\relative are serialization flags.
RELATIVE_PATH_FLAG = str('relative')  # runtime state of the path values are always fully resolved.
PROJECT_RELATIVE_FLAG = str('project_relative')  # runtime state of the path values are always fully resolved.
ROOT_PATH_FLAG = str('root')

# MAYA Custom Config Keys
MAYA_SCRIPT_PATH = str('MAYA_SCRIPT_PATH')
XBMLANG_PATH = str('XBMLANGPATH')
MAYA_PLUG_IN_PATH = str('MAYA_PLUG_IN_PATH')

# 3DSMAX Custom Config Keys
MAX_PLUGIN_PATH = str('MAX_PLUGIN_PATH')

# BLENDER Custom Config Keys

# Config Values
STR_2018 = str('2018')
STR_2017 = str('2017')
STR_2016 = str('2016')
STR_2015 = str('2015')
STR_2014 = str('2014')
PYTHON_PATH = str('PYTHONPATH')
DIR_MAYA = str('maya')
DIR_ICONS = str('icons')
DIR_SCRIPTS = str('scripts')
DIR_MEL = str('mel')
DIR_PYTHON = str('python')
DIR_PLUGINS = str('plugins')
DIR_SHARED = str('shared')

# MAYA Config Values
MAYAPY_RELATIVE_EXE_PATH = str('bin\\mayapy.exe')
MAYA_RELATIVE_EXE_PATH = str('bin\\maya.exe')
MAYA_SETUP_FILE = str('userSetup.py')
MAYA_WORKSPACE_FILE = str('workspace.mel')
MAYA_REG_KEY = str('MAYA_INSTALL_LOCATION')
MAYA_REG_PATH_2017 = str('SOFTWARE\\Autodesk\\Maya\\2017\\Setup\\InstallPath')
MAYA_REG_PATH_2016 = str('SOFTWARE\\Autodesk\\Maya\\2016\\Setup\\InstallPath')
MAYA_ENV_PATH = str('MAYA_LOCATION')


MAYA_PATH_SCRIPTS_2017 = os.path.join(DIR_MAYA, STR_2017, DIR_SCRIPTS)
MAYA_PATH_MEL_2017 = os.path.join(DIR_MAYA, STR_2017, DIR_SCRIPTS, DIR_MEL)
MAYA_PATH_PYTHON_2017 = os.path.join(DIR_MAYA, STR_2017, DIR_SCRIPTS, DIR_PYTHON)
MAYA_PATH_ICONS_2017 = os.path.join(DIR_MAYA, STR_2017, DIR_ICONS)
MAYA_PATH_PLUGINS_2017 = os.path.join(DIR_MAYA, STR_2017, DIR_PLUGINS)

MAYA_PATH_SCRIPTS_2016 = os.path.join(DIR_MAYA, STR_2016, DIR_SCRIPTS)
MAYA_PATH_MEL_2016 = os.path.join(DIR_MAYA, STR_2016, DIR_SCRIPTS, DIR_MEL)
MAYA_PATH_PYTHON_2016 = os.path.join(DIR_MAYA, STR_2016, DIR_SCRIPTS, DIR_PYTHON)
MAYA_PATH_ICONS_2016 = os.path.join(DIR_MAYA, STR_2016, DIR_ICONS)
MAYA_PATH_PLUGINS_2016 = os.path.join(DIR_MAYA, STR_2016, DIR_PLUGINS)

MAYA_PATH_SCRIPTS = os.path.join(DIR_MAYA, DIR_SCRIPTS)
MAYA_PATH_MEL = os.path.join(DIR_MAYA, DIR_SCRIPTS, DIR_MEL)
MAYA_PATH_PYTHON = os.path.join(DIR_MAYA, DIR_SCRIPTS, DIR_PYTHON)
MAYA_PATH_ICONS = os.path.join(DIR_MAYA, DIR_ICONS)
MAYA_PATH_PLUGINS = os.path.join(DIR_MAYA, DIR_PLUGINS)



# Environment Variables - Unused
# ENVAR_3DSMAX_X64_2015 = str('ADSK_3DSMAX_X64_2015')
# ENVAR_3DSMAX_X64_2016 = str('ADSK_3DSMAX_X64_2016')
# ENVAR_MAYA_LOCATION = str('MAYA_LOCATION')
# ENVAR_MAYA_MODULE_PATH = str('MAYA_MODULE_PATH')
# ENVAR_MAYA_PLUG_IN_PATH = str('MAYA_PLUG_IN_PATH')
# ENVAR_MAYA_PLUG_IN_RESOURCE_PATH = str('MAYA_PLUG_IN_RESOURCE_PATH')
# ENVAR_MAYA_PRESET_PATH = str('MAYA_PRESET_PATH')
# ENVAR_MAYA_SCRIPT_PATH = str('MAYA_SCRIPT_PATH')
# ENVAR_PYTHONHOME = str('PYTHONHOME')
# ENVAR_PYTHONPATH = str('PYTHONPATH')
# ENVAR_MP_PROJECT = str('MP_PROJECT')
# ENVAR_MP_PROJECT_PATH = str('MP_PROJECT_PATH')
# ENVAR_MP_BOOTSTRAP = str('MP_BOOTSTRAP')
# ENVAR_MP_PYTHON_PATH = str('MP_PYTHON_PATH')
# ENVAR_MP_DEBUG = str('MP_DEBUG')
