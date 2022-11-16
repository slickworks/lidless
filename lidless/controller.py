from os.path import expanduser, dirname, join, exists
import json

from lidless.exceptions import LidlessConfigError
from lidless.models import Node, Target
from lidless.tools import get_tool
from lidless.utils import join_paths, find_duplicates
from lidless.collect import collect_nodes

BASE = dirname(dirname(dirname(__file__)))  # TODO: change!
DEFAULT_CONFIG_FILE = join(BASE, "backup.config.json")
DEFAULT_CACHE_DIR = join(BASE, ".cache")


class Controller:
    # config_file: str
    # cache_dir: str

    def __init__(
        self, config_file=DEFAULT_CONFIG_FILE, cache_dir=DEFAULT_CACHE_DIR, data=None
    ) -> None:
        self.config_file = expanduser(config_file)
        self.cache_dir = expanduser(cache_dir)
        self.__data = data or {}

    @property
    def data(self):
        self._load()
        return self.__data

    def _load(self):
        if not len(self.__data):
            if exists(self.config_file):
                with open(self.config_file) as fp:
                    self.__data = json.load(fp)
            else:
                self.__data = {"nodes": {}, "exclude": [], "targets": {}}

    def get_target(self, target_key):
        roots = self.data["roots"]
        default_tags = self.data["settings"].get("default_tags", [])
        target_data = self.data["targets"][target_key]
        base_dest = target_data.get("dest", "")
        target_tags = target_data["tags"]
        return Target(
            config=self,
            name=target_key,
            tool=get_tool(target_key, target_data),
            nodes=collect_nodes(roots, base_dest, target_tags, default_tags),
        )

    # def get_exclude_file(self, path, exclude):
    #     pass

    # def _save(self):
    #     with open(self.config_file, "w") as fp:
    #         json.dump(self.__data, fp, indent=4)

    # def add_target(self, name, cmd):
    #     self.data["targets"][name] = {"cmd": cmd}
    #     self._save()

    # def add_node(self, path):
    #     pass

    # def add_repo(self, path):
        pass
