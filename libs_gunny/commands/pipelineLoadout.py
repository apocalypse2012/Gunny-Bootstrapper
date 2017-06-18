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
Module Documentation: MpPy\mp_command\loudout.py

Startup class to manage GDS Workspace file migration services for the DCC pipeline.
"""
import errno
import os, sys
import shutil, stat
import traceback
from .baseCommand import Command
from libs_gunny.commands import util

PIPELINE_PATH = 'gds/pipeline'
PIPELINE_MARKER = 'pipeline_root'
DCC_PATH = 'dcc'
SHARED_PATH = 'shared'
ROOT_FILES = 'root_files'
ASSETS_FOLDER = 'assets'
START_SERVICE_FILE = 'startService.exe'

if os.name == "nt":
    # Subbing in Windows compatible operations on symlinks for cross platform operation.
    os.symlink = util.symlink_ms
    os.path.islink = util.islink_ms
    os.unlink = os.rmdir


def ensure_directory(path):
    if os.path.islink(path):
        os.unlink(path)
    try:
        os.makedirs(path)
    except OSError as err:
        if err.errno != errno.EEXIST:
            print("Directory Copy Failed: {}\n{}".format(path, err))


def ensure_symlink(target_path, source_path):
    if os.path.exists(source_path):
        if os.path.exists(target_path):
            if os.path.islink(target_path):
                return
            shutil.rmtree(target_path)
        source_parent = os.path.dirname(target_path)
        ensure_directory(source_parent)
        os.symlink(source_path, target_path)


def ensure_file(relative_file, target_path, root):
    source_file = os.path.join(root, relative_file)
    target_file = os.path.join(target_path, relative_file)
    if os.path.exists(target_file):
        target_time = os.path.getmtime(target_file)
        source_time = os.path.getmtime(source_file)
        if source_time <= target_time:
            DELETE_ME.log.info("Copy Refused: {}".format(target_file))
            return
    try:
        ensure_directory(os.path.dirname(target_file))
        shutil.copy2(source_file, target_file)
        os.chmod(target_file, stat.S_IWRITE)
    except Exception as err:
        # T, V, TB = sys.exc_info()
        print("Copy Failed: {}\n{}".format(target_file, err))


def get_relative_files(walk_start_dir):
    files = []
    for dirpath, dirnames, filenames in os.walk(walk_start_dir):
        relative_path = os.path.relpath(dirpath, walk_start_dir)
        for filename in filenames:
            relative_file = os.path.join(relative_path, filename)
            norm_file = os.path.normpath(relative_file)
            files.append(norm_file)
    return files


def copy_proc(wsRootPath):
    sdk_pipeline_path = util.STARTSERVICE_PATH

    file_migration = ((wsRootPath, os.path.join(sdk_pipeline_path, ROOT_FILES)),
                      (os.path.join(wsRootPath, ASSETS_FOLDER), ''),
                      (os.path.join(wsRootPath, PIPELINE_PATH), (
                          os.path.join(sdk_pipeline_path, START_SERVICE_FILE),
                          os.path.join(sdk_pipeline_path, PIPELINE_MARKER))
                       ),
                      (os.path.join(wsRootPath, PIPELINE_PATH, DCC_PATH), os.path.join(sdk_pipeline_path, DCC_PATH)),
                      (os.path.join(wsRootPath, PIPELINE_PATH, SHARED_PATH), os.path.join(sdk_pipeline_path,
                                                                                              SHARED_PATH)))
    for targetDir, sourceDir in file_migration:
        ensure_directory(targetDir)
        filesToCopy = []
        if isinstance(sourceDir, tuple):
            for dir in sourceDir:
                sourceDir, filename = os.path.split(dir)
                filesToCopy.append(filename)
        elif os.path.isfile(sourceDir):
            sourceDir, filename = os.path.split(sourceDir)
            filesToCopy = [filename]
        elif os.path.isdir(sourceDir):
            filesToCopy = get_relative_files(sourceDir)
        else:
            filesToCopy = []

        for file_val in filesToCopy:
            ensure_file(file_val, targetDir, sourceDir)


def symlink_proc(wsRootPath):
    ensure_directory(wsRootPath)
    ensure_directory(os.path.join(wsRootPath, ASSETS_FOLDER))
    ensure_symlink(os.path.join(wsRootPath, PIPELINE_PATH), util.STARTSERVICE_PATH)
    root_files_path = os.path.join(util.STARTSERVICE_PATH, ROOT_FILES)
    filesToCopy = get_relative_files(root_files_path)
    for file_val in filesToCopy:
        ensure_file(file_val, wsRootPath, root_files_path)


class Pipeline_Loadout(Command):

    PARSER_DESC = 'Add DCC toolchain to workspace root.'
    WORKSPACE_ROOT = 'Workspace'
    COPY_STATE = 'copy_files'

    def __init__(self, subParsers):
        self.wsRootPath = None
        self.isCopy = False
        super(Pipeline_Loadout, self).__init__(subParsers)

    def registerArguments(self, parser):

        parser.add_argument(self.WORKSPACE_ROOT,
                            help="Supply the full path to the workspace root.")

        parser.add_argument("-c",
                            "--copy",
                            help="Copy files for DCC toolchain.",
                            default=self.isCopy,
                            dest=self.COPY_STATE,
                            action="store_true")

    def setState(self, args):
        """ Use the args properties to set state into on the class. Return self. """
        print(args)
        dictArgs = vars(args)
        self.isCopy = dictArgs.get(self.COPY_STATE, None)
        self.wsRootPath = dictArgs.get(self.WORKSPACE_ROOT, None)
        return self


    def doCommand(self):
        """ execute the intended procedure. """
        if os.path.exists(self.wsRootPath):
            if self.isCopy:
                copy_proc(self.wsRootPath)
            else:
                symlink_proc(self.wsRootPath)
            retCode = 1 #os.EX_OK

        else: # not responsible for creating the workspace directory. If it doesn't exist fail and exit.
            retCode = 2 #os.EX_USAGE

        return retCode
