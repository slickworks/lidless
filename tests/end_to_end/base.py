import os
from os.path import dirname, join
import glob
import unittest
import json
import shutil


# TODO: set LIDLESS_SYNC_SAFE_TARGET and assest it is set

from lidless.main import cmd_backup

from lidless.tools import Rsync
from lidless.utils import join_paths, create_file, create_dir

# assert Rsync.

from tests.common import TestBase, TMP_DIR, SRC_DIR, DEST_DIR


def local(path):
    return join(TMP_DIR, path)


def clean_lines(file_list_str) -> list[str]:
    lines = []
    for line in file_list_str.split(os.linesep):
        line = line.strip() 
        if len(line):
            lines.append(line)
    lines.sort()
    return lines


def create_dir_contents(base, file_list_str) -> None:
    for line in clean_lines(file_list_str):
        path = join_paths(base, line)
        if "." in line:
            create_file(path, "foo")
        else:
            create_dir(path)


def read_dir_contents(path) -> list[str]:
    lines = glob.glob("**/*", root_dir=path, recursive=True)
    lines.sort()
    return lines


class EndToEndTest(TestBase):
    config_file = {}

    # @classmethod
    # def setUpClass(cls):
    #     os.makedirs(CACHE_DIR, exist_ok=True)
    #     with open(CONFIG_FILE, "w") as fp:
    #         json.dump(cls.config_file, fp, indent=4)
        
    # @classmethod
    # def tearDownClass(cls):
    #     os.rmdir(CACHE_DIR)

    def setUp(self):
        os.makedirs(TMP_DIR, exist_ok=True)
        super().setUp()

    def tearDown(self):
        shutil.rmtree(TMP_DIR)

    def setSrcDir(self, file_list_str):
        create_dir_contents(SRC_DIR, file_list_str)

    def setDestDir(self, file_list_str):
        create_dir_contents(DEST_DIR, file_list_str)

    def cmd_backup(self, *args, **kwargs):
        # TODO: check that paths are in tmp dir for safety?
        cmd_backup(self.ctrl, *args, **kwargs)

    def assertDest(self, file_list_str):
        self.assertEqual(read_dir_contents(DEST_DIR), clean_lines(file_list_str))
