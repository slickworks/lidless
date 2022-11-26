from dataclasses import dataclass
from lidless.tools import BaseTool

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from config import Config


@dataclass
class Node:
    config: "Config"
    path: str
    dest: str
    exclude: list[str]

    # @property
    # def exclude_file(self):
    #     return self.config.get_exclude_file(self.path, self.exclude)


@dataclass
class Change:
    """
    Describes a change between a node and a remote.
    """

    path: str
    action: str



@dataclass
class Target:
    """
    A backup target.
    """
    name: str
    dest: str
    tags: list[str]
    tool: BaseTool
    nodes: list[Node]

    # exclude: list[str]

    # def __init__(self, config, name, tool, nodes) -> None:
    #     self.config = config
    #     self.name = name
    #     self.tool = tool
    #     self.changes = []

    def find_changes(self) -> None:
        for node in self.nodes:
            self._add_changes(node, node.exclude_file)
            for save in node.save:
                self._add_changes(save, save.exclude_file)

    def sync(self):
        pass

    def _add_changes(self, path, exclude_file):
        changes = self.tool.diff(path, exclude_file)
        self.changes.extend(changes)