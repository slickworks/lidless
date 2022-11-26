from tests.base import CONFIG_FILE, CACHE_DIR, DEST_DIR
from lidless import Config


class TestBase:
    def setup_method(self):
        self.roots = {}
        self.targets = {}
        self.settings = {}
        self.default_dest = DEST_DIR

    def create_target(self, **kwargs):
        target = {
            "tool": "rsync",
            "dest": self.default_dest
        }
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


class BaseWithTarget(TestBase):

    target_key = "ext"
    target_tag = "foo"

    def setup_method(self):
        super().setup_method()
        self.targets[self.target_key] = self.create_target(tags=[self.target_tag])