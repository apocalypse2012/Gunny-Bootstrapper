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
PackageDocumentation: config

<document this package>
"""

import importlib

# The __init__.py files help guide import statements without automattically
# importing all of the modules
__all__ = ['config_defaults',
           'config_file_defaults',
           'config_parse',
           'bootstrap']
log_source = 'libs_gunny/config'

for pkgStr in __all__:
    try:
        importlib.import_module('.'+pkgStr, package=__name__)
    except Exception as e:
        print("{0} ImportFail: {1} in {2}\r".format(log_source, e, pkgStr))
        pass
#---------------------