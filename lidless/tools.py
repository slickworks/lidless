import os
from pydantic import BaseModel

from dataclasses import dataclass


@dataclass
class BaseTool:
    def diff(self, src, dest, exclude):
        cmd = self._diff_cmd(src, dest, exclude)
        print(cmd)

    def _diff_cmd(self, src, dest, exclude):
        pass

    def sync(self, src, dest, exclude):
        cmd = self._sync_cmd(src, dest, exclude)
        print(cmd)

    def _sync_cmd(self, src, dest, exclude):
        pass

    def __str__(self):
        return f"{type(self).__name__}:{os.linesep}{super().__str__()}"


@dataclass
class Rsync(BaseTool):
    diff_cmd = "rsync {src} {dest} -r --delete-after --exclude-from {exclude}"

    def sync(self, src, dest, exclude):
        safe_target = os.environ.get("LIDLESS_SYNC_SAFE_TARGET", "")
        if len(safe_target):
            assert dest.startswith(safe_target)
        super().sync(src, dest, exclude)


@dataclass
class Rclone(BaseTool):
    diff_cmd = "rclone sync {src} {provider}:{dest} --exclude-from {exclude}"
    provider: str


config = {
    "rsync": Rsync,
    "rclone": Rclone,
}


def get_tool(**target_data) -> BaseTool:
    key = target_data["tool"]
    cls = config[key]
    return cls()
    # TODO: determine required args from cls and extract.
    # **target_data)
