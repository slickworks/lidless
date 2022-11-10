import os
from pydantic import BaseModel


class BaseTool(BaseModel):

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


class Rsync(BaseTool):
    diff_cmd = "rsync {src} {dest} -r --delete-after --exclude-from {exclude}"
    dest: str

    def sync(self, src, dest, exclude):
        safe_target = os.environ.get("LIDLESS_SYNC_SAFE_TARGET", "")
        if len(safe_target):
            assert dest.startswith(safe_target)
        super().sync(src, dest, exclude)


class Rclone(BaseTool):
    diff_cmd = "rclone sync {src} {provider}:{dest} --exclude-from {exclude}"
    dest: str
    provider: str


config = {
    "rsync": Rsync,
    "rclone": Rclone,
}


def get_tool(name, remote_data) -> BaseTool:
    name = remote_data["tool"]
    cls = config[name]
    return cls(**remote_data)
