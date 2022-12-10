from dataclasses import dataclass
from typing import Optional

from lidless.models import Actions, Change
from lidless.utils import join_paths
from .base_rsync import RsyncBase


@dataclass
class Rsync(RsyncBase):
    maps: dict
    cmd: str = "rsync {opts} --mkpath {src} {dest} --delete"
    exclude_from: Optional[str] = None

    def _get_cmd_opts(self, diff_only, reverse):
        if diff_only:
            # Use %n rather than %f as %f prints full path for "send" but 
            # relative paths for "del." entries. We join the base path later.
            opts = '-ain --out-format="%o %l %n"'
        else:
            opts = "-az"
        if self.exclude_from:
            opts += f' --exclude-from "{self.exclude_from}"'
        return opts

    def _parse_output(self, node, output) -> Optional[Change]:
        if output:
            action, size, path = output.split(" ", maxsplit=2)
            path = join_paths(node.path, path)
            return Change(action=self._parse_action(action), size=int(size), path=path)
        
    def _parse_action(self, action) -> str:
        if action == "send":
            return Actions.copy
        elif action == "del.":
            return Actions.delete
        else:
            return Actions.unknown
    