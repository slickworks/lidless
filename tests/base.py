from os.path import dirname, join
from lidless import Config


TMP_DIR = join(dirname(__file__), "tmp")
ROOT = dirname(dirname(__file__))
CONFIG_FILE = join(TMP_DIR, "config.json")
CACHE_DIR = join(TMP_DIR, "cache")
SRC_DIR = join(TMP_DIR, "src")
DEST_DIR = join(TMP_DIR, "dest")
REMOTE = "test"


class BaseAll:
    """
    Base class for all tests.
    """

    def setup_method(self):
        self.roots = {}
        self.targets = {}
        self.settings = {}
        self.default_dest = DEST_DIR

    def create_target(self, **kwargs):
        target = {"tool": "rsync", "dest": self.default_dest}
        target.update(kwargs)
        return target

    def get_config(self):
        data = {
            "roots": self.roots,
            "settings": self.settings,
            "targets": self.targets,
        }
        return Config(CONFIG_FILE, CACHE_DIR, data)

    def get_target(self, key):
        return self.get_config().get_target(key)

    def get_nodes(self, key):
        return self.get_target(key).nodes
