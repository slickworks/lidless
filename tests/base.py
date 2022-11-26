from os.path import dirname, join
import unittest


TMP_DIR = join(dirname(__file__), "tmp")
CONFIG_FILE = join(TMP_DIR, "config.json")
CACHE_DIR = join(TMP_DIR, "cache")
SRC_DIR = join(TMP_DIR, "src")
DEST_DIR = join(TMP_DIR, "dest")
REMOTE = "test"



# class TestBase(unittest.TestCase):
#     nodes = {
#         SRC_DIR: {
#             "remotes": {
#                 REMOTE: {}
#             }
#         }
#     }
#     remotes = {
#         REMOTE: {
#             "tool": "rsync",
#             "dest": DEST_DIR
#         }
#     }

#     def setUp(self):
#         self.config = {"remotes": self.remotes, "nodes": self.nodes}
#         self.ctrl = Controller(CONFIG_FILE, CACHE_DIR, self.config)

#     def getConfigSrcDir(self) -> dict:
#         return self.ctrl.data["nodes"][SRC_DIR]

#     def getConfigRemote(self) -> dict:
#         return self.ctrl.data["remotes"][REMOTE]
    