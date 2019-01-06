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
Module Documentation: MpPy\mp_config\project_parse.py

< document module here>
"""


import json
import os
from collections import Mapping, Sequence, OrderedDict
from config_parse import Config_Parser, EnsureBackup
from config_marshall import ConfigEncoder
import config_defaults
from constants import *


class Project_Parser(Config_Parser):

    def __init__(self, file_name=None):
        self.project_file = None
        self.project_config = None

        super(Project_Parser, self).__init__()

        self.project_config = OrderedDict([(DESC_CONFIG_PROJECT, config_defaults.CONFIG_PROJECT)])
        if file_name is not None:
            self.project_file = file_name
            self.project_config = self._load_file_project(self.project_file)

        self._set_CURRENT_CONFIG__(self.project_config, clean=True)

    def _load_file_project(self, file_name):
        """
        Load configuration data from file.
        :return: loaded configuration data as an OrderedDict()
        """
        if os.path.exists(file_name):
            config_base = json.load(open(file_name.lower(), mode='r'), object_hook=ConfigEncoder.class_mapper)
            return config_base
        else:
            return None

    def SaveProjectConfig(self, file_name=None):
        default_cfg_file = file_name
        if default_cfg_file is None:
            default_cfg_file = self.project_file
        temp_file = default_cfg_file + '.TEMP'
        # TODO: Update self.project_config with parameter changes from _CURRENT_CONFIG. This will require scary changes
        # TODO: to how deep_update works in 'clean' mode. I.E. updating from a superset without pulling data that does
        # TODO: not already have a place in the subset. We need an 'intersection'.
        if os.path.exists(default_cfg_file):
            json.dump(self.project_config,
                      open(temp_file.lower(),
                           mode='w'),
                      cls=ConfigEncoder,
                      sort_keys=False,
                      indent=4)
            EnsureBackup(temp_file, default_cfg_file)
        else:
            path_value = os.path.dirname(default_cfg_file)
            if not os.path.isdir(path_value):
                os.mkdir(path_value)
            json.dump(self.project_config,
                      open(default_cfg_file.lower(),
                           mode='w'),
                      cls=ConfigEncoder,
                      sort_keys=False,
                      indent=4)
