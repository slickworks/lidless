from dataclasses import dataclass
from lidless.tools import BaseTool


@dataclass
class Target:
    """
    A backup target.
    """
    name: str
    dest: str
    tags: list[str]
    tool: BaseTool


    def cmd_show(self, args):
        """
        Shows collection data.
        """

    def cmd_changes(self, args):
        """
        Shows changes.
        """

    def cmd_backup(self, args):
        """
        Runs backup.
        """

    def cmd_restore(self, args):
        """
        Runs restore.
        """

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