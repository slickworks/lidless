from dataclasses import dataclass
from lidless.tools import BaseTool


@dataclass
class Node:
    path: str
    tags: list[str]
    exclude: list[str]
    data: dict


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
    tags: list[str]
    tool: BaseTool
    nodes: list[Node]
