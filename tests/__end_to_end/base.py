# import os
# from os.path import dirname, join
# import glob
# import unittest
# import json
# import shutil


# # TODO: set LIDLESS_SYNC_SAFE_TARGET and assest it is set

# from lidless.main import cmd_backup

# from lidless.tools import Rsync
# from lidless.utils import join_paths, create_file, create_dir

# # assert Rsync.

# from tests.common import TestBase, TMP_DIR, SRC_DIR, DEST_DIR


# class EndToEndTest(TestBase):
#     config_file = {}

#     # @classmethod
#     # def setUpClass(cls):
#     #     os.makedirs(CACHE_DIR, exist_ok=True)
#     #     with open(CONFIG_FILE, "w") as fp:
#     #         json.dump(cls.config_file, fp, indent=4)

#     # @classmethod
#     # def tearDownClass(cls):
#     #     os.rmdir(CACHE_DIR)
