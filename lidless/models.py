import os
from dataclasses import dataclass
from lidless.utils import convert_size


class Tool:
    """
    Subclasses must:
        - Be dataclasses.
        - Specify own fields.
        - Implement public methods using same signatures.
    """
    cmd = "echo {src} && echo {dest} && ech {opts}"

    def _get_cmd(self, src, dest, opts):
        return self.cmd.format(src=src, dest=dest, opts=opts)

    def __str__(self):
        return f"{type(self).__name__}"

    def backup(self, nodes, no_prompt, print_only, diff_only):
        raise NotImplementedError()

    def restore(self, nodes, no_prompt, print_only, diff_only):
        raise NotImplementedError()


@dataclass
class Node:
    """
    A node in the tree of paths.
    """
    path: str
    tags: list[str]
    exclude: list[str]
    data: dict
    _parent: dict
    _relpath: str

    def save(self):
        data = {}
        if self.tags:
            data["tags"] = self.tags
        if self.exclude:
            data["exclude"] = self.exclude
        self._parent[self._relpath] = data


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
class GitChanges:
    path: str
    uncommitted: list[str]
    unpushed: list[str]

    def __str__(self):
        lines = [f"{os.linesep}  {self.path}"]
        if self.uncommitted:
            lines.append("    Uncommitted changes:")
            lines.extend(f"      {s}" for s in self.uncommitted)
        if self.unpushed:
            lines.append("    Unpushed commits:")
            lines.extend(f"      {s}" for s in self.unpushed)
        return os.linesep.join(lines)


@dataclass
class Target:
    """
    A backup target.
    """

    name: str
    tags: list[str]
    tool: Tool
    nodes: list[Node]
