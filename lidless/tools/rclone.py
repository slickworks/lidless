from dataclasses import dataclass
from typing import Optional

from lidless.models import Actions, Change
from lidless.utils import join_paths
from .base_rsync import RsyncBase


@dataclass
class Rclone(RsyncBase):
    maps: dict
    cmd = "rclone {opts} {src} {provider}:{dest}"
    provider: str
    exclude_from: Optional[str] = None

    def _get_cmd(self, src, dest, opts):
        return self.cmd.format(src=src, dest=dest, opts=opts, provider=self.provider)

    def _get_cmd_opts(self, diff_only, reverse):
        if diff_only:
            opts = "sync --dry-run"
        else:
            opts = "sync"
        if self.exclude_from:
            opts += f' --exclude-from "{self.exclude_from}"'
        return opts

    def _parse_output(self, node, output) -> Optional[Change]:
        """
        2022/12/10 11:52:18 NOTICE: code-snippets/delete_users.py: Skipped copy as --dry-run is set (size 601)
        """
        notice = "NOTICE:"
        if output and notice in output:
            _, after = output.split(notice, maxsplit=1)
            chunks = after.split(":")
            if len(chunks) != 2:
                return
            path, comment = chunks
            comment_chunks = comment.strip().split(" ")
            action = comment_chunks[1]
            size = comment_chunks[-1].strip(")")
            path = join_paths(node.path, path.strip())
            return Change(action=self._parse_action(action), size_str=size, path=path)

    def _parse_action(self, action) -> str:
        if action == "copy":
            return Actions.copy
        elif action in ("delete", "remove"):
            return Actions.delete
        else:
            return Actions.unknown
    
