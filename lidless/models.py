from dataclasses import dataclass
from lidless.utils import convert_size


class Tool:
    def backup(self, nodes, no_prompt, print_only, diff_only):
        raise NotImplementedError()

    def restore(self, nodes, no_prompt, print_only, diff_only):
        raise NotImplementedError()

    cmd = "echo {src} && echo {dest} && ech {opts}"

    def _get_cmd(self, src, dest, opts):
        return self.cmd.format(src=src, dest=dest, opts=opts)

    def __str__(self):
        return f"{type(self).__name__}"


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
    size: int

    def __str__(self):
        size = convert_size(self.size)
        return f"{self.action} {size: >8}   {self.path}"


@dataclass
class Target:
    """
    A backup target.
    """

    name: str
    tags: list[str]
    tool: Tool
    nodes: list[Node]
