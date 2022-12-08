import os
from os.path import expanduser, join, exists
import json
import pprint

from lidless.collect import collect_nodes
from lidless.exceptions import UserError, LidlessConfigError
from lidless.models import Target, Node
from lidless.tools import get_tool

LIDLESS_USER_DIR_ENV = "LIDLESS_USER_DIR"


def get_user_dir(user_dir=None):
    if not user_dir:
        try:
            user_dir = os.environ[LIDLESS_USER_DIR_ENV]
        except KeyError:
            raise LidlessConfigError(f"You must set {LIDLESS_USER_DIR_ENV} env var")
    return expanduser(user_dir)


class Config:
    def __init__(self, user_dir=None, data=None) -> None:
        user_dir = get_user_dir(user_dir)
        self.config_file = join(user_dir, "config.json")
        self.cache_dir = join(user_dir, "cache")
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
            return {"roots": {}, "settings": {}, "targets": {}}

    def _validate(self):
        for key in ["roots", "targets", "settings"]:
            if key not in self._data:
                data = pprint.pformat(self._data)
                raise LidlessConfigError(
                    f"Expected key {key} in config {os.linesep}{data}"
                )

    def save(self):
        with open(self.config_file, "w") as fp:
            json.dump(self._data, fp, indent=4, sort_keys=True)
        print("Config saved.")

    def target_keys(self):
        return list(self._data["targets"].keys())

    def get_target(self, target_key, with_nodes=True):
        try:
            data = self.targets[target_key]
        except KeyError:
            valid_keys = ", ".join(self.targets.keys())
            raise UserError(
                f"Invalid target '{target_key}' - must be one of [{valid_keys}]"
            )

        tags = data.pop("tags", [])
        nodes = []
        if with_nodes:
            nodes = self.get_nodes(tags)

        return Target(name=target_key, tags=tags, tool=get_tool(data), nodes=nodes)

    def get_nodes(self, tags=None) -> list[Node]:
        roots = self.roots
        default_tags = self.settings.get("default_tags", [])
        return collect_nodes(roots, tags, default_tags)

    def get_node(self, path: str) -> Node:
        """
        Returns an editable Node by path.
        """
        matches = []
        for node in self.get_nodes():
            if node.path == path:
                return node
            if path.startswith(node.path):
                matches.append(node)
        if matches:
            matches.sort(key=lambda x: len(x.path), reverse=True)
            closest = matches[0]
            relpath = path[len(closest.path):]
            parent = closest._parent[closest._relpath]
        else:
            relpath = path
            parent = self.roots
        return Node(
            path=path,
            tags=[],
            exclude=[],
            data={},
            _parent=parent,
            _relpath=relpath,
        )
