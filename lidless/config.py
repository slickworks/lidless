from os.path import expanduser, dirname, join, exists
import json
from lidless.collect import collect_nodes
from lidless.exceptions import UserError
from lidless.models import Target
from lidless.tools import get_tool


BASE = dirname(dirname(dirname(__file__)))  # TODO: change!
DEFAULT_CONFIG_FILE = join(BASE, "backup.config.json")
DEFAULT_CACHE_DIR = join(BASE, ".cache")


class Config:
    def __init__(
        self, config_file=DEFAULT_CONFIG_FILE, cache_dir=DEFAULT_CACHE_DIR, data=None
    ) -> None:
        self.config_file = expanduser(config_file)
        self.cache_dir = expanduser(cache_dir)
        self._data = data or self._load()
        self._validate()
        self.roots = self._data["roots"]
        self.settings = self._data["settings"]
        self.targets = self._data["targets"]

    def _load(self):
        if exists(self.config_file):
            with open(self.config_file) as fp:
                return json.load(fp)
        else:
            return {"nodes": {}, "exclude": [], "targets": {}}

    def _validate(self):
        pass

    def get_target(self, target_key, with_nodes=True):
        try:
            data = self.targets[target_key]
        except KeyError:
            valid_keys = ", ".join(self.targets.keys())
            raise UserError(f"Invalid target '{target_key}' - must be one of [{valid_keys}]")

        tags = data.pop("tags", [])
        dest = data.pop("dest", "")
        nodes = []
        if with_nodes:
            nodes = self.get_nodes(tags, dest)

        return Target(
            name=target_key,
            tags=tags,
            dest=dest,
            tool=get_tool(data),
            nodes=nodes
        )

    def get_nodes(self, tags, base_dest):
        roots = self.roots
        default_tags = self.settings.get("default_tags", [])
        return collect_nodes(roots, base_dest, tags, default_tags)
