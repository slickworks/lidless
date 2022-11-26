import os

from dataclasses import dataclass
from lidless.exceptions import DataclassInitErr


@dataclass
class BaseTool:
    """
    Subclasses must implement public methods using same signatures.
    Subclasses may specify additional dataclass fields.
    """
    diff_cmd = ""
    backup_cmd = ""

    def diff(self, src, dest, exclude):
        cmd = self._diff_cmd(src, dest, exclude)
        print(cmd)

    def _diff_cmd(self, src, dest, exclude):
        pass

    def backup(self, src, dest, exclude):
        cmd = self.backup_cmd.format(src=src, dest=dest, exclude=exclude)
        print(cmd)

    def __str__(self):
        return f"{type(self).__name__}:{os.linesep}{super().__str__()}"


class RsyncBase(BaseTool):

    def add_exclude(self, cmd, exclude):
        for ex in exclude:
            cmd += f" --exclude {ex}"


@dataclass
class Rsync(RsyncBase):
    dest: str = ''
    backup_cmd: str = "rsync -a {src} {dest} --delete-after"
    diff_cmd: str = "rsync {src} {dest} -r --delete-after"
    restore_cmd: str = "rsync {dest} {src} -r --delete-after"

    def backup(self, src, dest, exclude):
        safe_target = os.environ.get("LIDLESS_SYNC_SAFE_TARGET", "")
        if len(safe_target):
            assert dest.startswith(safe_target)
        super().backup(src, dest, exclude)


@dataclass
class Rclone(BaseTool):
    diff_cmd = "rclone sync {src} {provider}:{dest} --exclude-from {exclude}"
    provider: str


config = {
    "rsync": Rsync,
    "rclone": Rclone,
}


def get_tool(data: dict) -> BaseTool:
    try:
        key = data.pop("tool")
    except KeyError:
        raise
    cls = config[key]
    try:
        return cls(*data)
    except TypeError as err:
        raise DataclassInitErr(key, err)
