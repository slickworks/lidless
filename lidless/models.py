from dataclasses import dataclass

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from config import Config


@dataclass
class Node:
    config: "Config"
    path: str
    dest: str
    exclude: list[str]

    @property
    def exclude_file(self):
        return self.config.get_exclude_file(self.path, self.exclude)


@dataclass
class Change:
    """
    Describes a change between a node and a remote.
    """

    path: str
    action: str

